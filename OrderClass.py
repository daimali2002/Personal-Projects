from flask import Flask, render_template, request, jsonify
from Funcs import *
import random
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError


class OrderApp:

    def buy():
        try:
            data = request.get_json()

            address = data.get("Address")
            phone =  data.get("Phone")
            User = data.get("User")
            Products = data.get("Products")

            if not Products:
                return jsonify({'error': 'Products Cannot be empty at checkout'}), 400
            if not User:
                #GUEST CHECKOUT
                if not phone or not address:
                    return jsonify({'error': 'Phone or Address not entered'}), 400
                if not is_valid_phone(phone):
                    return jsonify({'error': 'Incorrect Phone entered'}), 400
                if len(address) < 10:
                    return jsonify({'error': 'Incorrect Address, Address must be atleast 10 Characters'}), 400
                guest_id = get_max_id() # Generating Order ID
                result = add_prod_guest(guest_id, Products)
                if 'error' in result:
                    return jsonify(result), 400
                sum = result.get("total_price")
                discount = result.get("discount")
                add_to_orders_guest(guest_id,phone,address,sum,discount)
                return jsonify({'message': 'Success, Order Placed'}), 200
            else:
                
                # get address and phone from users
                phone, address = get_user_details(User)
                if not phone and not address:
                    return jsonify({'error': 'USER DOES NOT EXIST'}), 400
                guest_id = get_max_id() # Generating Order ID
                result = add_prod_guest(guest_id, Products)
                if 'error' in result:
                    return jsonify(result), 400
                sum = result.get("total_price")
                discount = result.get("discount")
                add_to_orders_user(guest_id,User,phone,address,sum,discount)
                return jsonify({'message': 'Success, Order Placed'}), 200
            
        except Exception as e:
            return {'error': str(e)}
        
    def cart():
        return render_template("cart.html")
    
    def checkout():
        return render_template("checkout.html")
    
