import sqlite3

conn = sqlite3.connect("orders.db")

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS orders")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer TEXT,
    product TEXT,
    category TEXT,
    quantity INTEGER,
    price REAL,
    order_year INTEGER
)
""")
conn.commit()

rows_to_insert = [
("Alice", "Laptop", "Electronics", 1, 1200.00, 2023),
("Bob", "Headphones", "Electronics", 2, 150.00, 2023),
("Alice", "Desk Chair", "Furniture", 1, 320.00, 2022),
("Clara", "Monitor", "Electronics", 2, 300.00, 2023),
("David", "Notebook", "Stationery", 5, 8.00, 2022),
("Eve", "Desk", "Furniture", 1, 550.00, 2023),
("Bob", "Pen Pack", "Stationery", 3, 5.00, 2023),
("Clara", "Keyboard", "Electronics", 1, 120.00, 2022),
("Alice", "Lamp", "Furniture", 2, 45.00, 2023),
("David", "Tablet", "Electronics", 1, 600.00, 2022)
]

cursor.executemany("""
INSERT INTO orders (customer, product, category, quantity, price, order_year)
VALUES(?, ?, ?, ?, ?, ?)
""", rows_to_insert)
conn.commit()

cursor.execute("""
SELECT customer, product, category, quantity, price, order_year
FROM orders
ORDER BY order_year DESC
""")

sorted_orders = cursor.fetchall()

print("Orders Sorted by Year (descending):")
for row in sorted_orders:
    print(f"Customer: {row[0]}\n| Product: {row[1]}\n| Category: {row[2]}\n| Quantity: {row[3]}\n| Price: ${row[4]}\n| Order Year: {row[5]}\n")


cursor.execute("""
SELECT category, SUM(quantity * price) as total_revenue
FROM orders
WHERE quantity > 0
GROUP BY category
""")

total_revenue = cursor.fetchall()

print("Total Revenue per Category:")
for row in total_revenue:
    print(f"{row[0]} - ${row[1]}")


cursor.execute("""
SELECT customer, SUM(quantity * price) as total_spending
FROM orders
GROUP BY customer
ORDER BY total_spending DESC
LIMIT 2;
""")

highest_spenders = cursor.fetchall()

print("\nTop 2 Customers by Total Spending:")
for idx, row in enumerate(highest_spenders):
    print(f"{idx+1}. {row[0]} - ${row[1]}")


cursor.execute("""
SELECT category, SUM(quantity * price) AS total_revenue
FROM orders
GROUP BY category
HAVING total_revenue > 1000
""")

large_total_revenues = cursor.fetchall()

print("\nCategories Where Total Revenue is Greater Than $1000:")
for row in large_total_revenues:
    print(f"{row[0]} - ${row[1]}")


cursor.execute("""
SELECT order_year, AVG(quantity * price) AS average_value
FROM orders
GROUP BY order_year
ORDER BY order_year DESC
""")

average_order_value = cursor.fetchall()

print("\nAverage Order Value per Year:")
for row in average_order_value:
    print(f"{row[0]} - ${row[1]:.2f}")

cursor.execute("""
SELECT COUNT(*)
FROM orders
""")

row_count = cursor.fetchone()

print("\nRow Count:")
print(row_count[0])

cursor.execute("""
SELECT COUNT(DISTINCT customer)
FROM orders
""")

customer_count = cursor.fetchone()

print("\nCustomer Count:")
print(customer_count[0])

cursor.execute("""
SELECT MAX(price)
FROM orders
""")

max_price = cursor.fetchone()

print("\nMax Price:")
print(f"${max_price[0]}")


cursor.execute("""
SELECT MIN(price)
FROM orders
""")

min_price = cursor.fetchone()

print("\nMin Price:")
print(f"${min_price[0]}")


cursor.execute("""
SELECT AVG(price)
FROM orders
""")

avg_price = cursor.fetchone()

print("\nAverage Price:")
print(f"${avg_price[0]}")
