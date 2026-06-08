from flask import Blueprint, render_template
from flask.views import MethodView

from src.models.user_model import User
from src.models.room_model import Room

dashboard_bp = Blueprint(
"dashboard",
__name__,
url_prefix="/dashboard"
)

class DashboardView(MethodView):


    def get(self):

        # Temporary user for demo
        user_data = User.get_by_id(1)
        print("user_data")
        user = user_data.get("user")
        # print(user)
        room = None

        if user and user.get("room_id"):
            room_data = Room.get_by_id(user["room_id"])
            room = room_data.get("room")

        transactions = []
       
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
