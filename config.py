import os

# Use environment variables for sensitive information
SECRET_KEY = os.environ.get('SECRET_KEY', 'useraccount')
ADMIN_SECRET_KEY = os.environ.get('ADMIN_SECRET_KEY', 'adminaccount')

# Database configuration
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'grocery_db')
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '22FE1A04F1')