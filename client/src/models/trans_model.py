# src/models.py
from src.middleware.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# ============================================
# Transaction Model
# ============================================
class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.Enum('topup', 'payment'), nullable=False)
    status = db.Column(db.String(50), default='pending')
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ---------- Create ----------
    @classmethod
    def create(cls, user_id, amount, transaction_type, status='pending', description=''):
        transaction = cls(
            user_id=user_id,
            amount=amount,
            type=transaction_type,
            status=status,
            description=description
        )
        db.session.add(transaction)
        db.session.commit()
        return transaction.to_dict()

    # ---------- Read ----------
    @classmethod
    def get_all(cls):
        txs = cls.query.order_by(cls.created_at.desc()).all()
        return {
            tx.id: tx.to_dict()
            for tx in txs
        }

    @classmethod
    def get_by_user(cls, user_id):
        txs = cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()
        return {
            tx.id: tx.to_dict()
            for tx in txs
        }
    @classmethod
    def get_by_id(cls, tx_id):
        tx = cls.query.filter_by(id=tx_id).first()
        return {
            tx.id: tx.to_dict()
            
        }

   

    @classmethod
    def get_by_type(cls, transaction_type):
        return cls.query.filter_by(type=transaction_type).order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_status(cls, status):
        return cls.query.filter_by(status=status).order_by(cls.created_at.desc()).all()

    # ---------- Update ----------
    def update_status(self, status):
        self.status = status
        db.session.commit()

    def update_description(self, description):
        self.description = description
        db.session.commit()

    # ---------- Delete ----------
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # ---------- Serialization ----------
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": float(self.amount),
            "type": self.type,
            "status": self.status,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }




