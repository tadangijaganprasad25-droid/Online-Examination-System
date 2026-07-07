from flask import Flask, render_template, request, redirect, session
import sqlite3, datetime, os

app = Flask(__name__)
app.secret_key = 'secret'

# Absolute path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'exam.db')

# 🔥 FORCE DB + TABLE CREATION
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        password TEXT
    )
    """)

    # Create results table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        score INTEGER,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()

# Call once at startup
init_db()

def get_db():
    return sqlite3.connect(DB_PATH)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        db = get_db()
        db.execute(
            "INSERT INTO users(username,email,password) VALUES(?,?,?)",
            (request.form['username'], request.form['email'], request.form['password'])
        )
        db.commit()
        db.close()
        return redirect('/')
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (request.form['username'], request.form['password'])
    ).fetchone()
    db.close()

    if user:
        session['user'] = user[0]
        return redirect('/test')
    return "Invalid login"

@app.route('/test')
def test():
    if 'user' not in session:
        return redirect('/')
    return render_template('test.html')

@app.route('/submit', methods=['POST'])
def submit():
    if 'user' not in session:
        return redirect('/')

    score = int(request.form['score'])

    db = get_db()
    db.execute(
        "INSERT INTO results(user_id,score,time) VALUES(?,?,?)",
        (session['user'], score, str(datetime.datetime.now()))
    )
    db.commit()
    db.close()

    return render_template('result.html', score=score)

@app.route('/logout')
def logout():
    session.clear()   # removes all session data
    return redirect('/')
    
if __name__ == "__main__":
    print("DEBUG PATH:", DB_PATH, flush=True)
    app.run(debug=True, use_reloader=False)