from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import functools
import datetime
from dotenv import load_dotenv
from config import SECRET_KEY, ADMIN_SECRET_KEY

# Import all necessary database functions
from database import (
    add_user,
    get_user_by_username,
    add_product,
    get_all_products,
    get_product_by_id,
    update_product_stock,
    record_sale,
    record_sale_item,
    update_product_details
)

load_dotenv() # Load environment variables from a .env file

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Context processor to inject current year into all templates
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.datetime.now().year}

# Decorator to check if user is logged in
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

# Decorator to check if user is an admin
def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'role' not in session or session['role'] != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('dashboard'))
        return view(**kwargs)
    return wrapped_view

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_records = get_user_by_username(username)

        if user_records:
            user = user_records[0]
            if check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                flash('Logged in successfully!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.', 'danger')
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        admin_key = request.form.get('admin_key')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        if get_user_by_username(username):
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html')

        # Determine user role based on the admin key
        if admin_key and admin_key == ADMIN_SECRET_KEY:
            role = 'admin'
        else:
            role = 'user'

        hashed_password = generate_password_hash(password)
        success_id = add_user(username, hashed_password, role)

        if success_id:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed due to a database error. Please try again.', 'danger')
            return render_template('register.html')
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    products = get_all_products()
    return render_template('dashboard.html', products=products)

@app.route('/sell', methods=['POST'])
@login_required
def sell_product():
    product_id = request.form.get('product_id', type=int)
    quantity_to_sell = request.form.get('quantity', type=int)

    product_records = get_product_by_id(product_id)
    if not product_records:
        flash('Product not found.', 'danger')
        return redirect(url_for('dashboard'))

    product = product_records[0]

    if quantity_to_sell is None or quantity_to_sell <= 0:
        flash('Quantity to sell must be a positive number.', 'danger')
        return redirect(url_for('dashboard'))

    if product['stock_quantity'] < quantity_to_sell:
        flash(f"Not enough stock for {product['name']}. Available: {product['stock_quantity']}", 'danger')
        return redirect(url_for('dashboard'))

    new_stock = product['stock_quantity'] - quantity_to_sell
    update_product_stock(product_id, new_stock)

    total_price = product['price'] * quantity_to_sell
    sale_id = record_sale(session['user_id'], total_price)

    if sale_id:
        record_sale_item(sale_id, product_id, quantity_to_sell, product['price'])
        flash(f"Sold {quantity_to_sell} units of {product['name']}.", 'success')
    else:
        flash('Error recording sale. Please try again.', 'danger')

    return redirect(url_for('dashboard'))

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
@admin_required
def add_new_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        category = request.form['category']
        stock_quantity = request.form['stock_quantity']

        if not all([name, price, quantity, category, stock_quantity]):
            flash('All fields are required.', 'danger')
            return render_template('add_product.html')
        try:
            price = float(price)
            quantity = int(quantity)
            stock_quantity = int(stock_quantity)
        except ValueError:
            flash('Price, Quantity, and Stock Quantity must be numbers.', 'danger')
            return render_template('add_product.html')

        success = add_product(name, price, quantity, category, stock_quantity)
        if success:
            flash(f'Product "{name}" added successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Failed to add product due to a database error.', 'danger')
            return render_template('add_product.html')

    return render_template('add_product.html')

@app.route('/edit_product/<int:product_id>', methods=['GET'])
@login_required
@admin_required
def edit_product(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash('Product not found!', 'danger')
        return redirect(url_for('dashboard'))
    return render_template('edit_product.html', product=product[0])

@app.route('/update_product/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def update_product(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash('Product not found!', 'danger')
        return redirect(url_for('dashboard'))

    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    category = request.form['category']
    stock_quantity = request.form['stock_quantity']

    if not all([name, price, quantity, category, stock_quantity]):
        flash('All fields are required.', 'danger')
        return redirect(url_for('edit_product', product_id=product_id))

    try:
        price = float(price)
        stock_quantity = int(stock_quantity)
    except ValueError:
        flash('Price and Stock Quantity must be valid numbers.', 'danger')
        return redirect(url_for('edit_product', product_id=product_id))

    success = update_product_details(product_id, name, price, quantity, category, stock_quantity)

    if success:
        flash(f'Product "{name}" updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Failed to update product due to a database error.', 'danger')
        return redirect(url_for('edit_product', product_id=product_id))

@app.route('/reports')
@login_required
@admin_required
def reports():
    return render_template('reports.html')

# if __name__ == '__main__':
#     app.run(debug=True)