import sqlite3
def create_db():
    con=sqlite3.connect(database="ims.db")
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,dob text,doj text,pass text,utype text,address text,salary text)")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS monthly(eid INTEGER PRIMARY KEY AUTOINCREMENT,dop text, month text, item text, remaining amount text, given amount text, total amount text, description text)")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS office(eid INTEGER PRIMARY KEY AUTOINCREMENT,date text, item text, expense text, description text)")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS store(eid INTEGER PRIMARY KEY AUTOINCREMENT,asset text, qnt text, description text)")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS leave(eid INTEGER PRIMARY KEY AUTOINCREMENT,emp text, total text,taken text,remaining text, description text)")
    con.commit()
    
create_db()
