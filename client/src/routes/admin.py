from flask import Blueprint, render_template, redirect, url_for, flash 
from flask.views import MethodView

from src.models import User, Room, Transaction, AdminLog
from src.forms import AdminForms

from src.routes.analyze_admin import analysis_admin_bp

admin_bp = Blueprint(
"admin",
__name__,
url_prefix="/admin"
)

# =====================================================

# DASHBOARD

# =====================================================

class AdminDashboard(MethodView):


    def get(self):

        return render_template(
            "admin.html",

            users=User.get_all(),
            rooms=Room.get_all(),
            transactions=Transaction.get_all(),
            logs=AdminLog.get_all(),

            create_user_form=AdminForms.CreateUserForm(),
            update_user_form=AdminForms.UpdateUserForm(),
            delete_user_form=AdminForms.DeleteUserForm(),

            create_room_form=AdminForms.CreateRoomForm(),
            update_room_form=AdminForms.UpdateRoomForm(),
            delete_room_form=AdminForms.DeleteRoomForm()
        )


# =====================================================

# USERS

# =====================================================

class AdminUserCreate(MethodView):


    def post(self):

        form = AdminForms.CreateUserForm()

        if not form.validate_on_submit():

            flash(
                "Invalid user data",
                "error"
            )

            return redirect(
                url_for("admin.dashboard")
            )

        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )

        flash(
            "User created successfully",
            "success"
        )

        return redirect(
            url_for("admin.dashboard")
        )


class AdminUserUpdate(MethodView):


    def post(self):

        form = AdminForms.UpdateUserForm()
        print(form.user_id)
        print(form.email)
        print(form.username)
        if not form.validate_on_submit():

            flash(
                "Invalid user data",
                "error"
            )

            return redirect(
                url_for("admin.dashboard")
            )

        user = User.query.get_or_404(
            form.user_id.data
        )

        user.update_username(
            form.username.data
        )

        user.update_email(
            form.email.data
        )

        flash(
            "User updated successfully",
            "success"
        )

        return redirect(
            url_for("admin.dashboard")
        )


class AdminUserDelete(MethodView):


    def post(self):

        form = AdminForms.DeleteUserForm()

        

        if not form.validate_on_submit():

            flash(
                "Invalid request",
                "error"
            )

            return redirect(
                url_for("admin.dashboard")
            )

        user = User.query.get_or_404(
            form.user_id.data
        )

        user.delete()

        flash(
            "User deleted successfully",
            "success"
        )

        return redirect(
            url_for("admin.dashboard")
        )


# =====================================================

# ROOMS

# =====================================================

class AdminRoomCreate(MethodView):


    def post(self):

        form = AdminForms.CreateRoomForm()

        if not form.validate_on_submit():

            flash(
                "Invalid room data",
                "error"
            )

            return redirect(
                url_for("admin.dashboard")
            )

        Room.create(
            room_number=form.room_number.data,
            building=form.building.data,
            current_balance=form.balance.data
        )

        flash(
            "Room created successfully",
            "success"
        )

        return redirect(
            url_for("admin.dashboard")
        )


class AdminRoomUpdate(MethodView):


    def post(self):

        form = AdminForms.UpdateRoomForm()

        if not form.validate_on_submit():

            flash(
                "Invalid room data",
                "error"
            )

            return redirect(
                url_for("admin.dashboard")
            )

        room = Room.query.get_or_404(
            form.room_id.data
        )

        room.update_room_number(
            form.room_number.data
        )

        room.update_building(
            form.building.data
        )

        room.set_balance(
            form.balance.data
        )

        flash(
            "Room updated successfully",
            "success"
        )

        return redirect(
            url_for("admin.dashboard")
        )


class AdminRoomDelete(MethodView):


    def post(self):

        form = AdminForms.DeleteRoomForm()

        if not form.validate_on_submit():

            flash(
                "Invalid request",
                "error"
            )

            return redirect(
                url_for("admin.dashboard")
            )

        room = Room.query.get_or_404(
            form.room_id.data
        )

        room.delete()

        flash(
            "Room deleted successfully",
            "success"
        )

        return redirect(
            url_for("admin.dashboard")
        )


# =====================================================

# ROUTES

# =====================================================
admin_bp.register_blueprint(analysis_admin_bp)
admin_bp.add_url_rule(
"/",
view_func=AdminDashboard.as_view(
"dashboard"
)
)

admin_bp.add_url_rule(
"/users/create",
view_func=AdminUserCreate.as_view(
"create_user"
)
)

admin_bp.add_url_rule(
"/users/update",
view_func=AdminUserUpdate.as_view(
"update_user"
)
)

admin_bp.add_url_rule(
"/users/delete",
view_func=AdminUserDelete.as_view(
"delete_user"
)
)

admin_bp.add_url_rule(
"/rooms/create",
view_func=AdminRoomCreate.as_view(
"create_room"
)
)

admin_bp.add_url_rule(
"/rooms/update",
view_func=AdminRoomUpdate.as_view(
"update_room"
)
)

admin_bp.add_url_rule(
"/rooms/delete",
view_func=AdminRoomDelete.as_view(
"delete_room"
)
)
