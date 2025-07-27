# Grocery Store Management System

A web-based application built with the Flask framework for managing a small grocery store's day-to-day operations. This system provides a simple and intuitive interface for key tasks, including inventory tracking, sales processing, and secure user management.

## Features

  * **User Authentication**: The application includes a secure login and registration system with distinct roles for admins and regular users.
  * **Product Management**: Admins have the ability to add new products, and update existing product details such as name, price, and stock quantity.
  * **Sales Dashboard**: A central dashboard displays all available products, allowing users to easily record sales by entering a quantity.
  * **Stock Tracking**: The system automatically adjusts product stock levels in the database after each sale to ensure accurate inventory counts.
  * **Database Management**: All application data, including users, products, and sales, is stored and managed using a MySQL database.
  * **Reporting**: A dedicated section for admins is included to view reports (currently a placeholder, but ready for future development).

## Technologies Used

This project leverages the following technologies and Python libraries:

  * **Backend Framework**: [Flask](https://flask.palletsprojects.com/)
  * **Database**: [MySQL](https://www.mysql.com/)
  * **Database Connector**: The `mysql-connector-python` and `mysqlclient` libraries are used to connect Flask to the MySQL database.
  * **Security**: Password hashing is handled securely using `werkzeug.security`.
  * [cite\_start]**Forms**: `Flask-WTF` is used to handle web forms[cite: 1].
  * [cite\_start]**Login Management**: `Flask-Login` provides user session management[cite: 1].
  * **Frontend**: The user interface is built using standard HTML and CSS, with a layout suitable for Bootstrap.

## Getting Started

Follow these steps to set up and run the project on your local machine.

### Prerequisites

  * Python 3.7 or higher
  * MySQL Server installed and running

### 1\. Clone the repository

First, clone your project's Git repository to your local machine and navigate into the project directory.

```bash
git clone <your-repo-url>
cd GroceryStoreManagementSystem
```

### 2\. Set up the virtual environment

It's a best practice to use a virtual environment to manage your project dependencies and avoid conflicts with other projects.

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3\. Install dependencies

With your virtual environment active, install all the required Python libraries listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4\. Database Setup

The application uses a MySQL database named `grocery_db`. You will need to create this database and the necessary tables.

1.  Connect to your MySQL server (e.g., using the command `mysql -u root -p`).
2.  Create the database:
    ```sql
    CREATE DATABASE grocery_db;
    USE grocery_db;
    ```
3.  Create the following tables: `users`, `products`, `sales`, and `sale_items`. Your `database.py` file contains the functions to interact with these tables, but you will need to write the `CREATE TABLE` statements yourself to define the schema.

### 5\. Configuration

For security, the application's configuration is managed through environment variables. You will need to set these on your system or in a `.env` file.

  * `SECRET_KEY`: A secret key for Flask sessions.
  * `MYSQL_HOST`: The hostname of your MySQL server (e.g., `localhost`).
  * `MYSQL_DATABASE`: The name of your database (`grocery_db`).
  * `MYSQL_USER`: Your MySQL username (e.g., `root`).
  * `MYSQL_PASSWORD`: Your MySQL password.

### 6\. Run the Application

Once everything is set up, you can start the Flask development server from your project directory.

```bash
flask run
```

The application will be accessible at `http://127.0.0.1:5000`. You can then navigate to `/register` to create a user account and begin using the system.