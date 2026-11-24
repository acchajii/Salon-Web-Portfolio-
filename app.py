import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-secret-before-deployment")

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "4000"))
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

def get_connection():
    if all([MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE]):
        import pymysql
        return pymysql.connect(
            host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER,
            password=MYSQL_PASSWORD, database=MYSQL_DATABASE,
            cursorclass=pymysql.cursors.DictCursor,
            ssl={"ssl": {}}, connect_timeout=10
        )
    import sqlite3
    conn = sqlite3.connect("velora.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    mysql_mode = bool(MYSQL_HOST and MYSQL_USER and MYSQL_PASSWORD and MYSQL_DATABASE)
    cur = conn.cursor()
    if mysql_mode:
        cur.execute("""CREATE TABLE IF NOT EXISTS appointments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(120) NOT NULL,
            phone VARCHAR(30) NOT NULL,
            service VARCHAR(100) NOT NULL,
            preferred_date DATE NOT NULL,
            message TEXT,
            status VARCHAR(30) DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
    else:
        cur.execute("""CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL, phone TEXT NOT NULL,
            service TEXT NOT NULL, preferred_date TEXT NOT NULL,
            message TEXT, status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/book", methods=["POST"])
def book():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    service = request.form.get("service", "").strip()
    date = request.form.get("date", "").strip()
    message = request.form.get("message", "").strip()
    if not all([name, phone, service, date]):
        flash("Please complete all required fields.", "error")
        return redirect(url_for("home") + "#booking")
    try:
        datetime.strptime(date, "%Y-%m-%d")
        conn = get_connection()
        cur = conn.cursor()
        mysql_mode = bool(MYSQL_HOST and MYSQL_USER and MYSQL_PASSWORD and MYSQL_DATABASE)
        placeholder = "%s" if mysql_mode else "?"
        cur.execute(
            f"INSERT INTO appointments (customer_name, phone, service, preferred_date, message) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})",
            (name, phone, service, date, message)
        )
        conn.commit()
        cur.close()
        conn.close()
        flash("Your appointment request has been received. Our team will contact you to confirm.", "success")
    except Exception:
        flash("We couldn't submit your request right now. Please try again or contact the salon.", "error")
    return redirect(url_for("home") + "#booking")

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

@app.route("/admin")
def admin():
    # Demo admin page: protect this route before using the site for a real business.
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM appointments ORDER BY created_at DESC")
        appointments = cur.fetchall()
        cur.close()
        conn.close()
    except Exception:
        appointments = []
        flash("Database is not connected yet. Configure the database settings.", "error")
    return render_template("admin.html", appointments=appointments)

@app.route("/admin/status/<int:appointment_id>", methods=["POST"])
def update_status(appointment_id):
    status = request.form.get("status", "Pending")
    if status not in ["Pending", "Confirmed", "Completed", "Cancelled"]:
        flash("Invalid status.", "error")
        return redirect(url_for("admin"))
    try:
        conn = get_connection()
        cur = conn.cursor()
        mysql_mode = bool(MYSQL_HOST and MYSQL_USER and MYSQL_PASSWORD and MYSQL_DATABASE)
        placeholder = "%s" if mysql_mode else "?"
        cur.execute(f"UPDATE appointments SET status={placeholder} WHERE id={placeholder}", (status, appointment_id))
        conn.commit()
        cur.close()
        conn.close()
        flash("Appointment status updated.", "success")
    except Exception:
        flash("Could not update appointment status.", "error")
    return redirect(url_for("admin"))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
