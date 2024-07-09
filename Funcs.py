import mysql.connector
import bcrypt
import re
from datetime import datetime, timedelta
from flask import jsonify




def add_data(First, Last, Age, User, Pswd, Email, Phone):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='MyDB'
    )
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(Pswd.encode('utf-8'), bcrypt.gensalt())
    insert_query = """
    INSERT INTO USER_INFO (FIRST_NAME, LAST_NAME, AGE, USERNAME, PASSWORD, EMAIL, PHONE)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """

    data = (First, Last, Age, User, hashed_password, Email, normalized(Phone))
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
        query = "SELECT PASSWORD FROM USER_INFO WHERE EMAIL = %s;"
    elif (identifier.isdigit() and len(identifier) == 11):
        identifier = identifier[:4]+"-"+identifier[4:]
        query = "SELECT PASSWORD FROM USER_INFO WHERE PHONE = %s;"
    elif (identifier[:4].isdigit() and identifier[5:].isdigit() and identifier[4] == '-' and len(identifier) == 12):
        query = "SELECT PASSWORD FROM USER_INFO WHERE PHONE = %s;"
    else:
        query = "SELECT PASSWORD FROM USER_INFO WHERE USERNAME = %s;"

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
        query = "UPDATE USER_INFO SET PASSWORD = %s WHERE EMAIL = %s;"
    elif user.isdigit() and len(user) == 11:
        user = user[:4]+"-"+user[4:]
        query = "UPDATE USER_INFO SET PASSWORD = %s WHERE PHONE = %s;"
    elif (len(user) == 12  and (user[:4].isdigit() and user[5:].isdigit() and user[4] == '-')):
        query = "UPDATE USER_INFO SET PASSWORD = %s  WHERE PHONE = %s;"
    else:
        query = "UPDATE USER_INFO SET PASSWORD = %s  WHERE USERNAME = %s;"

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

    

def update_prods(id,title,description,category,price,rating,stock,brand):
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



def insert_prods(id,title,description,category,price,rating,stock,brand):
    conn = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database='MyDB'
                )
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO PRODUCTS (ID, TITLE, DESCRIPTION, CATEGORY, PRICE, RATING, STOCK, BRAND)
    VALUES (%s, %s, %s, %s,%s, %s, %s, %s)
    """
    data = (id,title,description,category,price,rating,stock,brand)
    cursor.execute(insert_query, data)
    conn.commit()
    cursor.close()
    conn.close()
    return cursor.lastrowid

    
