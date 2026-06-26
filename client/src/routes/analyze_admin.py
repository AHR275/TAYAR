from collections import defaultdict

from flask import Blueprint, render_template
from flask.views import MethodView

from src.models import ElectricityUsage, Room


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

        usages = ElectricityUsage.get_all()

        # ============================================
        # Overall Statistics
        # ============================================

        total_consumption = 0
        total_amount = 0

        room_totals = defaultdict(float)

        highest_room = None
        highest_usage = 0

        lowest_room = None
        lowest_usage = None

        # ============================================
        # Chart Data
        # ============================================

        monthly_data = defaultdict(float)
        room_consumption = defaultdict(float)
        room_revenue = defaultdict(float)

        # ============================================
        # Process Usage Records
        # ============================================

        for usage in usages.values():

            room_id = usage["room_id"]
            month = usage["month"][:7]

            consumption = float(usage["consumption_kwh"])
            amount = float(usage["amount_due"])

            total_consumption += consumption
            total_amount += amount

            room_totals[room_id] += consumption

            monthly_data[month] += consumption

            room_name = f"Room {room_id}"

            room_consumption[room_name] += consumption
            room_revenue[room_name] += amount

        # ============================================
        # Highest / Lowest Consumption Room
        # ============================================

        for room_id, consumption in room_totals.items():

            if consumption > highest_usage:

                highest_usage = consumption
                highest_room = Room.query.get(room_id)

            if lowest_usage is None or consumption < lowest_usage:

                lowest_usage = consumption
                lowest_room = Room.query.get(room_id)

        # ============================================
        # Average Consumption
        # ============================================

        average_consumption = 0

        if len(usages) > 0:

            average_consumption = (
                total_consumption /
                len(usages)
            )

        # ============================================
        # Highest Revenue Room
        # ============================================

        highest_revenue = 0
        highest_revenue_room = None

        for room_name, revenue in room_revenue.items():

            if revenue > highest_revenue:

                highest_revenue = revenue
                highest_revenue_room = room_name

        # ============================================
        # Monthly Peak
        # ============================================

        peak_month = None
        peak_month_usage = 0

        for month, value in monthly_data.items():

            if value > peak_month_usage:

                peak_month = month
                peak_month_usage = value

        # ============================================
        # Render Dashboard
        # ============================================

        return render_template(

            "analyze_admin.html",

            usages=usages,

            rooms=Room.get_all(),

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

            highest_revenue_room=highest_revenue_room,
            highest_revenue=round(
                highest_revenue,
                2
            ),

            peak_month=peak_month,
            peak_month_usage=round(
                peak_month_usage,
                2
            ),

            monthly_labels=list(
                monthly_data.keys()
            ),

            monthly_values=list(
                monthly_data.values()
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