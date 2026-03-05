from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sirisha@1237",
    database="slot_booking_db"
)

@app.route('/')
def home():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM slots")
    slots = cursor.fetchall()
    return render_template('index.html', slots=slots)

@app.route('/book/<int:id>', methods=['POST'])
def book_slot(id):
    name = request.form['name']
    cursor = db.cursor()
    cursor.execute("SELECT status FROM slots WHERE id=%s", (id,))
    result = cursor.fetchone()

    if result and result[0] == "Available":
        cursor.execute(
            "UPDATE slots SET status='Booked', booked_by=%s WHERE id=%s",
            (name, id)
        )
        db.commit()

    return redirect('/')

@app.route('/booked')
def booked_slots():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM slots WHERE status='Booked'")
    booked = cursor.fetchall()
    return render_template('booked.html', booked=booked)

if __name__ == '__main__':
    app.run(debug=True)