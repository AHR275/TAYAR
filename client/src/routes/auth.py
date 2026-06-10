from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    session
)
from flask.views import MethodView
from werkzeug.security import check_password_hash

from src.forms.auth_forms import (
    LoginForm,
    RegisterForm,
    ForgotPasswordForm
)

from src.models import User, Room


auth_bp = Blueprint("auth", __name__)

class LoginView(MethodView):

    def get(self):
        form = LoginForm()
        return render_template("login.html", form=form)

    def post(self):
        form = LoginForm()

        if form.validate_on_submit():

            identifier = form.email.data  # (this can be email OR username)
            password = form.password.data

            # try email first
            user = User.get_by_email(identifier)

            # if not found, try username
            if not user:
                user = User.get_by_username(identifier)

            if user and check_password_hash(user.password, password):

                session["user"] = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_admin": user.is_admin
                }

                flash("Login successful!", "success")
                return redirect(url_for("dashboard.dashboard"))

            flash("Invalid username/email or password", "danger")

        return render_template("login.html", form=form)
# ============================================
# Register
# ============================================
class RegisterView(MethodView):

    def get(self):
        form = RegisterForm()
        return render_template("register.html", form=form)

    def post(self):
        form = RegisterForm()

        if form.validate_on_submit():

            # check email already exists
            if User.get_by_email(form.email.data):
                flash("Email already exists", "danger")
                return render_template("register.html", form=form)

            # check username already exists
            if User.get_by_username(form.username.data):
                flash("Username already exists", "danger")
                return render_template("register.html", form=form)

            room_data = Room.get_by_room_number(form.room_number.data)

            room_id = list(room_data.values())[0]["id"]
            print (room_id) 
            # create user
            User.create(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                room_id=int(room_id) 
            )

            flash("Account created successfully!", "success")
            return redirect(url_for("auth.login"))

        return render_template("register.html", form=form)

# ============================================
# Forgot Password
# ============================================
class ForgotPasswordView(MethodView):

    def get(self):
        form = ForgotPasswordForm()

        return render_template(
            "forgot_password.html",
            form=form
        )

    def post(self):
        form = ForgotPasswordForm()

        if form.validate_on_submit():

            user = User.get_by_email(
                form.email.data
            )

            if not user:
                flash(
                    "Email not found",
                    "danger"
                )

                return render_template(
                    "forgot_password.html",
                    form=form
                )

            # Add reset-password logic here
            flash(
                "Password reset instructions sent.",
                "info"
            )

            return redirect(
                url_for("auth.login")
            )

        return render_template(
            "forgot_password.html",
            form=form
        )


# ============================================
# Routes
# ============================================
auth_bp.add_url_rule(
    "/login",
    view_func=LoginView.as_view(
        "login"
    )
)

auth_bp.add_url_rule(
    "/register",
    view_func=RegisterView.as_view(
        "register"
    )
)

auth_bp.add_url_rule(
    "/forgot-password",
    view_func=ForgotPasswordView.as_view(
        "forgot_password"
    )
)