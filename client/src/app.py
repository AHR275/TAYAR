from flask import Flask, render_template , redirect , url_for , request 
from src.middleware.config import CONFIG
from src.middleware.db import db 
from src.middleware.init_db import create_database, seed_db

from src.middleware.session_manager import SessionManager
from src.middleware.navbar import register_navbar


from src.routes.topup import topup_bp
from src.routes.homepage import home_bp
from src.routes.paymment import payment_bp
from src.routes.dashboard import dashboard_bp 
from src.routes.auth import auth_bp
from src.routes.admin import admin_bp
from src.routes.analyze_admin import analysis_admin_bp
from src.routes.analyze_user import analysis_user_bp
from src.routes.profile import profile_bp 

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

register_navbar(app)

app.register_blueprint(topup_bp)
app.register_blueprint(auth_bp)

app.register_blueprint(home_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(admin_bp)
# app.register_blueprint(analysis_admin_bp)
app.register_blueprint(analysis_user_bp)
app.register_blueprint(profile_bp)

@app.before_request  
def before_request() :
    user = SessionManager.get_user()
    

    ALLOWED_ENDPOINTS =["auth.register " , "auth.login" ,"homepage.homepage"]
    ADMIN_ENDPOINTS= ["admin.dashboard"  , "admin.analyze_admin"]
    

    if request.endpoint not in ALLOWED_ENDPOINTS: 
        if not user : 
            return redirect(url_for("auth.login")) 
        elif  user['is_admin']==False and request.endpoint in ADMIN_ENDPOINTS :
            return render_template("forbidden.html") 

