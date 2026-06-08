from flask import Flask, render_template
from src.middleware.config import CONFIG
from src.middleware.db import db , create_database



from src.routes.topup import topup_bp
<<<<<<< HEAD
from src.routes.auth import auth_bp
=======
from src.routes.homepage import home_bp
from src.routes.paymment import payment_bp
from src.routes.dashboard import dashboard_bp 
# from src.routes.analyze import analyze_bp

>>>>>>> ahmed

app = Flask(__name__)
app.config.update(CONFIG)


create_database()
db.init_app(app)

with app.app_context():
    import src.models   # Import all models once

    db.create_all()




# @app.route("/dashboard")
# def dashboard():
#     return render_template("dashboard.html")

app.register_blueprint(topup_bp)
app.register_blueprint(auth_bp)

app.register_blueprint(home_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(dashboard_bp)

# app.register_blueprint(analyze_bp)


if __name__ == "__main__":
    app.run(debug=True, port=5000)