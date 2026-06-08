from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask.views import MethodView
from datetime import datetime
import uuid
import random

# استيراد دوال Data Center
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.middleware.data_center import TransData, UsersData, RoomsData

payment_bp = Blueprint('payment', __name__)

trans_data = TransData()
users_data = UsersData()
rooms_data = RoomsData()


class PaymentView(MethodView):
    """Handle payment page GET and POST requests"""
    
    def get(self):
        """Display payment page"""
        room_number = request.args.get('room')
        amount = request.args.get('amount')
        
        print(f"Payment page visited: room={room_number}, amount={amount}")
        
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
        
        room = rooms_data.get_room(room_number)
        if not room:
            flash('Room not found', 'danger')
            return redirect(url_for('topup.topup'))
        
        return render_template('payment.html', room=room_number, amount=amount)
    
    def post(self):
        """Process payment confirmation"""
        room = request.form.get('room')
        amount = request.form.get('amount')
        payment_method = request.form.get('payment_method', 'card')
        
        if not room or not amount:
            flash('Missing payment information', 'danger')
            return redirect(url_for('topup.topup'))
        
        # Simulate payment processing (75% success rate)
        payment_successful = random.choice([True, True, True, False])
        
        transaction_id = str(uuid.uuid4())[:8].upper()
        
        if payment_successful:
            # Create transaction object
            transaction = {
                'id': transaction_id,
                'room': room,
                'amount': float(amount),
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'completed',
                'payment_method': payment_method
            }
            
            # Save using Data Center
            trans_data.add_transaction(transaction)
            
            flash(f'Payment successful! Transaction ID: {transaction_id}', 'success')
            return redirect(url_for('payment.success', tx_id=transaction_id))
        else:
            # Payment failed
            flash('Payment failed. Please try again.', 'danger')
            return render_template('fail.html', room=room, amount=amount)


class PaymentSuccessView(MethodView):
    """Handle payment success page"""
    
    def get(self, tx_id):
        transaction = trans_data.get_transaction(tx_id)
        if not transaction:
            flash('Transaction not found', 'danger')
            return redirect(url_for('topup.topup'))
        return render_template('success.html', transaction=transaction)


# Register routes
payment_bp.add_url_rule('/payment', view_func=PaymentView.as_view('payment'))
payment_bp.add_url_rule('/payment/success/<tx_id>', view_func=PaymentSuccessView.as_view('success'))