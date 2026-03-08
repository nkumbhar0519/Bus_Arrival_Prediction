from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import joblib

app = Flask(__name__)
app.secret_key = "bus_secret_key"

# Load trained ML model
model = joblib.load("bus_model.pkl")

# CREATE DATABASE TABLE

def create_routes_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS routes (
        route_id INTEGER,
        bus_number TEXT,
        stops TEXT,
        start_time TEXT,
        end_time TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

create_routes_table()


# ---------------- LOGIN PAGE ----------------
@app.route("/", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute("SELECT password FROM users WHERE username=?", (username,))
        user = c.fetchone()

        # USER EXISTS
        if user:
            if user[0] == password:
                session["user"] = username
                conn.close()
                return redirect(url_for("dashboard"))
            else:
                error = "Wrong password"

        # NEW USER (AUTO REGISTER)
        else:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            session["user"] = username

            conn.close()
            return redirect(url_for("dashboard"))

        conn.close()

    return render_template("login.html", error=error)


# ---------------- DASHBOARD ----------------
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    result = None

    if request.method == "POST":

        route = int(request.form["route"])
        stop = int(request.form["stop"])
        hour = int(request.form["hour"])
        day = int(request.form["day"])
        traffic = int(request.form["traffic"])

        prediction = model.predict([[route, stop, hour, day,traffic]])
        result = round(prediction[0], 2)

    return render_template("index.html", result=result)


# ---------------- ROUTES PAGE ----------------
@app.route("/routes")
def routes():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("routes.html")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.pop("user", None)
    return redirect(url_for("login"))


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)

def create_routes_table():

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS routes (
        route_id INTEGER,
        bus_number TEXT,
        stops TEXT,
        start_time TEXT,
        end_time TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


create_routes_table()   # call AFTER defining


def insert_routes():

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    routes = [
        (101,"KA-01-AB-1234","Station → Market → College → Hospital","06:00 AM","10:00 PM","On Time"),
        (102,"KA-02-CD-5678","Depot → Mall → IT Park → Airport","05:30 AM","11:00 PM","Delayed"),
        (103,"KA-03-EF-9012","City Center → Bus Stand → University","07:00 AM","09:30 PM","On Time")
    ]

    c.executemany("INSERT INTO routes VALUES (?,?,?,?,?,?)", routes)

    conn.commit()
    conn.close()
    insert_routes()