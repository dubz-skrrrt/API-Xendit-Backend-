import os
import time

import xendit
from flask import Flask, request, render_template, jsonify
from xendit import Xendit, XenditError, BalanceAccountType
import xendit
app = Flask(__name__)
# payment = [
#     {
#         'payment1': "CreditCard",
#     }
# ]
@app.route('/')
def index():
    print(f"credit-num-{int(time.time())}", )
    return render_template('index.html')
@app.route('/pay', methods = ['POST'])

def checker():
    api_key = "xnd_development_Qlza74hRWMGa4odmMKPAYsH51zryFsnokmHyHEBLrhpuZ4P0J2C3uTCVtgEN"
    xendit_instance = Xendit(api_key=api_key)
    cardNumber = request.form.get("number")
    expDate = request.form.get("exp_date")
    amount = request.form.get("amount")
    cvn = request.form.get("CVN")

    args = {
        "token_id": '6244121e798b79001c76ac50' ,
        "external_id": f"card_preAuth-{int(time.time())}",
        "amount": amount,
        "card_cvn": cvn,
    }
    try:
        creditPayment = xendit_instance.CreditCard.create_authorization(**args)
        print(creditPayment)
        return vars(creditPayment)
    except XenditError as e:
        print(e)
        return vars(e)
# @app.route('/app/api/payment/all')
# def showpayment():
#     return jsonify(payment)

if __name__ == '__main__':
    app.run(debug=True)
