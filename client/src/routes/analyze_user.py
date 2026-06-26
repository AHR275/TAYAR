from collections import defaultdict

from flask import Blueprint, render_template, redirect, url_for
from flask.views import MethodView

from src.middleware.session_manager import SessionManager
from src.models import User, Room, ElectricityUsage


analysis_user_bp = Blueprint(
    "analyze_user",
    __name__,
    url_prefix="/analysis"
)


# =====================================================
# USER ELECTRICITY ANALYSIS
# =====================================================

class UserAnalysisDashboard(MethodView):

    def get(self):

        current_user = SessionManager.get_user()

        if not current_user:
            return redirect(url_for("auth.login"))

        user_data = User.get_by_id(
            current_user["id"]
        )

        user = user_data.get("user")

        if not user or not user.get("room_id"):

            return render_template(
                "analyze_user.html",
                room=None,
                usages={}
            )

        room = Room.query.get(
            user["room_id"]
        )

        usages = ElectricityUsage.get_by_room(
            user["room_id"]
        )

        # ==========================================
        # Statistics
        # ==========================================

        total_consumption = 0
        total_amount = 0

        highest_usage = 0
        highest_month = None

        latest_bill = 0
        latest_month = None

        monthly_labels = []
        monthly_usage = []
        monthly_bill = []

        for usage in usages.values():

            consumption = float(
                usage["consumption_kwh"]
            )

            amount = float(
                usage["amount_due"]
            )

            month = usage["month"][:7]

            total_consumption += consumption
            total_amount += amount

            monthly_labels.append(month)
            monthly_usage.append(consumption)
            monthly_bill.append(amount)

            if consumption > highest_usage:

                highest_usage = consumption
                highest_month = month

            latest_month = month
            latest_bill = amount

        average_consumption = 0

        if len(usages) > 0:

            average_consumption = (
                total_consumption /
                len(usages)
            )

        return render_template(

            "analyze_user.html",

            room=room,

            usages=usages,

            total_consumption=round(
                total_consumption,
                2
            ),

            total_amount=round(
                total_amount,
                2
            ),

            average_consumption=round(
                average_consumption,
                2
            ),

            highest_usage=round(
                highest_usage,
                2
            ),

            highest_month=highest_month,

            latest_bill=round(
                latest_bill,
                2
            ),

            latest_month=latest_month,

            monthly_labels=monthly_labels,

            monthly_usage=monthly_usage,

            monthly_bill=monthly_bill
        )


# =====================================================
# ROUTES
# =====================================================

analysis_user_bp.add_url_rule(
    "/",
    view_func=UserAnalysisDashboard.as_view(
        "dashboard"
    )
)