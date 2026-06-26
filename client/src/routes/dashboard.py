from flask import Blueprint, render_template, session, redirect, url_for , flash  , request 
from flask.views import MethodView

from src.models import User , Room , Transaction
from src.middleware.session_manager import SessionManager
from src.forms import DashboardForms


dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


class DashboardView(MethodView):
    def get(self):
        user = SessionManager.get_user()

          

        

        if not user:
            return redirect(url_for("auth.login"))
        user_id = user["id"] 

        user_data = User.get_by_id(user_id)
        user = user_data.get("user")

        room = None

        if user and user.get("room_id"):
            room_data = Room.get_by_id(user["room_id"])
            room = room_data.get("room")

        transactions = Transaction.get_by_user(user_id)
        # print(transactions)

        return render_template(
            "dashboard.html",
            user=user,
            room=room,
            transactions=transactions
        )




class ProfileView(MethodView):

    def get(self):

        current_user = SessionManager.get_user()

        if not current_user:
            return redirect(url_for("auth.login"))

        user = User.query.get(current_user["id"])

        form = DashboardForms.ProfileForm()

        form.username.data = user.username
        form.email.data = user.email

        return render_template(
            "profile.html",
            form=form,
            user=user.to_dict()
        )

    def post(self):

        current_user = SessionManager.get_user()

        if not current_user:
            return redirect(url_for("auth.login"))

        user = User.query.get(current_user["id"])

        form = DashboardForms.ProfileForm()

        if not form.validate_on_submit():
            return render_template(
                "profile.html",
                form=form,
                user=user.to_dict()
            )

        if form.username.data != user.username:

            existing = User.get_by_username(form.username.data)

            if existing and existing.id != user.id:
                flash("Username already exists", "error")
                return redirect(url_for("dashboard.profile"))

            user.update_username(form.username.data)

        if form.email.data != user.email:

            existing = User.get_by_email(form.email.data)

            if existing and existing.id != user.id:
                flash("Email already exists", "error")
                return redirect(url_for("dashboard.profile"))

            user.update_email(form.email.data)

        if form.password.data:
            user.update_password(form.password.data)

        flash("Profile updated successfully", "success")

        return redirect(url_for("dashboard.profile"))

dashboard_bp.add_url_rule(
    "/profile",
    view_func=ProfileView.as_view("profile")
)




dashboard_bp.add_url_rule(
    "/",
    view_func=DashboardView.as_view("dashboard")
)