# src/models.py
from src.middleware.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime



# ============================================
# ElectricityUsage Model
# ============================================
class ElectricityUsage(db.Model):
    __tablename__ = "electricity_usage"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    month = db.Column(db.Date, nullable=False)
    consumption_kwh = db.Column(db.Numeric(10, 2), default=0)
    amount_due = db.Column(db.Numeric(10, 2), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('room_id', 'month', name='unique_room_month'),)

    # ---------- Create ----------
    @classmethod
    def create(cls, room_id, month, consumption_kwh, amount_due):
        usage = cls(
            room_id=room_id,
            month=month,
            consumption_kwh=consumption_kwh,
            amount_due=amount_due
        )
        db.session.add(usage)
        db.session.commit()
        return usage

    # ---------- Read ----------
    @classmethod
    def get_all(cls):
        data = cls.query.all()
        return {
            item.id: item.to_dict()
            for item in data
        }

    @classmethod
    def get_by_room(cls, room_id):
        data = cls.query.filter_by(room_id=room_id).order_by(cls.month).all()
        return {
            item.id: item.to_dict()
            for item in data
        }

    @classmethod
    def get_by_room(cls, room_id):
        return cls.query.filter_by(room_id=room_id).order_by(cls.month).all()

    @classmethod
    def get_by_month(cls, month):
        return cls.query.filter_by(month=month).all()

    @classmethod
    def get_by_room_and_month(cls, room_id, month):
        return cls.query.filter_by(room_id=room_id, month=month).first()

    # ---------- Update ----------
    def update_consumption(self, consumption_kwh):
        self.consumption_kwh = consumption_kwh
        db.session.commit()

    def update_amount_due(self, amount_due):
        self.amount_due = amount_due
        db.session.commit()

    # ---------- Delete ----------
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # ---------- Serialization ----------
    def to_dict(self):
        return {
            "id": self.id,
            "room_id": self.room_id,
            "month": self.month.isoformat() if self.month else None,
            "consumption_kwh": float(self.consumption_kwh),
            "amount_due": float(self.amount_due),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
