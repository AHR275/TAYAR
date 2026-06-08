from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask.views import MethodView
from datetime import datetime
import random

from src.models.room_model import Room
from src.models.trans_model import Transaction

payment_bp = Blueprint('payment', __name__)


class PaymentView(MethodView):
    """
    Handle payment page GET and POST requests
    """

    def get(self):
        room_number = request.args.get('room')
        amount = request.args.get('amount')

        if not room_number or not amount:
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

        room = Room.get_by_id(room_number)

        if not room:
            flash('Room not found', 'danger')
            return redirect(url_for('topup.topup'))

        return render_template(
            'payment.html',
            room=room,
            amount=amount_float
        )

    def post(self):
        room_number = request.form.get('room')
        amount = request.form.get('amount')
        payment_method = request.form.get('payment_method', 'card')

        if not room_number or not amount:
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

        room = Room.get_by_room_number(room_number)

        if not room:
            flash('Room not found', 'danger')
            return redirect(url_for('topup.topup'))

        user_id = session.get("user_id")

        if not user_id:
            flash('Please login first', 'danger')
            return redirect(url_for('auth.login'))

        # Simulate payment gateway
        payment_successful = random.choice([True, True, True, False])

        if payment_successful:

            # Create transaction record
            transaction = Transaction.create(
                user_id=user_id,
                amount=amount_float,
                transaction_type='topup',
                status='completed',
                description=f'Top up for Room {room.room_number} via {payment_method}'
            )

            # Update room balance
            room.update_balance(amount_float)

            flash(
                f'Payment successful! Transaction ID: {transaction.id}',
                'success'
            )

            return redirect(
                url_for(
                    'payment.success',
                    tx_id=transaction.id
                )
            )

        flash('Payment failed. Please try again.', 'danger')

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

        transaction = Transaction.get_by_id(tx_id)

        if not transaction:
            flash('Transaction not found', 'danger')
            return redirect(url_for('topup.topup'))

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