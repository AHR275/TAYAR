from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session
)
from flask.views import MethodView
from werkzeug.security import generate_password_hash

from src.middleware.db import db
from src.forms.profile_forms import ProfileForm
from src.models import User


profile_bp = Blueprint(
    "profile",
    __name__,
    url_prefix="/profile"
)


# =====================================================
# Profile
# =====================================================

class ProfileView(MethodView):

    def get(self):

        current = session.get("user")

        if not current:
            return redirect(url_for("auth.login"))

        user = User.query.get(current["id"])

        if not user:
            session.clear()

            flash(
                "User not found.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        form = ProfileForm()

        form.username.data = user.username
        form.email.data = user.email

        return render_template(
            "profile.html",
            form=form
        )

    def post(self):

        current = session.get("user")

        if not current:
            return redirect(url_for("auth.login"))

        user = User.query.get(current["id"])

        if not user:
            session.clear()

            flash(
                "User not found.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        form = ProfileForm()

        if form.validate_on_submit():

            # -----------------------------------------
            # Username already exists
            # -----------------------------------------

            existing_username = User.get_by_username(
                form.username.data
            )

            if (
                existing_username
                and existing_username.id != user.id
            ):

                flash(
                    "Username already exists.",
                    "danger"
                )

                return render_template(
                    "profile.html",
                    form=form
                )

            # -----------------------------------------
            # Email already exists
            # -----------------------------------------

            existing_email = User.get_by_email(
                form.email.data
            )

            if (
                existing_email
                and existing_email.id != user.id
            ):

                flash(
                    "Email already exists.",
                    "danger"
                )

                return render_template(
                    "profile.html",
                    form=form
                )

            # -----------------------------------------
            # Update user
            # -----------------------------------------

            user.username = form.username.data
            user.email = form.email.data

            if form.password.data:
                user.password = generate_password_hash(
                    form.password.data
                )

            db.session.commit()

            # -----------------------------------------
            # Update session
            # -----------------------------------------

            session["user"] = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin
            }

            flash(
                "Profile updated successfully!",
                "success"
            )

            return redirect(
                url_for("profile.profile")
            )

        return render_template(
            "profile.html",
            form=form
        )



# =====================================================
# Routes
# =====================================================

profile_bp.add_url_rule(
    "/",
    view_func=ProfileView.as_view(
        "profile"
    )
)

