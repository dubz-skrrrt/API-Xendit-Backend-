import os
import time
import json
from os import path
from json import  JSONEncoder
import requests
import xendit
from print_running_function import print_running_function
from flask import Flask, request, render_template, jsonify
from xendit import Xendit, XenditError, BalanceAccountType
import xendit

app = Flask(__name__)
payment_List = []

api_key = "xnd_development_Qlza74hRWMGa4odmMKPAYsH51zryFsnokmHyHEBLrhpuZ4P0J2C3uTCVtgEN"
xendit_instance = Xendit(api_key=api_key)

my_path = 'file.json'
class paymentEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class createPage:
    @app.route('/')
    def check():
        req = requests.get('https://api.xendit.co/')
        print(req.content)
        data = req.content
        return render_template(credit_card_payment())

class CreateAuthorization:
        # return render_template('index.html', data=data)
    @app.route('/pay', methods = ['POST', 'GET'])
    def authorize():
        authID = request.form.get("auth_id") #Get the data from input field
        amount = request.form.get("amount")  #Get the data from input field
        ext_id = f"card_preAuth-{int(time.time())}"
        cvn = request.form.get("CVN")        #Get the data from input field
        CreditCard = xendit_instance.CreditCard
        args = {
            "token_id": '62468d330313fe001bb00610' ,
            "external_id": ext_id,
            "amount": amount,
            "card_cvn": cvn,
            "authentication_id": authID
        }
        try:
            creditPayment = xendit_instance.CreditCard.create_authorization(**args)
            persistentList(vars(creditPayment))
            print_running_function("xendit_instance.CreditCard.create_authorization", args)
            return vars(creditPayment)
        except XenditError as e:
            print(e)
            return vars(e)

class CreateCharge:
    @app.route('/charge', methods = ['POST', 'GET'])
    def charge():
        authID = request.form.get("auth_id")
        amount = request.form.get("amount")
        ext_id = f"card_preAuth-{int(time.time())}"
        charge = xendit_instance.CreditCard
        args = {
            "token_id": '62468d330313fe001bb00610',
            "external_id": ext_id,
            "amount": amount,
            "card_cvn": '123',
            "authentication_id": authID
        }
        try:
            charge = xendit_instance.CreditCard.create_charge(**args)
            print_running_function("xendit_instance.CreditCard.create_charge", args)
            print(charge.capture_amount)
            return vars(charge)
        except XenditError as e:
            print(e)
            return vars(e)

class CreateRefund:
    @app.route('/refund', methods = ['POST', 'GET'])
    def showpayment():
        readList()
        CreditCard = xendit_instance.CreditCard
        credit_card_id = request.form.get("refund_ID")
        amount = request.form.get("amount")
            # input("Please input your credit card charge id: ")
        refund = CreditCard.create_refund(
            credit_card_charge_id= credit_card_id,
            amount=amount,
            external_id=f"card_refund-{int(time.time())}",
        )
        print_running_function("xendit_instance.CreditCard.create_refund", args)
        return jsonify(vars(refund))

def readList():
    if path.exists(my_path):
        with open(my_path, 'r') as f:
            prev_json = json.load(f)
            global payment_List
            payment_List += prev_json

def persistentList(payment):
    # Maybe can create a clickable table with this list
    payment_List.append(payment)
    with open(my_path, 'w') as f:
        json.dump(payment_List, f, indent=2, cls=paymentEncoder)

def ask_credit_card_input():
    print("Input the action that you want to use")
    print("0. Exit")
    print("1. Create Authorization")
    print("2. Create Charge")
    print("3. Create Refund")
    try:
        return int(input())
    except ValueError:
        print("Invalid input. Please type a number")
        return ask_credit_card_input()

def credit_card_payment():

    credit_card_input = ask_credit_card_input()
    print(credit_card_input)
    while credit_card_input != 0:
        if credit_card_input == 1:
            print("Running Create Authorization Test")
            return 'index.html'
        elif credit_card_input == 2:
            print("Running Create Charge Test")
            return 'charge.html'
        elif credit_card_input == 3:
            print("Running Create Refund Test")
            return 'refund.html'
        credit_card_input = ask_credit_card_input()
if __name__ == '__main__':
    app.run(debug=True)
