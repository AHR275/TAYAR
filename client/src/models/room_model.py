# src/models.py
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from collections import defaultdict
from src.middleware.db import db



# ============================================
# Room Model
# ============================================

class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(20), unique=True, nullable=False)
    building = db.Column(db.String(100))
    current_balance = db.Column(db.Numeric(10, 2), default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    users = db.relationship(
        'User',
        backref='room',
        lazy='dynamic'
    )
    electricity_usage = db.relationship(
        'ElectricityUsage',
        backref='room',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    # ---------- Create ----------
    @classmethod
    def create(cls, room_number, building, current_balance=0.00):
        room = cls(
            room_number=room_number,
            building=building,
            current_balance=current_balance
        )
        db.session.add(room)
        db.session.commit()
        return room

    # ---------- Read ----------
   # ---------- READ (FIXED) ----------

    @classmethod
    def get_all(cls):
        rooms = cls.query.all()
        return {
            room.id: room.to_dict()
            for room in rooms
        }

    @classmethod
    def get_by_id(cls, room_id):
        room = cls.query.get(room_id)
        return {"room": room.to_dict() if room else None}

    @classmethod
    def get_by_room_number(cls, room_number):
        room = cls.query.filter_by(room_number=room_number).first()
        return {"room": room.to_dict() if room else None}

    @classmethod
    def get_by_building(cls, building):
        rooms = cls.query.filter_by(building=building).all()
        return {
            room.id: room.to_dict()
            for room in rooms
        }
    
    @classmethod
    def get_by_buildings(cls):
        rooms = cls.query.all()

        grouped = defaultdict(dict)

        for room in rooms:
            grouped[room.building][room.id] = room.to_dict()

        return {
            "buildings": {
                building: {
                    "rooms": rooms_dict
                }
                for building, rooms_dict in grouped.items()
            }
        }
    # ---------- Update ----------
    def update_balance(self, amount):
        self.current_balance = float(self.current_balance) + amount
        db.session.commit()
        return self.current_balance

    def set_balance(self, new_balance):
        self.current_balance = new_balance
        db.session.commit()

    def update_room_number(self, room_number):
        self.room_number = room_number
        db.session.commit()

    def update_building(self, building):
        self.building = building
        db.session.commit()

    # ---------- Delete ----------
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # ---------- Relationships ----------
    def get_users(self):
        return self.users.all()

    def get_electricity_usage(self):
        return self.electricity_usage.all()

    # ---------- Serialization ----------
    def to_dict(self):
        return {
            "id": self.id,
            "room_number": self.room_number,
            "building": self.building,
            "current_balance": float(self.current_balance),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
