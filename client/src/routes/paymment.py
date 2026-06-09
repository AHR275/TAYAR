from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask.views import MethodView
from datetime import datetime
import random

from src.models import Room, Transaction, User  # استيراد صحيح
from src.middleware.db import db

payment_bp = Blueprint('payment', __name__)


class PaymentView(MethodView):
    """
    Handle payment page GET and POST requests
    """

    def get(self):
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

        # Get room by ID (assuming Room.get_by_id exists)
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
        room_id = request.form.get('room_id')
        print("room id :", room_id)
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

        # Get room
        room = Room.get_by_id(room_id)

        if not room:
            flash('Room not found', 'danger')
            return redirect(url_for('topup.topup'))

        # ✅ الحصول على user_id من الجلسة
        user_id = session.get("user_id")
        
        # ✅ إذا لم يكن هناك user_id، حاول الحصول على أول مستخدم من قاعدة البيانات
        # if not user_id:
        #     first_user = User.query.first()
        #     if first_user:
        #         user_id = first_user.id
        #         flash(f'No active session. Using user: {first_user.username}', 'warning')
        #     else:
        #         flash('No user found in database. Please register or login.', 'danger')
        #         return redirect(url_for('auth.login'))

        # # ✅ التحقق من وجود المستخدم فعلاً في قاعدة البيانات
        # user = User.query.get(user_id)
        # if not user:
        #     flash(f'User with ID {user_id} not found. Please login again.', 'danger')
        #     return redirect(url_for('auth.login'))

        # Simulate payment gateway (75% success rate)
        payment_successful = random.choice([True, True, True, False])

        if payment_successful:
            print(f"Processing payment: Room={room_id}, Amount={amount_float}, User={user_id}")
            
            # ✅ إنشاء المعاملة باستخدام Transaction.create
            try:
                print(room)
                # transaction = Transaction.create(
                #     user_id=user_id,
                #     amount=amount_float,
                #     transaction_type='topup',  # هذا يطابق الـ Enum
                #     status='completed',
                #     description=f'Top up for Room {room.room_number if hasattr(room, "room_number") else room_id} via {payment_method}'
                # )
                
                # # تحديث رصيد الغرفة (افترض وجود طريقة update_balance)
                # # إذا كان Room model عنده update_balance
                # if hasattr(Room, 'update_balance'):
                #     Room.update_balance(room_id, amount_float)
                # else:
                #     # إذا لم يكن موجود، يمكنك إضافته لاحقاً
                #     print(f"Room balance update needed for room {room_id}")
                
                # flash(f'Payment successful! Transaction ID: {transaction.id}', 'success')
                return redirect(url_for('payment.success', tx_id=20))
                
            except Exception as e:
                db.session.rollback()
                flash(f'Database error: {str(e)}', 'danger')
                return render_template('fail.html', room=room, amount=amount_float)

        # Payment failed
        flash('Payment failed. Please try again.', 'danger')
        return render_template('fail.html', room=room, amount=amount_float)


class PaymentSuccessView(MethodView):
    """
    Handle payment success page
    """

    def get(self, tx_id):
        # Transaction.get_by_id قد لا تكون موجودة، نستخدم query مباشرة
        transaction = Transaction.query.get(tx_id)

        if not transaction:
            flash('Transaction not found', 'danger')
            return redirect(url_for('topup.topup'))

        return render_template('success.html', transaction=transaction)


# Routes
payment_bp.add_url_rule('/payment', view_func=PaymentView.as_view('payment'))
payment_bp.add_url_rule('/payment/success/<int:tx_id>', view_func=PaymentSuccessView.as_view('success'))