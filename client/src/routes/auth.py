from flask import Blueprint, render_template, flash, redirect, url_for
from flask.views import MethodView

from src.forms.auth_forms import (
    LoginForm,
    RegisterForm,
    ForgotPasswordForm
)
from src.middleware.data_center import UsersData

auth_bp = Blueprint("auth", __name__)


class LoginView(MethodView):

    def get(self):
        form = LoginForm()
        return render_template("login.html", form=form)

    def post(self):
        form = LoginForm()

        if form.validate_on_submit():

            users = UsersData.get_users(self)

            email = form.email.data
            password = form.password.data

            user = next(
                (
                    u for u in users
                    if u["email"] == email
                    and u["password"] == password
                ),
                None
            )

            if user:
                flash("Login successful!", "success")

                return redirect(
                    url_for("dashboard.dashboard")
                )

            flash(
                "Invalid email or password",
                "danger"
            )

        return render_template(
            "login.html",
            form=form
        )
class RegisterView(MethodView):

    def get(self):
        form = RegisterForm()
        return render_template("register.html", form=form)

    def post(self):
        form = RegisterForm()

        if form.validate_on_submit():
            # register logic
            pass

        return render_template("register.html", form=form)
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
            # reset logic
            pass

        return render_template(
            "forgot_password.html",
            form=form
        )    
auth_bp.add_url_rule(
    "/login",
    view_func=LoginView.as_view("login")
)

auth_bp.add_url_rule(
    "/register",
    view_func=RegisterView.as_view("register")
)

auth_bp.add_url_rule(
    "/forgot-password",
    view_func=ForgotPasswordView.as_view("forgot_password")
)    