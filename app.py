from flask import Flask
from flask import request
import sqlite3

app = Flask(__name__)

# ======================
# CREATE DATABASE
# ======================
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
    """)

    # insert default user
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', '1234')")

    conn.commit()
    conn.close()


# ======================
# HOME PAGE
# ======================
@app.route("/")
def home():
    return "Welcome to DevSecOps Project"


# ======================
# LOGIN (VULNERABLE)
# ======================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # ❌ VERY BAD PRACTICE (SQL Injection vulnerability)
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)

        user = cursor.fetchone()

        conn.close()

        if user:
            return "Login successful"
        else:
            return "Invalid credentials"

    else:
        return """
        <h2>Login Page</h2>
        <form method="post">
            Username: <input type="text" name="username"><br><br>
            Password: <input type="password" name="password"><br><br>
            <input type="submit" value="Login">
        </form>
        """


# ======================
# RUN APP
# ======================
if __name__ == "__main__":
    init_db()
    app.run(debug=True)