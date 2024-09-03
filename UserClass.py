from flask import Flask, render_template, request, jsonify
import bcrypt
from Funcs import *
from myemail import *
import random

class UserAuthApp:
    
    def index(self):
        return render_template('index.html')
    
    def forgot_password_page(self):
        return render_template('forgot_password.html')
    
    def reset_password_page(self):
        return render_template('reset_password.html')

    def login(self):
        try:
            data = request.get_json()
            username = data.get("Username")
            user_pswd = data.get("Password")
            
            if not user_pswd or not username:
                return jsonify({'error': 'Fields cannot be empty'}), 400
            
            hashed_password = extract_data(username)
            
            if hashed_password is None:
                return jsonify({'error': 'Incorrect Username, Email or Phone'}), 400
            elif bcrypt.checkpw(user_pswd.encode('utf-8'), hashed_password.encode('utf-8')):
                return jsonify({'Message': 'Logged In', "UserID": extract_id(username)}), 200
            else:
                return jsonify({'error': 'Incorrect Password'}), 400
        except:
            return jsonify({'error': 'An Unexpected Error Occurred'}), 500

    def signup(self):
        try:
            user = request.get_json()
            
            if not user.get("First") or not user.get("Email") or not user.get("User") or not user.get("Pswd") or not user.get("RePswd") or not user.get("Age") or not user.get("Phone") or  not user.get("Address"):
                return jsonify({'error': 'Fields cannot be empty'}), 400
            if not is_valid_name(user.get("First")):
                return jsonify({'error': 'Incorrect First Name Entered, Must contain only Alphabets and be of appropriate length'}), 400 
            if user.get("Last") and not is_valid_name(user.get("Last")): 
                return jsonify({'error': 'Incorrect Last Name Entered, Must contain only Alphabets and be of appropriate length'}), 400 
            if not is_valid_email(user.get("Email")): 
                return jsonify({'error': 'Incorrect Email, Email must look like user@domain.example'}), 400
            if extract_data(user["Email"]) is not None:
                return jsonify({'error': 'Email Already Exists'}), 400
            if extract_data(user["User"]) is not None:
                return jsonify({'error': 'Username Already Exists'}), 400
            if not is_valid_username(user["User"]):
                return jsonify({'error': 'Incorrect Username, Username must include letters, may have numbers, and be 4-25 characters long.'}), 400
            if not is_password_strong(user["Pswd"]):
                return jsonify({'error': 'Weak Password,Password must have 1 uppercase, 1 lowercase, 1 number, and be 8-25 characters long.'}), 400
            if not user["Pswd"] == user["RePswd"]:
                return jsonify({'error': 'Passwords Do Not Match'}), 400
            if not is_valid_phone(user.get("Phone")):
                return jsonify({'error': 'Incorrect phone number entered. It must be 11 digits long and start with 03'}), 400
            if extract_data(user.get("Phone")) is not None:
                return jsonify({'error': 'Phone Number Already Exists'}), 400
            if not is_valid_age(user.get("Age")):
                return jsonify({'error': 'Incorrect Age, Age must be between 1 and 150'}), 400
            if len(user.get("Address")) < 10:
                return jsonify({'error': 'Incorrect Address, Address must be atleast 10 Characters'}), 400

            add_data(user["First"], user.get("Last"), user.get("Age"), user["User"], user["Pswd"], user["Email"], user["Phone"], user.get("Address"))

            return jsonify({'Message': 'You are Signed Up!',"UserID": extract_id(user["User"])}), 201
        except:
            return jsonify({'error': 'An Unexpected Error Occurred'}), 500
        
    def reset_password_api(self):
        try:
            
            user = request.get_json()
            email = user.get("Email")
            new_password = user.get("New-Password")
            re_new_password = user.get("Re-New-Password")
            otp = user.get("OTP")

            if not email or not new_password or not re_new_password or not otp:
                return jsonify({'error': 'Fields cannot be empty'}), 400
            otp_tuple = valid_otp(email)
            if not otp_tuple:
                return jsonify({'error': 'Regenerate OTP'}), 400
            if otp != otp_tuple[2]:
                return jsonify({'error': 'Incorrect OTP'}), 400
            if datetime.now() > otp_tuple[4]:
                return jsonify({'error': 'OTP has expired'}), 400
            hashed_password = extract_data(email)
            if bcrypt.checkpw(new_password.encode('utf-8'), hashed_password.encode('utf-8')):
                return jsonify({'error': 'New Password Cannot be same as Old Password'}), 400
            if new_password != re_new_password:
                return jsonify({'error': 'Passwords Donot Match'}), 400
            if not is_password_strong(new_password):
                return jsonify({'error': 'Weak Password,Password must have 1 uppercase, 1 lowercase, 1 number, and be 8-25 characters long.'}), 400 
            else:
                reset_password(email,new_password)
                return jsonify({'Message': 'Password has been Reset!'}), 200
        except:
             return jsonify({'error': 'An Unexpected Error Occurred'}), 500

    def forgot_password(self):
        try:
            user = request.get_json()
            username = user.get("Email")
            if not username:
                return jsonify({'error': 'Fields cannot be empty'}), 400
            hashed_password = extract_data(username)
            if hashed_password is None:
                return jsonify({'error': 'Incorrect Email entered'}), 400
            else:
                otp = "".join(random.choices("0123456789", k=6))
                send_otp(user.get("Email"), otp)
                add_otp(otp, user.get("Email"))
                email = blur_email(user.get("Email"))
                return jsonify({'Message': f"An OTP has been sent to you email address: {email}. Please Check your inbox to proceed"}), 200
        except:
            return jsonify({'error': 'An Unexpected Error Occurred in fp'}), 500

    def get_address(self):
        conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='MyDB'
        )
        user = request.args.get("ID")
        cursor = conn.cursor()
        query = "SELECT PHONE, ADDRESS, EMAIL FROM USER WHERE USER_ID = %s;"
        cursor.execute(query, (user,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return jsonify({"address": result[1] , "phone" : result[0], "email" : result[2]}),200
        else:
            return jsonify({'error': 'An Unexpected Error Occurred, None Found'}), 500