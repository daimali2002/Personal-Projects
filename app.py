from flask import Flask, render_template, send_from_directory, redirect, url_for
from UserClass import *
from ProdClass import *
from OrderClass import *
from transaction import *

app = Flask(__name__)
userObject = UserAuthApp()
productsObject = ProdApp()
transobj = transactions()

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/login", methods=['POST'])
def loginCaller():
    return userObject.login()

@app.route("/dashboard", methods=['GET'])
def Dashboard():
    return productsObject.dashboard()

@app.route("/product-details", methods=['GET'])
def prod_one():
    return productsObject.one_prod()

@app.route("/signup", methods = ["POST"])
def signupCaller():
    return userObject.signup()

@app.route("/forgot-password", methods=['POST'])
def forgotPasswordCaller1():
    return userObject.forgot_password()

@app.route("/forgot-password-page", methods=['GET'])
def forgotPasswordCaller2():
    return userObject.forgot_password_page()

@app.route("/reset-password-page", methods=['GET'])
def forgotPasswordCaller3():
    return userObject.reset_password_page()

@app.route("/reset-password", methods=['POST'])
def resetPasswordCaller():
    return userObject.reset_password_api()

@app.route("/getall", methods=['GET'])
def fetchAllProductsCaller():
    return productsObject.getall()

@app.route("/getone", methods=['GET'])
def fetchOneProductCaller():
    return productsObject.getone()

@app.route("/insertProd", methods=['POST'])
def insertProductCaller():
    return productsObject.insertProd()

@app.route("/updatevals", methods=['PATCH'])
def updateProductCaller():
    return productsObject.updatevals()

@app.route("/deleteprod", methods=['DELETE'])
def deleteProductCaller():
    return productsObject.deleteprod()

@app.route("/buy", methods = ["POST"])
def buycaller():
    return OrderApp.buy()

@app.route("/cart", methods = ["GET"])
def Cart():
    return OrderApp.cart()

@app.route("/checkout", methods = ["GET"])
def checkout():
    return OrderApp.checkout()

@app.route("/order-details", methods = ["GET"])
def ord():
    return render_template("order-details.html")

@app.route("/user-address", methods = ["GET"])
def gettt():
    return userObject.get_address()

@app.route('/send-order-email', methods=['POST'])
def send_order_email():
    data = request.get_json()
    receiver = data.get('receiver')
    order_details = data.get('order_details')
    send_order_details(receiver, order_details)
    return jsonify({'status': 'Email sent successfully'}), 200

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.form.to_dict()
        response = transobj.initiate_payment(data.get("PaRes"),None)
        print(response)
        if response.get("code") == "00":
            return render_template("order-details.html")
        else:
            error_message = response.get("message", "Unknown error")
            return render_template('failure_page.html', error=error_message)
    except Exception as e:
        return jsonify({'status': f'failure {e}'}), 500
    
@app.route('/webhook2', methods=['GET'])
def webhook2():
    try:
        otp = request.args.get('otp')        
        response = transobj.initiate_payment(None,otp)
        print(response)
        if response.get("code") == "00":
            return render_template("order-details.html")
        else:
            error_message = response.get("message", "Unknown error")
            return render_template('failure_page.html', error=error_message)
    except:
        return jsonify({'status': 'failure'}), 500
       
@app.route("/make-payment", methods = ["GET"])
def make_pay():
    return render_template("make-payment.html")

@app.route("/otp", methods = ["GET"])
def otp():
    transobj.basket_id = request.args.get('basket_id')
    transobj.txnamt = request.args.get('txnamt')
    transobj.order_date = request.args.get('order_date')
    transobj.customer_mobile_no = request.args.get('customer_mobile_no')
    transobj.customer_email_address = request.args.get('customer_email_address')
    transobj.account_type_id = request.args.get('account_type_id')
    transobj.currency_code = request.args.get('currency_code')
    transobj.bank_code = request.args.get('bank_code')
    transobj.account_number = request.args.get('account_number')
    transobj.cnic = request.args.get('cnic')
    transobj.card_number = request.args.get('card_number')
    transobj.expiry_month = request.args.get('expiry_month')
    transobj.expiry_year = request.args.get('expiry_year')
    transobj.cvv = request.args.get('cvv')
    transobj.gettoken()
    return transobj.customervalidate()

@app.route("/get-otp", methods = ["GET"])
def get_otp():
    return render_template("get-otp.html")

@app.route('/failure_page')
def failure_page():
    error = request.args.get('error', 'Unknown error')
    return render_template('failure_page.html', error=error)

if __name__ == "__main__":
    app.run(debug=True)
