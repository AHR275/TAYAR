from flask import Flask, render_template
from src.routes.topup import topup_bp
from src.routes.homepage import home_bp


app = Flask(__name__)
app.config['SECRET_KEY']= "LDKHGLJEIFNOWJ9403I4F"


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

app.register_blueprint(topup_bp)
app.register_blueprint(home_bp)


