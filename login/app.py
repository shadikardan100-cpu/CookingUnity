from flask import Flask, render_template, request, redirect, session
import json, os

app = Flask(__name__)
app.secret_key = "supersecret"  # needed for sessions

# --- Load users from file ---
def load_users():
    if not os.path.exists("users.json"):
        return {}
    with open("users.json", "r") as f:
        return json.load(f)

# --- Save users to file ---
def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

@app.route("/")
def home():
    if "username" in session:
        return render_template("home.html", name=session["username"])
    return redirect("/login")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        users = load_users()

        if name in users:
            return "User already exists. Try logging in."

        users[name] = password
        save_users(users)

        return redirect("/login")

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        users = load_users()

        if name not in users:
            return "User not found. Please sign up first."

        if users[name] != password:
            return "Wrong password."

        session["username"] = name
        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
