from flask import Blueprint, render_template,redirect, url_for 
from flask.views import View , MethodView
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from src.forms.topup_forms import TopupForm


from src.models import Room , User , Transaction 
from src.middleware.session_manager import SessionManager








topup_bp = Blueprint(
    "topup",
    __name__,
    url_prefix="/topup"
)



# @topup_bp.route("/")




class TopupView(MethodView):
    def get(self):
        user = SessionManager.get_user()
        if not user:
            return redirect(url_for("auth.login"))
        user_id = user["id"]
        amounts = [10, 20, 50, 75, 100]
        form = TopupForm()
        
        # Get all buildings
        buildings = Room.get_by_buildings()["buildings"] 
         # assuming this returns list of building names
    
        # Build building choices for WTForms
        buildings_name = list(buildings.keys())
        form.building.choices = [(b,b) for b in buildings_name]  # use building name as value

        # # Default selected building (first one)
        default_building = buildings_name[0]

        # # Get rooms for default building
        rooms = buildings[default_building]["rooms"]
        print("rooms" , rooms)
        form.room.choices = [
            (room["id"], f"Room {room['room_number']}")
            for room in rooms.values()
        ]
        print("choices : ",form.room.choices)

        return render_template(
            "topup.html",
            form=form,
            amounts=amounts,
            buildings=buildings
        )

    def post(self):
        user = SessionManager.get_user()
        if not user:
            return redirect(url_for("auth.login"))
        user_id = user["id"]
        amounts = [10, 20, 50, 75, 100]
        form = TopupForm()
        selected_building = form.building.data
        buildings = Room.get_by_buildings()["buildings"] 
         # assuming this returns list of building names
    
        # Build building choices for WTForms
        buildings_name = list(buildings.keys())
        form.building.choices = [(b,b) for b in buildings_name]  # use building name as value

        # # Default selected building (first one)
        

        # # Get rooms for default building
        rooms = buildings[selected_building]["rooms"]
        print("rooms" , rooms)
        form.room.choices = [
            (room["id"], f"Room {room['room_number']}")
            for room in rooms.values()
        ]


        if form.validate_on_submit():
            room = form.room.data
            amount = form.amount.data

            print("go to payment")
            print("room :" , room, "\n amount : " , amount )
            # print(url_for("payment.payment", room=room, amount=amount))
            return redirect(url_for("payment.payment", room=room, amount=amount))

        return render_template(
            "topup.html",
            form=form,
            amounts=amounts,
            buildings=buildings
        )
    


class TopupHistoryView(View):
    
    
    def dispatch_request(self):
        user = SessionManager.get_user()
        if not user:
            return redirect(url_for("auth.login"))
        user_id = user["id"]
        transactions = Transaction.get_by_user(user_id)

        topups = {
            k: v for k, v in transactions.items()
            if v["type"] == "topup"
        }
        # print(transactions)
        # return "transi : " , transactions
        return render_template(
            "topup_history.html",
            transactions=topups
        )


topup_bp.add_url_rule(
    "/",
    view_func=TopupView.as_view("topup")
)

topup_bp.add_url_rule(
    "/history",
    view_func=TopupHistoryView.as_view("history")
)