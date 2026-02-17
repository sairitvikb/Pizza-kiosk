from flask import Flask, render_template, request, redirect, url_for, session, g
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database configuration
db_config = {
    'user': 'root',         # your MySQL username
    'password': 'Mailp@ssw0rd',   # your MySQL password
    'host': 'localhost',    # your MySQL host, usually localhost
    'database': 'pizza_app_db'  # the name of your database
}

def get_db():
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(**db_config)
        except Error as e:
            print(f"Error: {e}")
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('menu'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/menu')
def menu():
    cursor = get_db().cursor()
    cursor.execute('SELECT * FROM pizzas')
    pizzas = cursor.fetchall()
    cursor.close()
    return render_template('menu.html', pizzas=pizzas)

@app.route('/order', methods=['POST'])
def order():
    user_id = session.get('user_id')
    pizza_id = request.form['pizza_id']
    quantity = request.form['quantity']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO orders (user_id, pizza_id, quantity) VALUES (%s, %s, %s)', (user_id, pizza_id, quantity))
    db.commit()
    cursor.close()
    return render_template('order_success.html')

@app.route('/orders')
def orders():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))  # Redirect to login if user is not authenticated
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT o.id, p.name, p.size, o.quantity
        FROM orders o
        JOIN pizzas p ON o.pizza_id = p.id
        WHERE o.user_id = %s
    ''', (user_id,))
    orders = cursor.fetchall()
    cursor.close()
    
    return render_template('orders.html', orders=orders)


if __name__ == '__main__':
    app.run(debug=True)
