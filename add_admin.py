import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

password = generate_password_hash("admin123")

cursor.execute("INSERT INTO admin (email, password) VALUES (?, ?)",
               ("admin@gmail.com", password))

conn.commit()
conn.close()

print("Admin added!")