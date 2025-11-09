import enum
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, Integer, Enum as SAEnum, ForeignKey, Numeric
)
from app.models.base_class import Base


class OrderStatus(str, enum.Enum):
    PENDENTE = "pendente"
    PAGO = "pago"
    ENVIADO = "enviado"
    CANCELADO = "cancelado"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key= True, index= True)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(SAEnum(OrderStatus), nullable=False, default=OrderStatus.PENDENTE)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="orders")

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")