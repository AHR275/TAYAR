from flask import Flask, render_template
from src.middleware.config import CONFIG
from src.middleware.db import db 


from src.routes.topup import topup_bp
from src.routes.homepage import home_bp
# from src.routes.analyze import analyze_bp


app = Flask(__name__)
app.config.update(CONFIG)




@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

app.register_blueprint(topup_bp)

app.register_blueprint(home_bp)

# app.register_blueprint(analyze_bp)


if __name__ == "__main__":
    app.run(debug=True, port=5000)