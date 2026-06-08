import json
import threading
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "../data"
USERS_FILE = DATA_DIR / "users.json"
ROOMS_FILE = DATA_DIR / "rooms.json"
TRANS_FILE = DATA_DIR / "transactions.json"
_lock = threading.Lock()


def read_data(file: Path):
    """Read the entire data.json"""
    with _lock:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)


def write_data(data, file: Path):
    """Write the entire data.json"""
    with _lock:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)


# ---- Helper methods for convenience ---- #

# USERS
class UsersData:
    def get_users(self):
        """Get all users"""
        data = read_data(USERS_FILE)
        if isinstance(data, list):
            return data
        return data.get("users", [])

    def get_user(self, user_id):
        return next((u for u in self.get_users() if u.get("id") == user_id), None)

    def add_user(self, user):
        """Add a new user"""
        full_data = read_data(USERS_FILE)
        
        # Handle old format (list)
        if isinstance(full_data, list):
            full_data = {"users": full_data}
        
        # Ensure users key exists
        if "users" not in full_data:
            full_data["users"] = []
        
        full_data["users"].append(user)
        write_data(full_data, USERS_FILE)


# ROOMS
class RoomsData:
    def get_rooms(self):
        """Get all buildings with rooms"""
        data = read_data(ROOMS_FILE)
        if isinstance(data, list):
            return data
        return data.get("buildings", [])

    def get_room(self, room_number):
        """Get a room by room number"""
        for building in self.get_rooms():
            for room in building.get("rooms", []):
                if str(room.get("room_number")) == str(room_number):
                    return room
        return None
    
    def add_building(self, building):
        """Add a new building"""
        full_data = read_data(ROOMS_FILE)
        
        if isinstance(full_data, list):
            full_data = {"buildings": full_data}
        
        if "buildings" not in full_data:
            full_data["buildings"] = []
        
        full_data["buildings"].append(building)
        write_data(full_data, ROOMS_FILE)
    
    def add_room(self, room_number, building_name):
        """Add a room to a building"""
        full_data = read_data(ROOMS_FILE)
        
        if isinstance(full_data, list):
            full_data = {"buildings": full_data}
        
        for building in full_data.get("buildings", []):
            if building.get("name") == building_name:
                if "rooms" not in building:
                    building["rooms"] = []
                building["rooms"].append({"room_number": room_number})
                break
        
        write_data(full_data, ROOMS_FILE)


# TRANSACTIONS
class TransData:
    def get_transactions(self):
        """Get all transactions"""
        data = read_data(TRANS_FILE)
        if isinstance(data, list):
            return data
        return data.get("transactions", [])

    def get_transaction(self, tx_id):
        """Get a single transaction by ID"""
        transactions = self.get_transactions()
        return next((t for t in transactions if t.get("id") == tx_id), None)

    def add_transaction(self, transaction):
        """Add a new transaction"""
        full_data = read_data(TRANS_FILE)
        
        # Handle old format (list)
        if isinstance(full_data, list):
            full_data = {"transactions": full_data}
        
        # Ensure transactions key exists
        if "transactions" not in full_data:
            full_data["transactions"] = []
        
        full_data["transactions"].append(transaction)
        write_data(full_data, TRANS_FILE)