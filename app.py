from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

#Application and Database Setup
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@loacalhost/online_store'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Necessary Tables
class Product(db.Model):
    __tablename__ = 'Products'
    ProductID = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(100))
    Price = db.Column(db.Numeric(10, 2))
    Stock = db.Column(db.Integer)

class CartItem(db.Model):
    __tablename__ = 'CartItems'
    CartItemID = db.Column(db.Integer, primary_key=True)
    CartID = db.Column(db.Integer, db.ForeignKey('ShoppingCart.CartID'))
    ProductID = db.Column(db.Integer, db.ForeignKey('Products.ProductID'))
    Quantity = db.Column(db.Integer)

class ShoppingCart(db.Model):
    __tablename__ = 'ShoppingCart'
    CartID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('Customers.CustomerID'))
    CreatedAt = db.Column(db.DateTime, default=db.func.current_timestamp())

#Automated Database Setup
def setup_database():
    with open('schema.sql', 'r') as file:
        schema_sql = file.read()
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cursor.execute(schema_sql)
        conn.commit()
        cursor.close()
        conn.close()

#Home Page
@app.route('/')
def home():
    return render_template('home.html')

#Products Page
@app.route('/products')
def products():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    db.close()
    return render_template('products.html', products=products)

#Get Products
@app.route('/get_products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_list.append({
            'id': product.ProductID,
            'name': product.Name,
            'price': str(product.Price),
            'decription': product.Description,
            'image': product.Image
        })
    return jsonify(product_list), 200

#Shopping Cart Page
@app.route('/cart')
def cart():
    return render_template('cart.html')

#Add item to cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity', 1)
    customer_id = session.get('customer_id')
    
    if not customer_id:
        return jsonify({'error': 'Customer is not logged in'}), 401
    
    #Getting customer cart or making one
    cart = ShoppingCart.query.filter_by(CustomerId=customer_id).first()
    if not cart:
        cart = ShoppingCart(CustomerId=customer_id)
        db.session.add(cart)
        db.session.commit()
    
    #Ensuring product exists and in stock
    product = Product.query.filter_by(ProductID=product_id).first()
    if not product: return jsonify({'error': 'Product does not exist'}), 404
    if product.Stock < quantity: return jsonify({'error': f'Not enough stock for {product.ProductName}. Only {product.Stock} left'}), 400

    #Adding item to customers cart
    cart_item = CartItem.query.filter_by(CartID=cart.CartID, ProductID=product_id).first()

    try:
        if cart_item:
            cart_item.Quantity += quantity
        else:
            new_cart_item = CartItem(CartID=cart.CartID, ProductID=product_id, Quantity=quantity)
            db.session.add(new_cart_item)
        
        product.Stock -= quantity
        db.session.commit()
        return jsonify({'success': f'{product.ProductName} added to cart'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add product to cart', 'details': str(e)}), 500

#Checkout Page
def checkout():
    cart_data = request.json['cart']
    total_amount = request.json['total']
    #Logic to handle order processing, payment, and inventory updates
    return jsonify({'status': 'Order processed succesfully', 'total': total_amount})

#Customer Profile Page
@app.route('/profile')
def profile():
    customer_id = 1
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Customers WHERE CustomerID = %s", (customer_id,))
    customer = cursor.fetchone()
    db.close()
    return render_template('profile.html', customer=customer)

#Running the app
if __name__ == '__main__':
    setup_database()
    app.run(debug=True)