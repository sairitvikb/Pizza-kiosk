import mysql.connector
import pandas as pd

# Load the CSV data
file_path = 'E:/Project/New folder/pizza_app/pizza_menu.csv'
pizza_data = pd.read_csv(file_path)

# Connect to the MySQL database
db_config = {
    'user': 'root',         # your MySQL username
    'password': 'Mailp@ssw0rd',   # your MySQL password
    'host': 'localhost',    # your MySQL host, usually localhost
    'database': 'pizza_app_db'  # the name of your database
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Clear existing pizza data
cursor.execute('DELETE FROM pizzas')

# Insert new data
for index, row in pizza_data.iterrows():
    cursor.execute('INSERT INTO pizzas (name, size, price, ingredients, category) VALUES (%s, %s, %s, %s, %s)',
                   (row['pizza_name'], row['pizza_size'], row['unit_price'], row['pizza_ingredients'], row['pizza_category']))

# Commit and close the connection
conn.commit()
cursor.close()
conn.close()
