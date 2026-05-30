from flask import Flask, render_template
from src.routes.topup import topup_bp

app = Flask(__name__)
app.config['SECRET_KEY']= "LDKHGLJEIFNOWJ9403I4F"
@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

app.register_blueprint(topup_bp)


