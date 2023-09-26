import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'products.sqlite')
# db = SQLAlchemy(app)

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


    return jsonify({"error": "Product not found"}), 404
    
@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    #Didn't enter enough information
    if "name" not in data or "price" not in data or "quantity" not in data:
        return jsonify({"error": "Name, price, and quantity are required"}), 400
        
    product_name = data['name'],
    product_price = data['price'],
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
    
@app.route('/products/<int:product_id>', methods=['POST'])
def product_to_cart(product_id):
    quant = request.get.json('quantity')
    user_id = request.get.json('user_id')
    
    if quant == 0:
        return jsonify({"Error": "Can't add a 0 quantity"}), 400
    
    product = get_product_by_id(product_id)
    
    if product['quantity'] + quant > 0:
        if product_id in data['items']:
            data['items'][product_id]['quantity'] += quant
            data['items'][product_id]['total_price'] +=  quant * product['price'] 
            return jsonify({"message": "Product added"})
        else:
            data['items'][product_id] = {
                "quantity" : quant,
                "total_price" : quant * product["price"]
            }
            return jsonify({"message": "Product added"})
    if product['quantity'] + quant == 0:
        delete_product(product_id)
        return jsonify({"message": "Product deleted"})
    
    # Do I have enough inventory to decrease 
    if quant > product["quantity"]:
        return jsonify({"Error": "There's not enough stock"})
    
    
    # get the users cart 
    response = request.get(f'https://cart-wcrt.onrender.com/cart/{user_id}')
    data = response.json()
    # when deleting producted  
    if product_id in data['items']:
        data['items'][product_id]['quantity'] += quant
        data['items'][product_id]['total_price'] +=  quant * product['price'] 
    
    cart_update = request.post(f'https://cart-wcrt.onrender.com/cart/{user_id}', json=data)
    
    if cart_update.status_code() != 200:
        return jsonify({"Erorr": "Couldn't update cart"})
    # now update the quantity of the change the quantity avaiable in the product 
    product['quantity'] -= quant
    
    return jsonify({"message": "Product added", "User_cart" : data}), 200 
    
    
    
if __name__ == '__main__':
    app.run(debug=True,port= 5000)
    