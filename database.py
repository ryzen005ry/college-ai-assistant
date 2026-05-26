import sqlite3

def init_db():
    conn = sqlite3.connect('college.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, marks INTEGER, group_12th TEXT, interests TEXT)''')
    conn.commit()
    conn.close()

def add_student(name, marks, group_12th, interests):
    conn = sqlite3.connect('college.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (name, marks, group_12th, interests) VALUES (?, ?, ?, ?)", (name, marks, group_12th, interests))
    conn.commit()
    conn.close()

def get_all_students():
    conn = sqlite3.connect('college.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    data = c.fetchall()
    conn.close()
    return data
