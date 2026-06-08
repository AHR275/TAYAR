# src/models.py
from src.middleware.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# ============================================
# AdminLog Model
# ============================================

class AdminLog(db.Model):
    __tablename__ = "admin_logs"

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ---------- Create ----------
    @classmethod
    def create(cls, admin_id, action, details=None):
        log = cls(
            admin_id=admin_id,
            action=action,
            details=details
        )
        db.session.add(log)
        db.session.commit()
        return log

    # ---------- Serialization ----------
    def to_dict(self):
        return {
            "id": self.id,
            "admin_id": self.admin_id,
            "action": self.action,
            "details": self.details,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    # ---------- Read (DICT STYLE) ----------

   
    @classmethod
    def get_all(cls):
        logs = cls.query.order_by(cls.created_at.desc()).all()
        return {
            log.id: log.to_dict()
            for log in logs
        }

    @classmethod
    def get_by_id(cls, log_id):
        log = cls.query.get(log_id)

        return {
            "log": log.to_dict() if log else None
        }

    @classmethod
    def get_by_admin(cls, admin_id):
        logs = cls.query.filter_by(admin_id=admin_id)\
                        .order_by(cls.created_at.desc())\
                        .all()

        return {
            "logs": {
                log.id: log.to_dict()
                for log in logs
            }
        }

    @classmethod
    def get_by_action(cls, action):
        logs = cls.query.filter_by(action=action)\
                        .order_by(cls.created_at.desc())\
                        .all()

        return {
            "logs": {
                log.id: log.to_dict()
                for log in logs
            }
        }

    # ---------- Delete ----------
    def delete(self):
        db.session.delete(self)
        db.session.commit()