import os
import time

from flask import Flask, request, render_template, jsonify
from xendit import Xendit, XenditError, BalanceAccountType

app = Flask(__name__)
payment = [
    {
        'payment1': "CreditCard",
        # 'credit card number': int(input()),
        # 'exp date': int(input()),
        # 'cvn': int (input())
    }
]
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/pay', methods = ['POST'])
def pay():
    cardNumber = request.form.get("number")
    expDate = request.form.get("exp_date")
    amount = request.form.get("amount")
    args = {
        "token_id": "12qwe345rftsdf35",
        "external_id": f"credit-num-{int(time.time())}",
        "amount": amount,
    }
    api_key = "xnd_development_Qlza74hRWMGa4odmMKPAYsH51zryFsnokmHyHEBLrhpuZ4P0J2C3uTCVtgEN"
    xendit_instance = Xendit(api_key=api_key)
    try:
        creditPayment = xendit_instance.CreditCard.create_authorization(**args)
        return vars(creditPayment)
    except XenditError as e:
        return vars(e)
@app.route('/app/api/payment/all')
def showpayment():
    return jsonify(payment)

if __name__ == '__main__':
    app.run(debug=True)


#
#
# Balance = xendit_instance.Balance
# CreditCard = xendit_instance.CreditCard
# balance = Balance.get(
#     account_type=BalanceAccountType.CASH,
# )
# charge = CreditCard.create_authorization(
#     token_id="5f0410898bcf7a001a00879d",
#     external_id="card_preAuth-1594106356",
#     amount=75000,
#     card_cvn="123",
# )
#print(balance)
#print(charge)