import requests
from flask import render_template, jsonify, Response
import traceback

class transactions:

    def __init__(self) -> None:
        self.token = None
        self.transaction_id = None
        self.data_3ds_secureid = None
        self.basket_id = None
        self.txnamt = None
        self.order_date =None
        self.customer_mobile_no = None
        self.customer_email_address = None
        self.account_type_id = None
        self.currency_code = None
        self.bank_code = None
        self.account_number = None
        self.cnic = None
        self.card_number = None
        self.expiry_month = None
        self.expiry_year = None
        self.cvv = None

    def gettoken(self):
        url = "https://apipxyuat.apps.net.pk:8443/api/token"
        payload  = {
            'merchant_id': '102',
            'secured_key': 'zWHjBp2AlttNu1sK',
            'grant_type': 'client_credentials'
        }
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        response_data = response.json() 
        token = response_data["token"] 
        self.token = token
    
    def customervalidate(self):

        url = "https://apipxyuat.apps.net.pk:8443/api/customer/validate"

        payload  = {
            'basket_id': self.basket_id,
            'txnamt': self.txnamt,
            'order_date': self.order_date,
            'customer_mobile_no': self.customer_mobile_no, #from user/db
            'customer_email_address': self.customer_email_address,
            'account_type_id': self.account_type_id, 
            'card_number': self.card_number,# from user
            'expiry_month': self.expiry_month,# from user
            'expiry_year': self.expiry_year,# from user
            'cvv': self.cvv,# from user
            'data_3ds_callback_url': 'http://127.0.0.1:5000/webhook',# where to redirect upon sucsess
            'currency_code': 'PKR', #hard coded to pkr
            'bank_code': self.bank_code,
            'account_number':self.account_number,
            'cnic_number':self.cnic 
        }
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': "Bearer " + self.token
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()
        self.transaction_id = response.get("transaction_id")
        self.data_3ds_secureid = response.get("data_3ds_secureid")
        print(response)
        if response.get("code") == '00':
            return jsonify({"code": "00", "result" :response.get("data_3ds_html")})
        else:
            return jsonify({"code": response.get("code"), "error": response.get("message")})
        
    def initiate_payment(self,payres,otp):
        try:
            url = "https://apipxyuat.apps.net.pk:8443/api/transaction"

            payload = {
                    'data_3ds_pares': payres,
                    'transaction_id': self.transaction_id, # form 3.10
                    'data_3ds_secureid': self.data_3ds_secureid,# from 3.10
                    'basket_id': self.basket_id,
                    'txnamt': self.txnamt,
                    'order_date': self.order_date,
                    'customer_mobile_no': self.customer_mobile_no, #from user/db
                    'customer_email_address': self.customer_email_address,
                    'account_type_id': self.account_type_id, 
                    'card_number': self.card_number,# from user
                    'expiry_month': self.expiry_month,# from user
                    'expiry_year': self.expiry_year,# from user
                    'cvv': self.cvv,# from user
                    'currency_code': 'PKR', #hard coded to pkr
                    'bank_code': self.bank_code,
                    'account_number':self.account_number,
                    'cnic_number':self.cnic,
                    'otp' : otp

                }
            headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': 'Bearer ' + self.token
                    }
            response = requests.request("POST", url, headers=headers, data=payload).json()
            return response
        except Exception as e:
            error_message = traceback.format_exc()
            return jsonify({"error": "something went wrong " + error_message}),500





