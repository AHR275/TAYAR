from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to TAYAR Electricity System"


@app.route("/login")
def login():
    return "Login Page"


@app.route("/register")
def register():
    return "Register Page"


@app.route("/dashboard")
def dashboard():
    return "User Dashboard"


@app.route("/admin")
def admin():
    return "Admin Dashboard"


@app.route("/recharge")
def recharge():
    return "Recharge Page"


if __name__ == "__main__":
    app.run(debug=True)