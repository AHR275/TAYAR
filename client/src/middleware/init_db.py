from src.models import  User, Room, Transaction, AdminLog, ElectricityUsage
from datetime import date , timedelta
from src.middleware.db import db 
from sqlalchemy import create_engine, text


def create_database():

    engine = create_engine(
        "mysql+pymysql://root:@localhost"
    )

    with engine.connect() as conn:
        conn.execute(
            text("CREATE DATABASE IF NOT EXISTS tayar")
        )
        conn.commit()
# Create a global SQLAlchemy object (similar to your singleton idea)

def seed_db():
    print("🌱 Checking seed data...")

    # --------------------------
    # Seed Rooms
    # --------------------------
 
    # --------------------------
    # Seed Users
    # --------------------------
    if User.query.count() == 0:
        u1 = User.create("admin", "admin@test.com", "123456", room_id=1, is_admin=True)
        u2 = User.create("john", "john@test.com", "123456", room_id=2)
        u3 = User.create("sara", "sara@test.com", "123456", room_id=3)
        print("✅ Users seeded")

    # --------------------------
    # Seed Transactions
    # --------------------------
    if Transaction.query.count() == 0:
        Transaction.create(1, 20, "topup", "success", "Initial topup")
        Transaction.create(2, 15, "payment", "pending", "Electricity bill")
        Transaction.create(3, 50, "topup", "success", "Wallet recharge")
        print("✅ Transactions seeded")

    # --------------------------
    # Seed Admin Logs
    # --------------------------
    if AdminLog.query.count() == 0:
        AdminLog.create(1, "CREATE_USER", "Created initial admin + users")
        print("✅ Admin logs seeded")

    # --------------------------
    # Seed Electricity Usage
    # --------------------------
  

    


    print("⚡ Seeding electricity usage...")

    if ElectricityUsage.query.count() > 0:
        print("⚡ Electricity usage already exists, skipping...")
        return

    # --------------------------
    # Build structure
    # --------------------------
    buildings = {
        "Building A": ["A101", "A102", "A103"],
        "Building B": ["B201", "B202", "B203"],
        "Building C": ["C301", "C302", "C303"],
    }

    # --------------------------
    # Ensure rooms exist (3 per building)
    # --------------------------
    rooms_map = {}

    for building, room_numbers in buildings.items():
        for room_number in room_numbers:
            room = Room.query.filter_by(room_number=room_number).first()

            if not room:
                room = Room.create(
                    room_number=room_number,
                    building=building,
                    current_balance=100.00
                )

            rooms_map[room_number] = room

    # --------------------------
    # Generate 2 weeks of usage per room
    # --------------------------
    start_date = date(2026, 6, 1)

    for room_number, room in rooms_map.items():

        for week in range(2):  # 2 weeks
            usage_date = start_date + timedelta(weeks=week)

            # realistic fake values
            base = 50 + (room.id * 5)
            consumption = base + (week * 10)
            amount_due = round(consumption * 0.25, 2)

            ElectricityUsage.create(
                room_id=room.id,
                month=usage_date,
                consumption_kwh=consumption,
                amount_due=amount_due
            )

    print("✅ Electricity usage seeded (2 weeks per room)")
    print("🎉 Seeding complete")