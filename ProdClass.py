from flask import Flask, render_template, request, jsonify
from Funcs import *
import random
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

class ProdApp:

    def getall(self):
        try:
            conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='MyDB'
            )
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM PRODUCTS"
            cursor.execute(query)
            result = cursor.fetchall()
            result = {"PRODUCTS" : result, "TOTAL" : len(result)}
            cursor.close()
            conn.close()
            return jsonify(result)
        except:
            return jsonify({'error': 'An Unexpected Error Occurred'}), 500
    
    def getone(self):
        try:
            conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='MyDB'
            )
            cursor = conn.cursor(dictionary=True)
            id = request.args.get("ID")
            if not id or not id.isdigit():
                return jsonify({'error': 'Incorrect ID Entered'}), 400
            query = f"SELECT * FROM PRODUCTS WHERE ID = {id}"
            cursor.execute(query)
            result = cursor.fetchone()
            if not result:
                return jsonify({'error': 'Incorrect ID Entered'}), 400
            cursor.close()
            conn.close()
            return jsonify(result)
        except:
            return jsonify({'error': 'An Unexpected Error Occurred'}), 500
            
    def updatevals(self):
        try:
            data = request.get_json()

            id = data.get("ID")
            title = data.get("TITLE")
            description = data.get("DESCRIPTION")       
            category =  data.get("CATEGORY")       
            price =  data.get("PRICE")   
            rating =  data.get("RATING")  
            stock = data.get("STOCK")
            brand = data.get("BRAND")
            discount =  data.get("DISCOUNT")
            
            if not id:
                return jsonify({'error': "must provide ID to update its values"}), 400
            if not exists_in_db(id):
                return jsonify({'error': "ID provided does not exist"}), 400 
            if price and not valid_price(price):
                return jsonify({'error': "Invalid Price entered"}), 400
            if rating and not valid_rating(rating):
                return jsonify({'error': "Invalid rating entered"}), 400
            if title and len(title) > 64:
                return jsonify({'error': "Invalid title length, must be less than 64 Characters"}), 400
            if description and len(description) > 255:
                return jsonify({'error': "Invalid Description length, must be less than 255 Characters"}), 400
            if category and len(category) > 32:
                return jsonify({'error': "Invalid category length, must be less than 32 Characters"}), 400
            if brand and len(brand) > 255:
                return jsonify({'error': "Invalid brand length, must be less than 64 Characters"}), 400
            if stock and (not stock.isdigit() or int(stock) < 0):
                return jsonify({'error': "Invalid stock entered"}), 400
            if discount and not valid_discount(discount):
                 return jsonify({'error': "Invalid Discount entered"}), 400
            
            update_prods(id,title,description,category,price,rating,stock,brand, discount)
            return jsonify({'Message': "Values Updated!"}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    def insertProd(self):
        try:
            data = request.get_json()
            id = data.get("ID")
            title = data.get("TITLE")
            description = data.get("DESCRIPTION")       
            category =  data.get("CATEGORY")       
            price =  data.get("PRICE")   
            rating =  data.get("RATING","0.00")  
            stock = data.get("STOCK", "0")
            brand = data.get("BRAND")
            discount = data.get("DISCOUNT")
            

            if not price:
                return jsonify({'error': "must provide price"}), 400
            if not title:
                return jsonify({'error': "must provide Title"}), 400
            if id and exists_in_db(id):
                return jsonify({'error': "ID provided already exists"}), 400 
            if not valid_price(price):
                return jsonify({'error': "Invalid Price entered"}), 400
            if rating and not valid_rating(rating):
                return jsonify({'error': "Invalid rating entered"}), 400
            if len(title) > 64:
                return jsonify({'error': "Invalid title length, must be less than 64 Characters"}), 400
            if description and len(description) > 255:
                return jsonify({'error': "Invalid Description length, must be less than 255 Characters"}), 400
            if category and len(category) > 32:
                return jsonify({'error': "Invalid category length, must be less than 32 Characters"}), 400
            if brand and len(brand) > 255:
                return jsonify({'error': "Invalid brand length, must be less than 64 Characters"}), 400
            if stock and (not stock.isdigit() or int(stock) < 0):
                return jsonify({'error': "Invalid stock entered"}), 400
            if not valid_discount(discount):
                 return jsonify({'error': "Invalid Discount entered"}), 400
            
            num = insert_prods(id,title,description,category,price,rating,stock,brand, discount)
            return jsonify({'Message': f"Product added to database! ID: {num}"}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def deleteprod(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='MyDB'
            )
            cursor = conn.cursor()
            data = request.get_json()
            id = data.get("ID")
            if not id or not str(id).isdigit():
                return jsonify({'error': 'Incorrect ID Entered'}), 400
            query = "DELETE FROM PRODUCTS WHERE ID = %s"
            cursor.execute(query, (id,))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({'error': 'ID not found'}), 400
            cursor.close()
            conn.close()
            return jsonify({'message': 'ID has been deleted'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def dashboard(self):
        return render_template('dashboard.html')
    
    def one_prod(self):
        return render_template("product-details.html")







