import enum
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, Integer, String, Enum as SAEnum, ForeignKey, 
    CheckConstraint, Numeric
)
from app.models.base_class import Base

class ProductCategory(str, enum.Enum):
    HORTIFRUTI = "hortifruti"
    GRAOS_E_CEREAIS = "graos_e_cereais"
    PROTEINA_ANIMAL = "proteina_animal"
    LATICINIOS_E_OVOS = "laticinios_e_ovos"
    INSUMOS_AGRICOLAS = "insumos_agricolas"
    ALIMENTACAO_ANIMAL = "alimentacao_animal"
    MAQUINARIO_E_FERRAMENTAS = "maquinario_e_ferramentas"
    PROCESSADOS_E_AGROINDUSTRIA = "processados_e_agroindustria"
    OUTROS = "outros"

class Produto(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index= True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Numeric(10, 2), nullable= False)
    amount = Column(Integer, nullable= False)
    category = Column(SAEnum(ProductCategory), nullable=False, default=ProductCategory.OUTROS)
    localization = Column(String(30), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="products")

    __table_args__ = (
        CheckConstraint('price > 0', name='check_price_positive'),

        CheckConstraint('amount >= 0', name='check_amount_non_positive'),
    )