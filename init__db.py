import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()

# User Table
cur.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
""")

# Notes Table
cur.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,    
        username TEXT NOT NULL,
        content TEXT NOT NULL
    )
""")

con.commit()
con.close()
print("Database initialized successfully!")
