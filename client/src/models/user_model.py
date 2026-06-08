# src/models.py
from src.middleware.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# ============================================
# User Model
# ============================================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    transactions = db.relationship(
        'Transaction',
        backref='user',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    admin_logs = db.relationship(
        'AdminLog',
        backref='admin',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    # ---------- Create ----------
    @classmethod
    def create(cls, username, email, password, room_id=None, is_admin=False):
        user = cls(
            username=username,
            email=email,
            password=generate_password_hash(password),
            room_id=room_id,
            is_admin=is_admin
        )
        db.session.add(user)
        db.session.commit()
        return user

    # ---------- Read ----------
    @classmethod     
    def get_all(cls):
        users = cls.query.all()
        return {
            user.id: user.to_dict()
            for user in users
    }

    @classmethod
    def get_by_id(cls, user_id):
        user = cls.query.get(user_id)
        return {"user": user.to_dict() if user else None}

   

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return user
        return None

    # ---------- Update ----------
    def update_username(self, username):
        self.username = username
        db.session.commit()

    def update_email(self, email):
        self.email = email
        db.session.commit()

    def update_password(self, password):
        self.password = generate_password_hash(password)
        db.session.commit()

    def update_room(self, room_id):
        self.room_id = room_id
        db.session.commit()

    # ---------- Delete ----------
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # ---------- Relationships ----------
    def get_transactions(self):
        return self.transactions.all()

    def create_transaction(self, amount, transaction_type, status='pending', description=''):
        from src.models import Transaction
        transaction = Transaction(
            user_id=self.id,
            amount=amount,
            type=transaction_type,
            status=status,
            description=description
        )
        db.session.add(transaction)
        db.session.commit()
        return transaction

    # ---------- Serialization ----------
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "room_id": self.room_id,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }



