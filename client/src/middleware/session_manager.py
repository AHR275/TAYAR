from flask import session


class SessionManager:

    @staticmethod
    def get_user():
        return session.get("user", {})

    @staticmethod
    def get_user_id():
        return session.get("user", {}).get("id")

    @staticmethod
    def get_username():
        return session.get("user", {}).get("username")

    @staticmethod
    def get_email():
        return session.get("user", {}).get("email")

    @staticmethod
    def is_admin():
        return session.get("user", {}).get("is_admin", False)

    @staticmethod
    def is_authenticated():
        return "user" in session

    @staticmethod
    def logout():
        session.pop("user", None)