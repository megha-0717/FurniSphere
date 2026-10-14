#import pymysql

#def connect():
   # return pymysql.connect(
       # host="localhost",
      # user="root",
        #password="",
        #database="furniture"
        
    #)

import os
import ssl
import pymysql

def connect():
    ca_certificate = os.environ.get("DB_SSL_CA")

    ssl_context = ssl.create_default_context(
        cadata=ca_certificate
    ) if ca_certificate else ssl.create_default_context()

    return pymysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        port=int(os.environ.get("DB_PORT", "3306")),
        charset="utf8mb4",
        ssl=ssl_context
    )
    
def add_text(name,email,number,password):
    connection=connect()
    cursor=connection.cursor()
    cursor.execute("INSERT INTO tbl1 (Name,Email,Number,Password)VALUES(%s,%s,%s,%s)",(name,email,number,password))
    connection.commit()
    cursor.close()
    connection.close()
    

def check_user(username, password):

    connection = connect()
      

    cursor = connection.cursor()

    query = """
    SELECT * FROM tbl1
    WHERE (Name=%s OR Email=%s) AND Password=%s
    """

    cursor.execute(query, (username, username, password))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user

def save_order(user_email, fullname, email, mobile, address, city, state, pincode, payment, total):

    connection = connect()
    cursor = connection.cursor()

    query = """
    INSERT INTO orders
    (user_email, fullname, email, mobile, address, city, state, pincode, payment, total_amount)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(query,(
        user_email,
        fullname,
        email,
        mobile,
        address,
        city,
        state,
        pincode,
        payment,
        total
    ))

    connection.commit()

    cursor.close()
    connection.close()
    
def add_cart_db(email, name, price):

    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT qty FROM cart WHERE email=%s AND product=%s",
        (email, name)
    )

    row = cursor.fetchone()

    if row:

        cursor.execute(
            "UPDATE cart SET qty=qty+1 WHERE email=%s AND product=%s",
            (email, name)
        )

    else:

        cursor.execute(
            "INSERT INTO cart(email,product,price,qty) VALUES(%s,%s,%s,%s)",
            (email, name, price, 1)
        )

    connection.commit()
    cursor.close()
    connection.close()
    
def get_cart_items(email):

    connection = connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    query="""
        SELECT
        product AS name,
        price,
        qty
        FROM cart
        WHERE email=%s
    """
    cursor.execute(query,(email,))
    items = cursor.fetchall()

    cursor.close()
    connection.close()

    return items 

def get_cart_count(email):

    connection = connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute(
        "SELECT SUM(qty)  AS total FROM cart WHERE email=%s",
        (email,)
    )

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    return row["total"] if row["total"] else 0


def clear_cart(email):

    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM cart WHERE email=%s",
        (email,)
    )

    connection.commit()

    cursor.close()
    connection.close()
    
def change_qty_db(email, name, change):

    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE cart SET qty=qty+%s WHERE email=%s AND product=%s",
        (change, email, name)
    )

    cursor.execute(
        """
        DELETE FROM cart WHERE qty<=0 AND email=%s AND  product=%s """,
        (email,name)
    )

    connection.commit()

    cursor.close()
    connection.close()
  
def get_product_qty(email, name):

    connection = connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute(
        "SELECT qty FROM cart WHERE email=%s AND product=%s",
        (email, name)
    )

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    return row["qty"] if row else 0

def toggle_wishlist(email, name, price, image):

    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM wishlist WHERE email=%s AND product=%s",
        (email, name)
    )

    row = cursor.fetchone()

    if row is not None:

        cursor.execute(
            "DELETE FROM wishlist WHERE email=%s AND product=%s",
            (email, name)
        )

        status = "removed"

    else:

        cursor.execute(
            "INSERT INTO wishlist(email,product,price,image) VALUES(%s,%s,%s,%s)",
            (email, name, price, image)
        )

        status = "added"

    connection.commit()

    cursor.close()
    connection.close()

    return status

def get_wishlist_count(email):

    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*)   FROM wishlist WHERE email=%s",
        (email,)
    )

    row=cursor.fetchone()

    cursor.close()
    connection.close()

    return row[0]

def get_wishlist_items(email):

    connection = connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute(
        "SELECT product AS name, price, image FROM wishlist WHERE email=%s",
        (email,)
    )

    items = cursor.fetchall()

    cursor.close()
    connection.close()

    return items
    

    
