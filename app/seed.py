from faker import Faker
from models import Restaurant, Pizzas, Restaurant_Pizza, db
import random
from app import app

fake = Faker()

with app.app_context():
    Restaurant.query.delete()
    Pizzas.query.delete()
    Restaurant_Pizza.query.delete()
    
    db.session.commit()

    restaurants = []

    for _ in range(12):
        restaurant = Restaurant(
            name = f'Restaurant: {fake.name()}',
            address = fake.address()
        )
        restaurants.append(restaurant)

        db.session.add(restaurant)
        db.session.commit()


    pizza_size = ['Mega','Family','Large']
    pizzas = []

    for _ in range(12):
        pizza = Pizzas(
            name = f'{random.choice(pizza_size)} {fake.name()}',
            ingredients = fake.sentence()
        )
        pizzas.append(pizza)

        db.session.add(pizza)
        db.session.commit()


