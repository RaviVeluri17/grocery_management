import mysql.connector
from mysql.connector import Error
import os

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('MYSQL_HOST'),
            database=os.environ.get('MYSQL_DATABASE'),
            user=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD')
        )
        if connection.is_connected():
            print("Successfully connected to the database")
        else:
            print("Failed to connect to the database")
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
    return connection


def execute_query(query, params=None):
    """ Execute a single query (e.g., INSERT, UPDATE, DELETE) """
    connection = create_connection()
    if not connection:
        return None

    cursor = connection.cursor()
    try:
        cursor.execute(query, params or ())
        connection.commit()
        return cursor.lastrowid if 'insert' in query.lower() else True
    except Error as e:
        print(f"Error executing query: {e}")
        connection.rollback()
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def fetch_query(query, params=None):
    """ Fetch data from a query (e.g., SELECT) """
    connection = create_connection()
    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)
    result = None
    try:
        cursor.execute(query, params or ())
        result = cursor.fetchall()
    except Error as e:
        print(f"Error fetching data: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
    return result

def add_user(username, password, role):
    query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
    return execute_query(query, (username, password, role))

def get_user_by_username(username):
    query = "SELECT * FROM users WHERE username = %s"
    return fetch_query(query, (username,))

def add_product(name, price, quantity, category, stock_quantity):
    query = "INSERT INTO products (name, price, quantity, category, stock_quantity) VALUES (%s, %s, %s, %s, %s)"
    return execute_query(query, (name, price, quantity, category, stock_quantity))

def get_all_products():
    query = "SELECT * FROM products"
    return fetch_query(query)

def get_product_by_id(product_id):
    query = "SELECT * FROM products WHERE id = %s"
    return fetch_query(query, (product_id,))

def update_product_stock(product_id, new_stock_quantity):
    query = "UPDATE products SET stock_quantity = %s WHERE id = %s"
    return execute_query(query, (new_stock_quantity, product_id))

def record_sale(user_id, total):
    query = "INSERT INTO sales (user_id, total, date_time) VALUES (%s, %s, NOW())"
    return execute_query(query, (user_id, total))

def record_sale_item(sale_id, product_id, quantity, price):
    query = "INSERT INTO sale_items (sale_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)"
    return execute_query(query, (sale_id, product_id, quantity, price))

def update_product_details(product_id, name, price, quantity, category, stock_quantity):
    query = """
    UPDATE products
    SET name = %s, price = %s, quantity = %s, category = %s, stock_quantity = %s
    WHERE id = %s
    """
    params = (name, price, quantity, category, stock_quantity, product_id)
    return execute_query(query, params)