from flask import Blueprint, render_template,redirect, url_for 
from flask.views import View , MethodView
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from src.forms.topup_forms import TopupForm
from src.middleware.data_center import TransData

global transactions


td= TransData()
transactions = td.get_transactions()


topup_bp = Blueprint(
    "topup",
    __name__,
    url_prefix="/topup"
)



# @topup_bp.route("/")




class TopupView(MethodView):
    def get(self):

        amounts = [10, 20, 50,75,  100]
        return render_template(
            "topup.html",
            form=TopupForm(),
            amounts=amounts
        )

    def post(self):
        form = TopupForm()
        amounts = [10, 20, 50,75,  100]

        if form.validate_on_submit():

            room = form.room.data
            amount = form.amount.data
           
            

            return redirect(

                url_for("topup.history")
            )

        return render_template(
            "topup.html",
            form=form,
            amounts= amounts
        )

class TopupHistoryView(View):
    
    
    def dispatch_request(self):
        
        # print(transactions)
        # return "transi : " , transactions
        return render_template(
            "topup_history.html",
            transactions=transactions
        )


topup_bp.add_url_rule(
    "/",
    view_func=TopupView.as_view("topup")
)

topup_bp.add_url_rule(
    "/history",
    view_func=TopupHistoryView.as_view("history")
)