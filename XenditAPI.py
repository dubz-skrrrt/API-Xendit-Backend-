import os
import time
import json
from os import path
from json import  JSONEncoder
import xendit
from flask import Flask, request, render_template, jsonify
from xendit import Xendit, XenditError, BalanceAccountType
import xendit

app = Flask(__name__)
payment_List = []
my_path = 'file.json'
class paymentEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

@app.route('/')
def index():
    print(f"credit-num-{int(time.time())}", )
    return render_template('index.html')
@app.route('/pay', methods = ['POST'])
def checker():
    api_key = "xnd_development_Qlza74hRWMGa4odmMKPAYsH51zryFsnokmHyHEBLrhpuZ4P0J2C3uTCVtgEN"
    xendit_instance = Xendit(api_key=api_key)
    CreditCard = xendit_instance.CreditCard
    cardNumber = request.form.get("number")
    expDate = request.form.get("exp_date")
    amount = request.form.get("amount")
    cvn = request.form.get("CVN")
    charge = CreditCard.create_charge(
        token_id="5f0410898bcf7a001a00879d",
        external_id="card_charge-1594106478",
        amount=75000,
        card_cvn="123",
    )
    print(charge)

    args = {
        "token_id": '62451a02ceeb1e001c27ef20' ,
        "external_id": f"card_preAuth-{int(time.time())}",
        "amount": amount,
        "card_cvn": cvn,
    }
    try:
        creditPayment = xendit_instance.CreditCard.create_authorization(**args)
        persistentList(vars(creditPayment))
        print (payment_List)
        return vars(creditPayment)
    except XenditError as e:
        print(e)
        return vars(e)

@app.route('/refund')
def showpayment():
    readList()
    return jsonify(payment_List)

def readList():
    if path.exists(my_path):
        with open(my_path, 'r') as f:
            prev_json = json.load(f)
            global payment_List
            payment_List += prev_json


print(payment_List)
def persistentList(payment):
    payment_List.append(payment)

    with open(my_path, 'w') as f:
        json.dump(payment_List, f, indent=2, cls=paymentEncoder)

if __name__ == '__main__':
    app.run(debug=True)
