import os
from flask import Flask, jsonify, request
import requests
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'products.sqlite')
# db = SQLAlchemy(app)
# render url: https://cart-wcrt.onrender.com/cart/
# render url: https://product-3q2q.onrender.com/products/
products = [
    {"id": 1, "name": "milk", "price": 1.99, "quantity" : 20},
     {"id": 2, "name": "cerel", "price": 1.50, "quantity" : 15},
      {"id": 3, "name": "banana", "price": 1.00, "quantity" : 13},
       {"id": 4, "name": "strawberries", "price": 2.00, "quantity" : 12},
        {"id": 5, "name": "pineapples", "price": 3.00, "quantity" : 20}
]

    
    
#see a list of all the avaible products, including name, price, quantiy 
@app.route('/products', methods=['GET'])
def get_products_info():
    # products = Products.query.all()
    # products_list = [{"id": product.product_id, "name": product.product_name, "quantity": product.product_quantity, "price": product.product_price} for product in products]
    return jsonify({"products": products})

 
@app.route('/products/<int:product_id>', methods=['GET']) 
def get_product_by_id(product_id):
    for product in products:
        if product['id'] == product_id:
            return jsonify({"products": product}), 200
    return jsonify({"Error" : "Product not found"}),404    



    
@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    #Didn't enter enough information
    if "name" not in data or "price" not in data or "quantity" not in data:
        return jsonify({"error": "Name, price, and quantity are required"}), 400
        
    product_name = data['name']
    product_price = data['price']
    product_quantity = data['quantity']

    # if the product already exist then +1 the quantity of that item 
    for product in products:
        if product['name'] == product_name:
            product['quantity'] += product_quantity
            return jsonify({"message" : "Product quantity has been updated"}), 200

    # if enter product withut the same name, then create a new 
    new_product = {
        "id": len(products) + 1,
        "name" : product_name,
        "price": product_price,
        "quantity": product_quantity 
    }

    products.append(new_product)


    return jsonify({'message': 'Product created successfully', 'product': new_product}) , 200

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    for product in products:
        if product['id'] == product_id:
            product.remove(product)
            return jsonify({"message": "Product deleted"}), 200
        else:
            return jsonify({"message" : "Product not found"}), 404
    
#update endpoint
@app.route('/products/<int:product_id>', methods=['POST'])
def product_to_cart(product_id):
    quant = request.get_json().get('quantity')
    
    if quant == 0:
        return jsonify({"Error": "Can't add a 0 quantity"}), 400
    
     
    
    if products[product_id -1 ]['quantity'] + quant > 0:
        products[product_id -1]['quantity'] -= quant
        
    elif products[product_id -1]['quantity'] + quant == 0:
        delete_product(product_id)
        return jsonify({"message": "Product deleted"})
    else:
        # Do I have enough inventory to decrease
        return jsonify({"Error": "There's not enough stock"}),400

    return jsonify({"message": "Product quantity updated"}), 200 
    
    
    
if __name__ == '__main__':
    app.run(debug=True,port= 5000)
    