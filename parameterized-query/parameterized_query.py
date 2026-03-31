import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS users")

cursor.execute("""
CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    city TEXT
)
""")

users_data = [
    ("Alice", 25, "Miami"),
    ("Bob", 30, "New York"),
    ("Charlie", 22, "Los Angeles"),
    ("Diana", 40, "Chicago"),
    ("Eve", 28, "Miami"),
    ("Frank", 35, "Houston"),
    ("Grace", 19, "New York"),
    ("Hannah", 31, "Miami"),
    ("Ian", 27, "Chicago"),
    ("Jack", 45, "Houston"),
    ("Karen", 33, "Los Angeles"),
    ("Leo", 21, "Miami"),
    ("Maya", 29, "Chicago"),
    ("Nina", 38, "New York"),
    ("Oscar", 26, "Houston")
]

cursor.executemany("""
INSERT INTO users (name, age, city)
VALUES (?, ?, ?)
""", users_data)
conn.commit()

cursor.execute("SELECT * FROM users WHERE age > ?", (25,))

print("Users Older Than 25:")
for row in cursor.fetchall():
    print(f"Name: {row[1]}\nAge: {row[2]}\nCity: {row[3]}\n")

cursor.execute("SELECT * FROM users WHERE age > ? AND city = ?", (25, "Miami"))

print("Users Older Than 25 and in Miami:")
for row in cursor.fetchall():
    print(f"Name: {row[1]}\nAge: {row[2]}\nCity: {row[3]}\n")

cursor.execute("SELECT * FROM users WHERE age > ? ORDER BY age DESC", (20,))

print("Users Older Than 20 Sorted by Age Desc:")
for row in cursor.fetchall():
    print(f"Name: {row[1]}\nAge: {row[2]}\nCity: {row[3]}\n")

cursor.execute("SELECT COUNT(*) FROM users WHERE age > ?", (25,))

print("How Many Users are Older Than 25?:")
print(cursor.fetchone()[0])

cursor.execute("""
SELECT city, COUNT(id)
FROM users
GROUP BY city
ORDER BY COUNT(id) DESC
""")

print("\nHow Many Users are in Each City?:")
for row in cursor.fetchall():
    print(f"{row[0]} - {row[1]}")
