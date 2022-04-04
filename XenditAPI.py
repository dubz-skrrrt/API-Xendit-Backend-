import os
import time
import json
from os import path
from json import  JSONEncoder

import requests
import xendit
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

class CreateAuthorization:
    @app.route('/')
    def index():
        ask_credit_card_input()
        return render_template('index.html')
    @app.route('/pay', methods = ['POST', 'GET'])
    def authorize():
        authID = request.form.get("auth_id")
        amount = request.form.get("amount")
        ext_id = f"card_preAuth-{int(time.time())}"
        cvn = request.form.get("CVN")
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
            print (payment_List)
            return vars(creditPayment)
        except XenditError as e:
            print(e)
            return vars(e)

class CreateCharge:
    @app.route('/')
    @app.route('/charge')
    def charge():
        authID = request.form.get("auth_id")
        amount = request.form.get("amount")
        ext_id = f"card_preAuth-{int(time.time())}"
        cvn = request.form.get("CVN")
        charge = xendit_instance.CreditCard
        args = {
            "token_id": '62468d330313fe001bb00610',
            "external_id": ext_id,
            "amount": amount,
            "card_cvn": cvn,
            "authentication_id": authID
        }
        try:
            charge = xendit_instance.CreditCard.create_charge(**args)
            return vars(charge, "Charge Successfully Created.")
        except XenditError as e:
            print(e)
            return vars(e)

class CreateRefund:
    @app.route('/')
    @app.route('/refund')
    def showpayment():
        readList()
        CreditCard = xendit_instance.CreditCard
        credit_card_id = input("Please input your credit card charge id: ")
        refund = CreditCard.create_refund(
            credit_card_charge_id= credit_card_id,
            amount=2000,
            external_id=f"card_refund-{int(time.time())}",
        )
        return jsonify(vars(refund, "Refund successfully requested"))

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
    while credit_card_input != 0:
        if credit_card_input == 1:
            print("Running Create Authorization Test")
            CreateAuthorization.authorize()
        elif credit_card_input == 2:
            print("Running Create Charge Test")

        elif credit_card_input == 3:
            print("Running Create Refund Test")
        credit_card_input = ask_credit_card_input()

if __name__ == '__main__':
    app.run(debug=True)
