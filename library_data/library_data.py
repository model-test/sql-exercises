import sqlite3

conn = sqlite3.connect("library.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS library(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    genre TEXT,
    author TEXT,
    pages INTEGER,
    year INTEGER,
    rating REAL
)
""")
conn.commit()

cursor.execute("DELETE from library")
conn.commit()

rows_to_insert = [
("The Silent Forest", "Fantasy", "A. Rivera", 420, 2018, 4.6),
("Numbers and Noise", "Science", "D. Kim", 310, 2020, 4.2),
("Hidden Cities", "Fantasy", "A. Rivera", 510, 2021, 4.8),
("The Last Algorithm", "Technology", "S. Patel", 275, 2017, 4.1),
("Quantum Drift", "Science", "D. Kim", 390, 2019, 4.5),
("Minimal Lines", "Technology", "R. Zhao", 150, 2022, 3.9),
("Echoes of Steel", "Fantasy", "M. Laurent", 610, 2015, 4.7),
("Data Horizons", "Science", "L. Thompson", 340, 2023, 4.4),
("Binary Dawn", "Technology", "S. Patel", 480, 2016, 4.3),
("Ancient Tides", "Fantasy", "M. Laurent", 530, 2014, 4.9),
]

cursor.executemany("""
INSERT INTO library (title, genre, author, pages, year, rating)
VALUES (?, ?, ?, ?, ?, ?)
""", rows_to_insert)
conn.commit()

cursor.execute("""
SELECT title, year
FROM library
ORDER BY year DESC
""")

ordered_books = cursor.fetchall()

print("Ordered by Year (Descending):")
for row in ordered_books:
    print(f"{row[0]} - {row[1]}")


cursor.execute("""
SELECT genre, COUNT(*) AS total_books
FROM library
GROUP BY genre
""")

total_genres = cursor.fetchall()

print("\nTotal Number of Books per Genre:")
for row in total_genres:
    print(f"{row[0]} - {row[1]}")


cursor.execute("""
SELECT genre, AVG(rating) as average_rating
FROM library
GROUP BY genre
""")

average_ratings = cursor.fetchall()

print("\nAverage Rating per Genre:")
for row in average_ratings:
    print(f"{row[0]} - {row[1]:.2f}")


cursor.execute("""
SELECT genre, AVG(rating) as average_rating
FROM library
GROUP BY genre
HAVING average_rating > 4.4
""")

high_average_ratings = cursor.fetchall()

print("\nGenres With Average Rating Greater Than 4.4:")
for row in high_average_ratings:
    print(f"{row[0]} - {row[1]:.2f}")


cursor.execute("""
SELECT title, pages
FROM library
ORDER BY pages DESC
LIMIT 3;
""")

longest_books = cursor.fetchall()

print("\nTop 3 Longest Books:")
for idx, row in enumerate(longest_books):
    print(f"{idx+1}. {row[0]} - {row[1]} pages")
