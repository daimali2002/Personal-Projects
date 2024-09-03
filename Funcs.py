import bcrypt
import mysql.connector
import re
from datetime import datetime, timedelta
from flask import jsonify

def add_data(First, Last, Age, User, Pswd, Email, Phone, Address):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='MyDB'
    )
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(Pswd.encode('utf-8'), bcrypt.gensalt())
    insert_query = """
    INSERT INTO USER (FIRST_NAME, LAST_NAME, AGE, USERNAME, PASSWORD, EMAIL, PHONE, ADDRESS)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """

    data = (First, Last, Age, User, hashed_password, Email, normalized(Phone), Address)
    cursor.execute(insert_query, data)
    conn.commit()

    cursor.close()
    conn.close()

def extract_data(identifier):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='MyDB'
    )
    cursor = conn.cursor()
    if "@" in identifier:
        query = "SELECT PASSWORD FROM USER WHERE EMAIL = %s;"
    elif (identifier.isdigit() and len(identifier) == 11):
        identifier = identifier[:4]+"-"+identifier[4:]
        query = "SELECT PASSWORD FROM USER WHERE PHONE = %s;"
    elif (identifier[:4].isdigit() and identifier[5:].isdigit() and identifier[4] == '-' and len(identifier) == 12):
        query = "SELECT PASSWORD FROM USER WHERE PHONE = %s;"
    else:
        query = "SELECT PASSWORD FROM USER WHERE USERNAME = %s;"

    cursor.execute(query, (identifier,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result[0]
    return None

def extract_id(identifier):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='MyDB'
    )
    cursor = conn.cursor()
    if "@" in identifier:
        query = "SELECT USER_ID FROM USER WHERE EMAIL = %s;"
    elif (identifier.isdigit() and len(identifier) == 11):
        identifier = identifier[:4]+"-"+identifier[4:]
        query = "SELECT USER_ID FROM USER WHERE PHONE = %s;"
    elif (identifier[:4].isdigit() and identifier[5:].isdigit() and identifier[4] == '-' and len(identifier) == 12):
        query = "SELECT USER_ID FROM USER WHERE PHONE = %s;"
    else:
        query = "SELECT USER_ID FROM USER WHERE USERNAME = %s;"

    cursor.execute(query, (identifier,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result[0]
    return None

def reset_password(user,pswd):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='MyDB'
    )
    cursor = conn.cursor()

    if  "@" in user:
        query = "UPDATE USER SET PASSWORD = %s WHERE EMAIL = %s;"
    elif user.isdigit() and len(user) == 11:
        user = user[:4]+"-"+user[4:]
        query = "UPDATE USER SET PASSWORD = %s WHERE PHONE = %s;"
    elif (len(user) == 12  and (user[:4].isdigit() and user[5:].isdigit() and user[4] == '-')):
        query = "UPDATE USER SET PASSWORD = %s  WHERE PHONE = %s;"
    else:
        query = "UPDATE USER SET PASSWORD = %s  WHERE USERNAME = %s;"

    cursor.execute(query, (bcrypt.hashpw(pswd.encode('utf-8'), bcrypt.gensalt()),user))
    conn.commit()
    cursor.close()
    conn.close()

def add_otp(otp, email):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='MyDB'
    )
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO otp_table (email, otp, created_at, expires_at)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    otp = VALUES(otp),
    created_at = VALUES(created_at),
    expires_at = VALUES(expires_at);
    """
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    expires_at = (datetime.now() + timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')

    data = (email, otp, created_at, expires_at)
    cursor.execute(insert_query, data)
    conn.commit()
    cursor.close()
    conn.close()
    
def valid_otp(email):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='MyDB'
    )

    cursor = conn.cursor()

    query = """
        SELECT * FROM otp_table 
        WHERE email = %s 
        ORDER BY created_at DESC 
        LIMIT 1;
        """
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def is_password_strong(password):
    if len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in '!@#$%^&*()-_=+[{]}\\|;:\'",<.>/?' for c in password)
    
    return has_upper and has_lower and has_digit

def is_valid_email(email):
    if len(email) > 64:
        return False 
    if "@" in email:
        parts = email.split("@")
        if len(parts) == 2 and parts[0] and parts[1] and len(parts[0]) > 2 and len(parts[1]) > 3:
            if not re.match("^[a-zA-Z0-9._%+-]+$", parts[0]) or not re.match("^[a-zA-Z0-9.-]+$", parts[1]):
                return False
            parts = parts[1].split('.')
            if len(parts) >= 2 and parts[0] and parts[1]:
                return True
    return False

def is_valid_username(username):
    if "@" in username:
        return False
    if len(username) < 4 or len(username) > 25:
        return False
    if not re.match("^[a-zA-Z0-9_]*[a-zA-Z]+[a-zA-Z0-9_]*$", username):
        return False
    return True

def is_valid_name(name):
    if len(name) < 2 or len(name) > 32:
        return False
    if not re.match("^[a-zA-Z -]+$", name):
        return False
    
    return True

def is_valid_phone(phone):
    return ((phone.isdigit() and len(phone) == 11) or (phone[:4].isdigit() and phone[5:].isdigit() and phone[4] == '-' and len(phone) == 12)) and phone[0] == "0" and phone[1] == "3"

def is_valid_age(age):
    return age.isdigit() and 1 <= int(age) <= 150

def normalized(num):
    if len(num) == 12:
        return num
    else:
        return num[:4]+"-"+num[4:]
    
def blur_email(email):
    parts = email.split('@')
    username = parts[0]
    domain = parts[1]
    username_length = len(username)
    blurred_username = username[0] + username[1] + username[2] + '*' * (username_length - 4) + username[-1]
    blurred_email = blurred_username + '@' + domain
    return blurred_email

def valid_price(price):
    try:
        price = float(price)
        if price > 0 and price < 99999999:
                return True
    except ValueError:
        return False
    
def valid_rating(rating):
    try:
        rating = float(rating)
        if rating >= 0 and rating <= 5:
                return True
    except ValueError:
        return False
    
def valid_discount(disc):
    try:
        disc = float(disc)
        if disc >= 0 and disc <= 100:
                return True
    except ValueError:
        return False

def update_prods(id,title,description,category,price,rating,stock,brand,discount):
    conn = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database='MyDB'
                )
    cursor = conn.cursor()

    if title:
        insert_query = "UPDATE PRODUCTS SET TITLE =  %s WHERE ID = %s"
        data = (title,id)
        cursor.execute(insert_query, data)
        conn.commit()
    if description:
        insert_query = "UPDATE PRODUCTS SET DESCRIPTION =  %s WHERE ID = %s"
        data = (description,id)
        cursor.execute(insert_query, data)
        conn.commit()
    if category:
        insert_query = "UPDATE PRODUCTS SET CATEGORY =  %s WHERE ID = %s"
        data = (category,id)
        cursor.execute(insert_query, data)
        conn.commit()
    if price:
        insert_query = "UPDATE PRODUCTS SET PRICE =  %s WHERE ID = %s"
        data = (price,id)
        cursor.execute(insert_query, data)
        conn.commit()
    if rating:
        insert_query = "UPDATE PRODUCTS SET RATING =  %s WHERE ID = %s"
        data = (rating,id)
        cursor.execute(insert_query, data)
        conn.commit()
    if stock:
        insert_query = "UPDATE PRODUCTS SET STOCK =  %s WHERE ID = %s"
        data = (stock,id)
        cursor.execute(insert_query, data)
        conn.commit()
    if brand:
        insert_query = "UPDATE PRODUCTS SET BRAND =  %s WHERE ID = %s"
        data = (brand,id)
        cursor.execute(insert_query, data)
        conn.commit()
    if discount:
        insert_query = "UPDATE PRODUCTS SET DISCOUNT =  %s WHERE ID = %s"
        data = (discount,id)
        cursor.execute(insert_query, data)
        conn.commit()

    cursor.close()
    conn.close()

def exists_in_db(num):
     conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='MyDB'
        )
     cursor = conn.cursor()
     
     query = f"SELECT * FROM PRODUCTS WHERE ID = {num}"
     cursor.execute(query)
     result = cursor.fetchone()
     cursor.close()
     conn.close()
     return result

def insert_prods(id,title,description,category,price,rating,stock,brand,discount):
    conn = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database='MyDB'
                )
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO PRODUCTS (ID, TITLE, DESCRIPTION, CATEGORY, PRICE, RATING, STOCK, BRAND, DISCOUNT)
    VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s)
    """
    data = (id,title,description,category,price,rating,stock,brand,discount)
    cursor.execute(insert_query, data)
    conn.commit()
    cursor.close()
    conn.close()
    return cursor.lastrowid

def get_max_id():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='MyDB'
    )
    cursor = conn.cursor()
    query = "SELECT MAX(ID) FROM ORDERS;"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result and result[0] is not None:
        return result[0] + 1
    return 1 

def add_prod_guest(id, products):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='MyDB'
        )
        cursor = conn.cursor()

        # Start a transaction
        conn.start_transaction()

        tot = 0
        tot_disc = 0 


        for Prod in products:
            product_id = Prod["product_id"]
            product_quantity = Prod["quantity"]

            if not isinstance(product_quantity, int) or product_quantity  <= 0:
                raise ValueError('Products quantity can only be integers and greater than 0')

            query = "SELECT PRICE, STOCK, AMOUNT_AFTER_DISCOUNT FROM PRODUCTS WHERE ID = %s;"
            cursor.execute(query, (product_id,))
            result = cursor.fetchone()
            if result:
                price, stock , amount_after_discount= result
                discount = price - amount_after_discount
            else:
                raise ValueError(f'Product {product_id} does not exist')

            if stock < product_quantity:
                raise ValueError(f'Sorry, {stock} items left for Product {product_id}')

            insert_query = "INSERT INTO ORDERED_PRODUCTS (PROD_ID, ORDER_ID, QUANTITY, PRICE_PER_PROD, DISCOUNT_PER_PROD) VALUES (%s, %s, %s, %s, %s)"
            data = (product_id, id, product_quantity, price, discount)
            cursor.execute(insert_query, data)

            # Reduce Stock
            new_stock = stock - product_quantity
            query = "UPDATE PRODUCTS SET STOCK = %s WHERE ID = %s;"
            cursor.execute(query, (new_stock, product_id))
            
            tot += amount_after_discount * product_quantity  # Accumulate total price
            tot_disc +=  discount * product_quantity 
        # Commit transaction if all operations succeed
        conn.commit()
        return {'total_price': tot, 'discount' : tot_disc }

    except Exception as e:
        # Rollback if any error occurs
        conn.rollback()
        return {'error': str(e)}

    finally:
        cursor.close()
        conn.close()

def add_to_orders_guest(order_id,phone,address,amount,discount):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='MyDB'
    )
    cursor = conn.cursor()
    insert_query = "INSERT INTO ORDERS (ID, TOTAL_AMOUNT, USER_PHONE, USER_ADDRESS, TOTAL_DISCOUNT) VALUES (%s, %s, %s, %s, %s);"
    data = (order_id,amount,normalized(phone),address,discount)
    cursor.execute(insert_query, data)
    conn.commit()
    cursor.close()
    conn.close()

def add_to_orders_user(order_id,userid,phone,address,amount,discount):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='MyDB'
    )
    cursor = conn.cursor()
    insert_query = "INSERT INTO ORDERS (ID, USER_ID,TOTAL_AMOUNT, USER_PHONE, USER_ADDRESS,TOTAL_DISCOUNT) VALUES (%s, %s, %s, %s, %s, %s);"
    data = (order_id,userid,amount,phone,address,discount)
    cursor.execute(insert_query, data)
    conn.commit()
    cursor.close()
    conn.close()

def get_user_details(user):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='MyDB'
    )
    cursor = conn.cursor()
    query = "SELECT PHONE, ADDRESS FROM USER WHERE USER_ID = %s;"

    cursor.execute(query, (user,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result[0], result[1]
    else:
        return None, None