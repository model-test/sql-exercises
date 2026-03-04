import sqlite3

conn = sqlite3.connect("left_join_project.db")

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS customers")
cursor.execute("DROP TABLE IF EXISTS orders")
conn.commit()


cursor.execute("""
CREATE TABLE customers(
    id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT,
    signup_year INTEGER
)
""")

cursor.execute("""
CREATE TABLE orders(
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product TEXT,
    category TEXT,
    total REAL,
    order_year INTEGER
)
""")

customer_data = [
    (1, "Alice", "Miami", 2020),
    (2, "Bob", "Orlando", 2019),
    (3, "Clara", "Tampa", 2021),
    (4, "David", "Miami", 2018),
    (5, "Eva", "Orlando", 2022)
]
order_data = [
    (1, 1, "Laptop", "Electronics", 1200, 2023),
    (2, 1, "Mouse", "Electronics", 25, 2023),
    (3, 2, "Desk", "Furniture", 550, 2022),
    (4, 3, "Monitor", "Electronics", 300, 2023),
    (5, 3, "Keyboard", "Electronics", 120, 2022),
    (6, 3, "Chair", "Furniture", 200, 2023),
]

cursor.executemany("""
INSERT INTO customers (id, name, city, signup_year)
VALUES(?, ?, ?, ?)
""", customer_data)

cursor.executemany("""
INSERT INTO orders (id, customer_id, product, category, total, order_year)
VALUES(?, ?, ?, ?, ?, ?)
""", order_data)
conn.commit()

cursor.execute("""
SELECT 
    customers.name, 
    customers.city, 
    COALESCE(orders.product, 'NO ORDER') AS product, 
    COALESCE(orders.total, 0) AS total
FROM customers
LEFT JOIN orders
ON customers.id = orders.customer_id
ORDER BY customers.name ASC, total DESC
""")

customer_orders = cursor.fetchall()

print("All Customer Order Histories:")
for row in customer_orders:
    print(f"{row[0]}\n| City: {row[1]}\n| Product: {row[2]}\n| Total: ${row[3]:.2f}\n")


cursor.execute("""
SELECT customers.name, customers.city, orders.product
FROM customers
LEFT JOIN orders
ON customers.id = orders.customer_id
WHERE orders.id IS NULL
ORDER BY customers.name ASC 
""")

null_orders = cursor.fetchall()

print("Customers With No Orders:")
for row in null_orders:
    print(f"{row[0]}\n| City: {row[1]}\n")


cursor.execute("""
SELECT customers.name, COUNT(orders.id) AS order_count
FROM customers
LEFT JOIN orders
ON customers.id = orders.customer_id
GROUP BY name, customers.id
ORDER BY order_count DESC
""")

order_count = cursor.fetchall()

print("Number of Orders per Customer:")
for row in order_count:
    print(f"{row[0]} - {row[1]} order(s)")


cursor.execute("""
SELECT customers.name, SUM(COALESCE(orders.total, 0)) AS total_spent
FROM customers
LEFT JOIN orders
ON customers.id = orders.customer_id
GROUP BY name, customers.id
ORDER BY total_spent DESC
""")

total_spent = cursor.fetchall()

print("\nTotal Amount Spent per Customer:")
for row in total_spent:
    print(f"{row[0]} - ${row[1]:.2f}")


cursor.execute("""
SELECT customers.name, MAX(COALESCE(orders.order_year, "NO ORDERS"))
FROM customers
LEFT JOIN orders
ON customers.id = orders.customer_id
GROUP BY name
""")

latest_order_year = cursor.fetchall()

print(f"\nMost Recent Order Year per Customer:")
for row in latest_order_year:
    print(f"{row[0]} - {row[1]}")


cursor.execute("""
SELECT customers.name, SUM(COALESCE(orders.total, 0)) AS total_spent
FROM customers
LEFT JOIN orders
ON customers.id = orders.customer_id
GROUP BY name
ORDER BY total_spent DESC
LIMIT 3;
""")

top_customers = cursor.fetchall()

print("\nTop 3 Customers by Total Spending:")
for idx, row in enumerate(top_customers):
    print(f"{idx+1}. {row[0]} - ${row[1]:.2f}")


cursor.execute("""
SELECT customers.city, COALESCE(SUM(orders.total), 0) AS total_spent
FROM customers
LEFT JOIN orders
ON customers.id = orders.customer_id
GROUP BY city
""")

total_city_spending = cursor.fetchall()

print("\nTotal Revenue per City:")
for row in total_city_spending:
    print(f"{row[0]} - ${row[1]:.2f}")


cursor.execute("""
SELECT customers.name, customers.signup_year
FROM customers
LEFT JOIN orders
ON customers.id = orders.customer_id
WHERE orders.id IS NULL
    AND customers.signup_year < 2021
ORDER BY customers.signup_year, customers.name;
""")

signed_customers = cursor.fetchall()

print(f"\nCustomers Who Signed Up Before 2021 but Never Placed an Order:")
for row in signed_customers:
    print(f"{row[0]} - {row[1]}")


cursor.execute("""
SELECT orders.category, COUNT(orders.product) AS product_count
FROM orders
GROUP BY category
ORDER BY product_count DESC
LIMIT 1;
""")

popular_product = cursor.fetchall()

print(f"\nMost Popular Category:")
for row in popular_product:
    print(f"{row[0]} - {row[1]} order(s)")
