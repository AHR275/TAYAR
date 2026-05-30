import json
import threading
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "../data"
USERS_FILE = DATA_DIR/"users.json"
ROOMS_FILE = DATA_DIR/"rooms.json"
TRANS_FILE = DATA_DIR/"transactions.json"
_lock = threading.Lock()


def read_data(file:Path):
    """Read the entire data.json"""
    

    with _lock:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)


def write_data(data,file:Path):
    """Write the entire data.json"""
    with _lock:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)


# ---- Helper methods for convenience ---- #

# USERS
class UsersData:
    def get_users(self):
        return read_data(USERS_FILE)['users']


    def get_user(self,user_id):
        return next((u for u in self.get_users() if u["id"] == user_id), None)


    def add_user(self,user):
        data = read_data(USERS_FILE)['users']
        data.append(user)
        write_data(data,USERS_FILE)


# ROOMS
class RoomsData: 
    def get_rooms(self):
        return read_data(ROOMS_FILE)["buildings"]


    def get_room(self,room_id):
        for building in self.get_rooms():
            for room in building["rooms"]:
                if room["id"] == room_id:
                    return room
        return None


# TRANSACTIONS
class TransData:
    def get_transactions(self):
        return read_data(TRANS_FILE)["transactions"]


    def get_transaction(self,tx_id):
        return next((t for t in self.get_transactions() if t["id"] == tx_id), None)


    def add_transaction(self,transaction):
        data = read_data(TRANS_FILE)["transactions"]
        data.append(transaction)
        write_data(data,TRANS_FILE)


# UTILITY







 