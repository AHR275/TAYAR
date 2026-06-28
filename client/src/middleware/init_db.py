from src.models import User, Room, Transaction, AdminLog, ElectricityUsage
from datetime import date, timedelta
from src.middleware.db import db
from sqlalchemy import create_engine, text
import random
from faker import Faker
from decimal import Decimal


fake = Faker()

def create_database():
    engine = create_engine(
        "mysql+pymysql://root:@localhost"
    )

    with engine.connect() as conn:
        conn.execute(
            text("CREATE DATABASE IF NOT EXISTS tayar")
        )
        conn.commit()

def seed_db():
    print("🌱 Checking seed data...")
    
    # Check if data already exists
    if User.query.count() > 0 or Room.query.count() > 0:
        print("⚠️ Database already has data, skipping seed...")
        return

    # --------------------------
    # 1. Seed Rooms (6 buildings, 30 rooms)
    # --------------------------
    print("🏢 Seeding rooms...")
    
    buildings = {
        "Building A": ["A101", "A102", "A103", "A104", "A105"],
        "Building B": ["B201", "B202", "B203", "B204", "B205"],
        "Building C": ["C301", "C302", "C303", "C304", "C305"],
        "Building D": ["D401", "D402", "D403", "D404", "D405"],
        "Building E": ["E501", "E502", "E503", "E504", "E505"],
        "Building F": ["F601", "F602", "F603", "F604", "F605"],
    }
    
    rooms_map = {}
    for building, room_numbers in buildings.items():
        for room_number in room_numbers:
            # Random initial balance between 50-500
            initial_balance = round(random.uniform(50, 500), 2)
            room = Room.create(
                room_number=room_number,
                building=building,
                current_balance=initial_balance
            )
            rooms_map[room_number] = room
    
    print(f"✅ Created {len(rooms_map)} rooms across 6 buildings")

    # --------------------------
    # 2. Seed Users (40 users + 3 admins)
    # --------------------------
    print("👤 Seeding users...")
    
    # Create 3 admins
    admin_names = ["Admin_System", "Admin_Finance", "Admin_Operations"]
    admins = []
    for i, name in enumerate(admin_names):
        admin = User.create(
            username=name,
            email=f"admin{i+1}@tayar.com",
            password="admin123",
            room_id=random.choice(list(rooms_map.values())).id,
            is_admin=True
        )
        admins.append(admin)
    
    # Create 40 regular users
    room_list = list(rooms_map.values())
    for i in range(40):
        # Random room assignment (some rooms might have multiple users)
        room = random.choice(room_list)
        username = fake.user_name()
        email = fake.email()
        
        # Create user with random balance top-up
        User.create(
            username=username,
            email=email,
            password="user123",
            room_id=room.id,
            is_admin=False
        )
    
    print(f"✅ Created 3 admins and 40 regular users")

    # --------------------------
    # 3. Seed Transactions (300 transactions)
    # --------------------------
    print("💰 Seeding transactions...")
    
    users = User.query.all()
    transaction_types = ["topup", "payment", "refund"]
    statuses = ["completed", "pending", "failed"]
    
    for i in range(300):
        user = random.choice(users)
        amount = round(random.uniform(10, 500), 2)
        trans_type = random.choice(transaction_types)
        status = random.choice(statuses)
        description = fake.sentence()
        
        Transaction.create(
            user_id=user.id,
            amount=amount,
            transaction_type=trans_type,
            status=status,
            description=description
        )
    
    print("✅ Created 300 transactions")

    # --------------------------
    # 4. Seed Admin Logs (more comprehensive)
    # --------------------------
    print("📋 Seeding admin logs...")
    
    admin_actions = [
        "CREATE_USER", "DELETE_USER", "UPDATE_USER", 
        "CREATE_ROOM", "DELETE_ROOM", "UPDATE_ROOM",
        "CREATE_TRANSACTION", "UPDATE_TRANSACTION", "DELETE_TRANSACTION",
        "CREATE_ADMIN", "DELETE_ADMIN", "UPDATE_ADMIN",
        "UPDATE_SETTINGS", "GENERATE_REPORT", "EXPORT_DATA",
        "SYSTEM_MAINTENANCE", "USER_VERIFICATION", "ACCOUNT_SUSPENSION"
    ]
    
    for i in range(50):
        admin = random.choice(admins)
        action = random.choice(admin_actions)
        details = f"{action} performed by {admin.username} - {fake.sentence()}"
        
        AdminLog.create(
            admin_id=admin.id,
            action=action,
            details=details
        )
    
    print("✅ Created 50 admin logs")

    # --------------------------
    # 5. Seed Electricity Usage (2000 records)
    # --------------------------
    print("⚡ Seeding electricity usage...")
    
    # Generate usage for the past 3 months (90 days)
    end_date = date(2026, 6, 28)
    start_date = end_date - timedelta(days=90)
    
    record_count = 0
    for room in rooms_map.values():
        # Generate 15-25 usage records per room (average ~20)
        num_records = random.randint(15, 25)
        
        for _ in range(num_records):
            # Random date within the 90-day window
            random_days = random.randint(0, 89)
            usage_date = start_date + timedelta(days=random_days)
            
            # Generate realistic consumption values
            # Base consumption depends on room size/building
            base_consumption = 30 + (room.id % 10) * 10  # 30-120 kWh base
            
            # Add random variation
            variation = random.uniform(-20, 30)
            consumption = max(10, round(base_consumption + variation, 1))
            
            # Seasonality adjustment (summer months have higher usage)
            month = usage_date.month
            if month in [6, 7, 8, 9]:  # Summer
                consumption *= random.uniform(1.1, 1.4)
            elif month in [12, 1, 2]:  # Winter
                consumption *= random.uniform(1.05, 1.2)
            
            consumption = round(consumption, 1)
            
            # Calculate amount due (rate: $0.15 - $0.35 per kWh)
            rate = round(random.uniform(0.15, 0.35), 3)
            amount_due = round(consumption * rate, 2)
            
            ElectricityUsage.create(
                room_id=room.id,
                month=usage_date,
                consumption_kwh=consumption,
                amount_due=amount_due
            )
            record_count += 1
            
            # Stop if we've reached 2000 records
            if record_count >= 2000:
                break
        
        if record_count >= 2000:
            break
    
    print(f"✅ Created {record_count} electricity usage records")

    # --------------------------
# 6. Additional: Update room balances based on usage and payments
# --------------------------
    print("🔄 Updating room balances based on usage...")


    for room in rooms_map.values():
        # Get total usage amount for this room
        total_usage = db.session.query(
            db.func.sum(ElectricityUsage.amount_due)
        ).filter(ElectricityUsage.room_id == room.id).scalar()
        
        # Handle None/null case
        if total_usage is None:
            total_usage = Decimal('0')
        
        # Convert total_usage to float for multiplication
        total_usage_float = float(total_usage)
        
        # Simulate payments (rooms pay between 60-100% of their usage)
        # This represents how much they've actually paid
        paid_amount = total_usage_float * random.uniform(0.6, 1.0)
        
        # Calculate new balance: initial balance + payments - total usage
        # Note: room.current_balance is the initial balance before usage
        initial_balance_float = float(room.current_balance)
        new_balance = initial_balance_float + paid_amount - total_usage_float
        
        # Ensure balance doesn't go below 0 (can't have negative balance)
        if new_balance < 0:
            new_balance = 0
        
        # Assign back (SQLAlchemy will handle the conversion to Decimal)
        room.current_balance = round(new_balance, 2)

    db.session.commit()
    # --------------------------
    # 7. Summary
    # --------------------------
    print("\n📊 Database Seed Summary:")
    print(f"  • Rooms: {Room.query.count()}")
    print(f"  • Users: {User.query.count()} (including {len(admins)} admins)")
    print(f"  • Transactions: {Transaction.query.count()}")
    print(f"  • Admin Logs: {AdminLog.query.count()}")
    print(f"  • Electricity Usage: {ElectricityUsage.query.count()}")
    print("🎉 Seeding complete!")