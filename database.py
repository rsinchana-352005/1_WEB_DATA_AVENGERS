import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# ---------------- ADMIN TABLE ---------------- #
cursor.execute('''
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
''')

# ---------------- STUDENT TABLE ---------------- #
cursor.execute('''
CREATE TABLE IF NOT EXISTS student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    usn TEXT UNIQUE,
    department TEXT,
    semester INTEGER,
    password TEXT
)
''')

# ---------------- FACULTY TABLE ---------------- #
cursor.execute('''
CREATE TABLE IF NOT EXISTS faculty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    department TEXT,
    password TEXT
)
''')


# ---------------- FACULTY ASSIGNMENT TABLE ---------------- #
cursor.execute('''
CREATE TABLE IF NOT EXISTS faculty_assignment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty_name TEXT,
    subject_code TEXT
)
''')

# ---------------- MARKS TABLE ---------------- #
cursor.execute('''
CREATE TABLE IF NOT EXISTS marks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usn TEXT,
    subject_code TEXT,
    ia1 INTEGER,
    ia2 INTEGER,
    ia3 INTEGER,
    attendance INTEGER
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usn TEXT,
    subject_code TEXT,
    credits INTEGER,
    ia_total INTEGER,
    see_marks INTEGER,
    total REAL,
    grade TEXT,
    grade_point INTEGER
)
''')
conn.commit()
conn.close()

print("✅ Final Database Created Successfully!")