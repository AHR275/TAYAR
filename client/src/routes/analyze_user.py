from flask import Blueprint, render_template, redirect, url_for
from flask.views import MethodView

from src.middleware.session_manager import SessionManager
from src.models import User, Room, ElectricityUsage, Transaction


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

        user_data = User.get_by_id(current_user["id"])
        user = user_data.get("user")

        if not user or not user.get("room_id"):
            return render_template(
                "analyze_user.html",
                room=None,
                usages={}
            )

        room = Room.query.get(user["room_id"])

        usages = ElectricityUsage.get_by_room(user["room_id"])
        transactions = Transaction.get_by_user(user["id"])

        # =====================================================
        # Split transactions
        # =====================================================

        payment_transactions = [
            t for t in transactions.values()
            if t["type"] == "payment"
        ]

        topup_transactions = [
            t for t in transactions.values()
            if t["type"] == "topup"
        ]

        # =====================================================
        # Electricity statistics
        # =====================================================

        total_consumption = 0
        highest_usage = 0
        highest_month = None

        monthly_labels = []
        monthly_usage = []
        monthly_bill = []

        for usage in usages.values():

            consumption = float(usage["consumption_kwh"])
            month = usage["month"][:7]

            total_consumption += consumption

            monthly_labels.append(month)
            monthly_usage.append(consumption)

            if consumption > highest_usage:
                highest_usage = consumption
                highest_month = month

        average_consumption = (
            total_consumption / len(usages)
            if usages else 0
        )

        # =====================================================
        # Payment statistics
        # =====================================================

        completed_payments = [
            t for t in topup_transactions
            if t["status"] == "completed"
        ]

        total_amount = sum(
            float(t["amount"])
            for t in completed_payments
        )

        pending_amount = sum(
            float(t["amount"])
            for t in topup_transactions
            if t["status"] == "pending"
        )

        latest_bill = 0
        latest_month = None

        if topup_transactions:

            latest_payment = max(
                topup_transactions,
                key=lambda t: t["created_at"]
            )

            latest_bill = float(latest_payment["amount"])
            latest_month = latest_payment["created_at"][:7]

        # =====================================================
        # Top-up statistics
        # =====================================================

        completed_topups = [
            t for t in topup_transactions
            if t["status"] == "completed"
        ]

        total_topup = sum(
            float(t["amount"])
            for t in completed_topups
        )

        latest_topup = 0

        if topup_transactions:

            latest_topup_transaction = max(
                topup_transactions,
                key=lambda t: t["created_at"]
            )

            latest_topup = float(
                latest_topup_transaction["amount"]
            )

        # =====================================================
        # Monthly bill chart
        # =====================================================

        payment_by_month = {}

        for payment in completed_payments:

            month = payment["created_at"][:7]

            payment_by_month[month] = (
                payment_by_month.get(month, 0)
                + float(payment["amount"])
            )

        for month in monthly_labels:
            monthly_bill.append(
                payment_by_month.get(month, 0)
            )

        # =====================================================
        # Render
        # =====================================================

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

            total_topup=round(
                total_topup,
                2
            ),

            latest_topup=round(
                latest_topup,
                2
            ),

            pending_amount=round(
                pending_amount,
                2
            ),

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