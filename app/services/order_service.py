from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.models.product import Produto
from app.schemas.order import OrderCreate
from app.crud import crud_product, crud_order

def create_new_order(db: Session, *, order_in: OrderCreate, current_user: User):

    if current_user.role != UserRole.COMPRADOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas compradores podem criar pedidos."
        )

    items_para_criar_no_db = []
    produtos_para_atualizar_stock = []
    total_do_pedido = 0.0

    try:
        for item in order_in.items:
            db_product = crud_product.get(db, id=item.product_id)

            if not db_product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Produto com ID {item.product_id} não encontrado."
                )

            if db_product.amount < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stock insuficiente para '{db_product.name}'. "
                           f"Pedido: {item.quantity}, Disponível: {db_product.amount}"
                )

            preco_no_momento = db_product.price
            total_do_pedido += preco_no_momento * item.quantity

            novo_stock = db_product.amount - item.quantity
            produtos_para_atualizar_stock.append(
                {"db_obj": db_product, "novo_stock": novo_stock}
            )
            items_para_criar_no_db.append({
                "product_id": db_product.id,
                "quantity": item.quantity,
                "price_at_purchase": preco_no_momento
            })

        for p in produtos_para_atualizar_stock:
            crud_product.update(db, db_obj=p["db_obj"], obj_in={"amount": p["novo_stock"]})

        new_order = crud_order.create_order(
            db=db,
            owner_id=current_user.id,
            total=total_do_pedido,
            items_to_create=items_para_criar_no_db
        )

        db.commit()
        db.refresh(new_order) 

        return new_order

    except Exception as e:
        db.rollback()

        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro interno ao processar o pedido: {e}"
        )