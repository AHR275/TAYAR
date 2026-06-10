from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask.views import MethodView
import random

from src.models import Room, Transaction, User
from src.middleware.db import db
from src.middleware.session_manager import SessionManager


payment_bp = Blueprint('payment', __name__)


class PaymentView(MethodView):
    """
    Handle payment page GET and POST requests
    """

    def get(self):
        user = SessionManager.get_user()
        if not user:
            return redirect(url_for("auth.login"))
        user_id = user["id"] 
        room_id = request.args.get('room')
        amount = request.args.get('amount')

        if not room_id or not amount:
            flash('Please select a room and amount first', 'warning')
            return redirect(url_for('topup.topup'))

        try:
            amount_float = float(amount)

            if amount_float <= 0:
                flash('Amount must be greater than 0', 'danger')
                return redirect(url_for('topup.topup'))

        except ValueError:
            flash('Invalid amount', 'danger')
            return redirect(url_for('topup.topup'))

        room = Room.get_by_id(room_id)

        if not room:
            flash('Room not found', 'danger')
            return redirect(url_for('topup.topup'))

        return render_template(
            'payment.html',
            room=room,
            amount=amount_float
        )

    def post(self):

        user = SessionManager.get_user()
        if not user:
            return redirect(url_for("auth.login"))
        user_id = user["id"] 
        room_id = request.form.get('room_id')
        amount = request.form.get('amount')
        payment_method = request.form.get('payment_method', 'card')

        if not room_id or not amount:
            flash('Missing payment information', 'danger')
            return redirect(url_for('topup.topup'))

        try:
            amount_float = float(amount)

            if amount_float <= 0:
                flash('Amount must be greater than 0', 'danger')
                return redirect(url_for('topup.topup'))

        except ValueError:
            flash('Invalid amount', 'danger')
            return redirect(url_for('topup.topup'))

        room = Room.get_by_id(room_id)

        if not room:
            flash('Room not found', 'danger')
            return redirect(url_for('topup.topup'))

        # ==========================
        # Get logged-in user
        # ==========================
        user = SessionManager.get_user()

        if not user:
            flash('Please login first', 'danger')
            return redirect(url_for('auth.login'))

        user_id = user["id"]

        # Simulate payment gateway (75% success rate)
        payment_successful = random.choice(
            [True, True, True, False]
        )

        if payment_successful:

            print(
                f"Processing payment: "
                f"Room={room_id}, "
                f"Amount={amount_float}, "
                f"User={user_id}"
            )

            try:

                print("User Session:")
                print(user)

                print("Room:")
                print(room)

                transaction = Transaction.create(
                    user_id=user_id,
                    amount=amount_float,
                    transaction_type='topup',
                    status='completed',
                    description=(
                        f"Top up for Room {room_id} "
                        f"via {payment_method}"
                    )
                )

                room = Room.get_by_id_obj(room_id)
                room.update_balance(amount_float)
                print("trans : " , transaction)
                print("tx_id " , transaction['id'])


                return redirect(
                    url_for(
                        'payment.success',
                        tx_id=transaction['id']
                    )
                )

            except Exception as e:

                db.session.rollback()

                flash(
                    f'Database error: {str(e)}',
                    'danger'
                )

                return render_template(
                    'fail.html',
                    room=room,
                    amount=amount_float
                )

        flash(
            'Payment failed. Please try again.',
            'danger'
        )

        return render_template(
            'fail.html',
            room=room,
            amount=amount_float
        )


class PaymentSuccessView(MethodView):
    """
    Handle payment success page
    """

    def get(self, tx_id):
        user = SessionManager.get_user()
        if not user:
            return redirect(url_for("auth.login"))
        user_id = user["id"] 
        transaction = Transaction.get_by_id(tx_id)

        if not transaction:
            flash(
                'Transaction not found',
                'danger'
            )

            return redirect(
                url_for(
                    'topup.topup'
                )
            )

        return render_template(
            'success.html',
            transaction=transaction
        )


# Routes
payment_bp.add_url_rule(
    '/payment',
    view_func=PaymentView.as_view('payment')
)

payment_bp.add_url_rule(
    '/payment/success/<int:tx_id>',
    view_func=PaymentSuccessView.as_view('success')
)