from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_FILE = "cleanomato.db"

# Initialize database
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                service TEXT NOT NULL,
                service_date TEXT NOT NULL,
                location TEXT NOT NULL
            )
        """)
        conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        service = request.form['service']
        service_date = request.form['service_date']
        location = request.form['location']

        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bookings (name, phone, email, service, service_date, location) 
                VALUES (?, ?, ?, ?, ?, ?)""", (name, phone, email, service, service_date, location))
            conn.commit()

        return render_template('success.html', name=name)

    return render_template('book.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
