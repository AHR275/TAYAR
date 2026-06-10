from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask.views import MethodView

from src.models import User, Room, Transaction, AdminLog


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# =====================================================
# MAIN DASHBOARD (ALL IN ONE PAGE)
# =====================================================
class AdminDashboard(MethodView):

    def get(self):

        return render_template(
            "admin.html",
            users=User.get_all(),
            rooms=Room.get_all(),
            transactions=Transaction.get_all(),
            logs=AdminLog.get_all()
        )


# =====================================================
# USERS ACTIONS
# =====================================================
class AdminUsers(MethodView):

    def post(self):

        action = request.form.get("action")

        # CREATE
        if action == "create":
            User.create(
                request.form["username"],
                request.form["email"],
                request.form["password"],
                request.form.get("room_id")
            )
            flash("User created", "success")

        # UPDATE (NO raw DB)
        elif action == "update":
            user = User.query.get_or_404(request.form["user_id"])
            user.update_username(request.form["username"])
            user.update_email(request.form["email"])
            user.update_room(request.form.get("room_id"))

            flash("User updated", "success")

        # DELETE (USING MODEL METHOD)
        elif action == "delete":
            user = User.query.get_or_404(request.form["user_id"])
            user.delete()

            flash("User deleted", "success")

        return redirect(url_for("admin.dashboard"))


# =====================================================
# ROOMS ACTIONS
# =====================================================
class AdminRooms(MethodView):

    def post(self):

        action = request.form.get("action")

        # CREATE
        if action == "create":
            Room.create(
                request.form["room_number"],
                request.form["building"],
                request.form.get("balance", 0)
            )
            flash("Room created", "success")

        # UPDATE (USING MODEL METHODS)
        elif action == "update":
            room = Room.query.get_or_404(request.form["room_id"])

            room.update_room_number(request.form["room_number"])
            room.update_building(request.form["building"])
            room.set_balance(request.form["balance"])

            flash("Room updated", "success")

        # DELETE (USING MODEL METHOD)
        elif action == "delete":
            room = Room.query.get_or_404(request.form["room_id"])
            room.delete()

            flash("Room deleted", "success")

        return redirect(url_for("admin.dashboard"))
    
admin_bp.add_url_rule(
    "/", view_func=AdminDashboard.as_view("dashboard")
)

admin_bp.add_url_rule(
    "/users", view_func=AdminUsers.as_view("users")
)

admin_bp.add_url_rule(
    "/rooms", view_func=AdminRooms.as_view("rooms")
)

