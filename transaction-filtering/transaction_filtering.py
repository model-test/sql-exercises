import sqlite3


# Database connection
conn = sqlite3.connect("transactions.db")

# Cursor
cursor = conn.cursor()

cursor.execute("DELETE FROM transactions")
conn.commit()

# Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    date TEXT,
    category TEXT,
    amount REAL
)
""")

# Commit
conn.commit()

# Define multiple rows
rows_to_insert = [
    ("2026-01-01", "Transport", 8.75),
    ("2026-01-02", "Entertainment", 20.00),
    ("2026-01-03", "Bills", 120.00),
    ("2026-01-04", "Transport", 7.25),
    ("2026-01-05", "Food", 5.00)
]

# Insert all rows
cursor.executemany("""
INSERT INTO transactions (date, category, amount)
VALUES(?, ?, ?)
""", rows_to_insert)

# Commit
conn.commit()

# Filter data with SELECT
cursor.execute("""
SELECT
    category,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_spent
FROM transactions
WHERE amount > 5
GROUP BY category
HAVING SUM(amount) > 15
ORDER BY total_spent DESC
""")

rows = cursor.fetchall()

for row in rows:
    print(row)
