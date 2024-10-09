from flask import Flask, jsonify, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

#Database connection     
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='clothing_store',
        user='root',
        password='password'
    )

#Home Page
@app.route('/')
def home():
    return render_template('home.html')

#Products Page
@app.route('/products')
def products():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    db.close()
    return render_template('products.html', products=products)

#Shopping Cart Page
@app.route('/cart')
def cart():
    return render_template('cart.html')

#Add item to cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.json['product_id']
    quantity = request.json['quantity']
    #Logic to update cart
    return jsonify({'status': 'Product added to cart'})

#Checkout Page
def checkout():
    cart_data = request.json['cart']
    total_amount = request.json['total']
    #Logic to handle order processing, payment, and inventory updates
    return jsonify({'status': 'Order processed succesfully', 'total': total_amount})

#Customer Profile Page

#Running the app
if __name__ == '__main__':
    app.run(debug=True)