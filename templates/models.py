
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from . import db

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True 
    id = Column(Integer, primary_key=True, autoincrement=True)

class Category(BaseModel):
    __tablename__ = 'category'
    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name

class Product(BaseModel):
    __tablename__ = 'product'
    name = Column(String(100), nullable=False)
    price = Column(Float, default=0)
    quantity = Column(Integer, nullable=False)
    image = Column(String(255), nullable=True)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    db.create_all()


