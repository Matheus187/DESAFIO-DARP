import enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Enum as SAEnum
from app.models.base_class import Base

class UserRole(str, enum.Enum):
    ADMIN = "administrador"
    PRODUTOR = "produtor"
    COMPRADOR = "comprador"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key= True, index= True)
    full_name = Column(String(100), nullable= False)
    email = Column(String(60), nullable=False, unique=True )
    hash_password = Column(String(100), nullable= False)
    role = Column(SAEnum(UserRole), nullable=False, default= UserRole.COMPRADOR)
    localization = Column(String(30), nullable=True)

    products = relationship(
        "Produto", 
        back_populates="owner"
    )

    orders = relationship("Order", back_populates="owner")

    