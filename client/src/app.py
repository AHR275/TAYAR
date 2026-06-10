from flask import Flask, render_template
from src.middleware.config import CONFIG
from src.middleware.db import db 
from src.middleware.init_db import create_database, seed_db



from src.routes.topup import topup_bp
from src.routes.homepage import home_bp
from src.routes.paymment import payment_bp
from src.routes.dashboard import dashboard_bp 
from src.routes.auth import auth_bp
from src.routes.admin import admin_bp
# from src.routes.analyze import analyze_bp


app = Flask(__name__)
app.config.update(CONFIG)


# create_database()
db.init_app(app)

with app.app_context():
    import src.models   # Import all models once

    db.create_all()
    seed_db()




# @app.route("/dashboard")
# def dashboard():
#     return render_template("dashboard.html")

app.register_blueprint(topup_bp)
app.register_blueprint(auth_bp)

app.register_blueprint(home_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(admin_bp)

# app.register_blueprint(analyze_bp)


if __name__ == "__main__":
    app.run(debug=True, port=5000)