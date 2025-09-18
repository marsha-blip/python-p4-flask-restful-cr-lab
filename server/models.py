from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, Integer, String, Numeric

db = SQLAlchemy()

class Plant(db.Model, SerializerMixin):
    __tablename__ = 'plants'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # Allow image to be nullable (so test creating with only name does not fail)
    image = Column(String, nullable=True, default="")  
    # Also allow price to be nullable, default 0.0
    price = Column(Numeric(10, 2), nullable=True, default=0.0)

    decimal_format = '{:.2f}'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image if self.image is not None else "",
            "price": float(self.price) if self.price is not None else 0.0
        }

