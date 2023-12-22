#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import db, Restaurant, Pizzas, Restaurant_Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return "Welcome to the API"

@app.route('/restaurants')
def restaurant():

    restaurants = [restaurant.to_dict() for restaurant in Restaurant.query.all()]

    response = make_response(
        jsonify(restaurants),
        200
    )
    return response

@app.route('/restaurants/<int:id>', methods=['GET','DELETE'])
def restaurant_by_id(id):

    if request.method == 'GET':
        restaurant = Restaurant.query.filter_by(id=id).first()

        if restaurant == None:
            response = make_response(
                jsonify({
                    "error": "Restaurant not found"
                    }),
                404
            )
            return response
        elif restaurant:

            response = make_response(
                jsonify(restaurant.to_dict()),
                200
            )
            return response
    elif request.method == 'DELETE':
        restaurant = Restaurant.query.filter_by(id=id).first()
        
        if restaurant:
            restaurant_pizza = Restaurant_Pizza.query.filter_by(restaurant_id=id).all()

            for item in restaurant_pizza:
                db.session.delete(item)
                db.session.commit()

            db.session.delete(restaurant)
            db.session.commit()

            response = make_response(
                jsonify({
                    "Delete_successful" : True,
                    "message" : " "
                }),
                200
            )
            return response
        
        elif restaurant == None:
            response = make_response(
                jsonify({
                    "error": "Restaurant not found"
                    }),
                404
            )
            return response

@app.route('/pizzas')
def pizzas():

    pizza = [pizza.to_dict() for pizza in Pizzas.query.all()]

    response = make_response(
        jsonify(pizza),
        200
    )
    return response

@app.route('/restaurant_pizzas', methods=['GET','POST'])
def restaurant_pizzas():

    data = request.get_json()

    new_restaurant_pizza = {
        "pizza_id": data["pizza_id"],
        "restaurant_id": data["restaurant_id"],
        "price": data["price"],
    }

    db.session.add(new_restaurant_pizza)
    db.session.commit()

    response = make_response(
        jsonify(new_restaurant_pizza.to_dict()),
        201
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)