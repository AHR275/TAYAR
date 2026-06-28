from collections import defaultdict

from flask import Blueprint, render_template
from flask.views import MethodView

from src.models import (
    ElectricityUsage,
    Room,
    Transaction,
    User
)


analysis_admin_bp = Blueprint(
    "analyze_admin",
    __name__,
    url_prefix="/analysis"
)


# =====================================================
# ELECTRICITY ANALYSIS DASHBOARD
# =====================================================

class ElectricityAnalysisDashboard(MethodView):

    def get(self):

        # =====================================================
        # Load Data
        # =====================================================

        usages = ElectricityUsage.get_all()
        transactions = Transaction.get_all()
        users = User.get_all()
        rooms= Room.get_all()

        # Create lookup table to avoid querying the database
        # for every transaction.

        user_lookup = {
            user["id"]: user
            for user in users.values()
        }

        # =====================================================
        # Split Transactions
        # =====================================================

        payment_transactions = [
            transaction
            for transaction in transactions.values()
            if transaction["type"] == "payment"
        ]

        topup_transactions = [
            transaction
            for transaction in transactions.values()
            if transaction["type"] == "topup"
        ]

        # print(topup_transactions, payment_transactions)

        completed_payments = [
            transaction
            for transaction in payment_transactions
            if transaction["status"] in ("completed", "success")
        ]

        completed_topups = [
            transaction
            for transaction in topup_transactions
            if transaction["status"] in ("completed", "success")
        ]
        # =====================================================
        # Overall Statistics
        # =====================================================

        total_consumption = 0

        total_payment = 0
        total_topup = 0

        highest_usage = 0
        highest_room = None

        lowest_usage = None
        lowest_room = None

        room_totals = defaultdict(float)

        # =====================================================
        # Chart Data
        # =====================================================

        monthly_consumption = defaultdict(float)
        monthly_payment = defaultdict(float)

        room_consumption = defaultdict(float)
        room_revenue = defaultdict(float)

        # =====================================================
        # Electricity Statistics
        # =====================================================

        for usage in usages.values():

            room_id = usage["room_id"]
            room_number = f"{rooms[room_id]['room_number']}"
            room_name = f"Room {room_number}"
            usage['room_name']= room_number

            month = usage["month"][:7]

            consumption = float(
                usage["consumption_kwh"]
            )

            total_consumption += consumption

            room_totals[room_id] += consumption

            monthly_consumption[month] += consumption

            room_consumption[room_name] += consumption

        # =====================================================
        # Room Statistics
        # =====================================================

        for room_id, consumption in room_totals.items():

            room = Room.query.get(room_id)

            if consumption > highest_usage:

                highest_usage = consumption
                highest_room = room

            if lowest_usage is None or consumption < lowest_usage:

                lowest_usage = consumption
                lowest_room = room

        # =====================================================
        # Payment Statistics
        # =====================================================

        total_payment = sum(
            float(transaction["amount"])
            for transaction in completed_payments
        )

        total_topup = sum(
            float(transaction["amount"])
            for transaction in completed_topups
        )

        pending_payment = sum(
            float(transaction["amount"])
            for transaction in payment_transactions
            if transaction["status"] == "pending"
        )

        # =====================================================
        # Revenue By Room
        # =====================================================

        for transaction in completed_topups:

            user = user_lookup.get(
                transaction["user_id"]
            )

            if not user:
                continue

            room_name = f"Room {rooms[user['room_id']]['room_number']}"

            room_revenue[room_name] += float(
                transaction["amount"]
            )

            month = transaction["created_at"][:7]

            monthly_payment[month] += float(
                transaction["amount"]
            )

        # =====================================================
        # Latest Transactions
        # =====================================================

        latest_payment = None
        latest_topup = None

        latest_payment_amount = 0
        latest_topup_amount = 0

        if payment_transactions:

            latest_payment = max(
                payment_transactions,
                key=lambda transaction:
                transaction["created_at"]
            )

            latest_payment_amount = float(
                latest_payment["amount"]
            )

        if topup_transactions:

            latest_topup = max(
                topup_transactions,
                key=lambda transaction:
                transaction["created_at"]
            )

            latest_topup_amount = float(
                latest_topup["amount"]
            )

        # =====================================================
        # Highest Revenue Room
        # =====================================================

        highest_revenue = 0
        highest_revenue_room = None

        for room_name, revenue in room_revenue.items():

            if revenue > highest_revenue:

                highest_revenue = revenue
                highest_revenue_room = room_name

        # =====================================================
        # Peak Consumption Month
        # =====================================================

        peak_month = None
        peak_month_usage = 0

        for month, value in monthly_consumption.items():

            if value > peak_month_usage:

                peak_month = month
                peak_month_usage = value

        # =====================================================
        # Average Consumption
        # =====================================================

        average_consumption = 0

        if usages:

            average_consumption = (
                total_consumption /
                len(usages)
            )

                # =====================================================
        # Render Dashboard
        # =====================================================

        return render_template(

            "analyze_admin.html",

            usages=usages,

            rooms=Room.get_all(),

            # -----------------------------------------
            # Electricity Statistics
            # -----------------------------------------

            total_consumption=round(
                total_consumption,
                2
            ),

            average_consumption=round(
                average_consumption,
                2
            ),

            highest_room=highest_room,

            highest_usage=round(
                highest_usage,
                2
            ),

            lowest_room=lowest_room,

            lowest_usage=round(
                lowest_usage,
                2
            ) if lowest_usage is not None else 0,

            peak_month=peak_month,

            peak_month_usage=round(
                peak_month_usage,
                2
            ),

            # -----------------------------------------
            # Financial Statistics
            # -----------------------------------------

            total_amount=round(
                total_topup+total_payment,
                2
            ),

            total_payment=round(
                total_payment,
                2
            ),

            total_topup=round(
                total_topup,
                2
            ),

            pending_payment=round(
                pending_payment,
                2
            ),

            latest_payment=round(
                latest_payment_amount,
                2
            ),

            latest_topup=round(
                latest_topup_amount,
                2
            ),

            highest_revenue_room=highest_revenue_room,

            highest_revenue=round(
                highest_revenue,
                2
            ),

            # -----------------------------------------
            # Charts
            # -----------------------------------------

            monthly_labels=list(
                monthly_consumption.keys()
            ),

            monthly_values=list(
                monthly_consumption.values()
            ),

            monthly_payment_labels=list(
                monthly_payment.keys()
            ),

            monthly_payment_values=list(
                monthly_payment.values()
            ),

            room_labels=list(
                room_consumption.keys()
            ),

            room_values=list(
                room_consumption.values()
            ),

            revenue_labels=list(
                room_revenue.keys()
            ),

            revenue_values=list(
                room_revenue.values()
            )
        )


# =====================================================
# ROUTES
# =====================================================

analysis_admin_bp.add_url_rule(
    "/",
    view_func=ElectricityAnalysisDashboard.as_view(
        "dashboard"
    )
)