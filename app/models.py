from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates


db = SQLAlchemy()

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    pizzas = db.relationship('Restaurant_Pizza', backref='restaurant')

    def __repr__(self):
        return f"{self.id}. {self.name} restaurant's address is {self.address})"

class Pizzas(db.Model,  SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    restaurant = db.relationship('Restaurant_Pizza' , backref='pizzas')

    def __repr__(self):
        return f'{self.id}. {self.name} pizza has the following ingredients; {self.ingredients})'

class Restaurant_Pizza(db.Model,  SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    
    @validates('price')
    def check_price(self,price):
        if 30 < price < 1:
            raise ValueError('Invalid! Price should be between 1 and 30')
        return price

    def __repr__(self):
        return f'Pizza ID:{self.pizza_id} of restaurant ID: {self.restaurant_id} pizza price is{self.price})'
    
# add any models you may need. 


