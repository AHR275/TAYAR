from flask import Blueprint, render_template, session, redirect, url_for
from flask.views import MethodView

from src.models import User , Room , Transaction
from src.middleware.session_manager import SessionManager


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


dashboard_bp.add_url_rule(
    "/",
    view_func=DashboardView.as_view("dashboard")
)