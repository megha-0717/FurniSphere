from flask import *
#pip install flask
from db import (
    add_text,
    check_user,
    add_cart_db,
    get_cart_items,
    get_cart_count,
    change_qty_db,
    get_product_qty,
    toggle_wishlist,
    get_wishlist_count,
    get_wishlist_items,
    save_order,clear_cart
)


#app=Flask(__name__)
#app.secret_key="furnisphere123"
import os
from flask import Flask

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")


#import os
#from flask import Flask

#app = Flask(__name__)
#app.secret_key = os.environ.get("SECRET_KEY")

#if not app.secret_key:
 #   raise RuntimeError("SECRET_KEY is not configured")

@app.route('/')
def home():

    logged_in = "user" in session

    cart_count = 0
    wishlist_count = 0

    if logged_in:
        cart_count = get_cart_count(session["user"])
        wishlist_count = get_wishlist_count(session["user"])

    return render_template(
        "index.html",
        logged_in=logged_in,
        cart_count=cart_count,
        wishlist_count=wishlist_count
    )

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/signup')
def signup():
     if "user" in session:
        return redirect(url_for("home"))
    
     return render_template("signup.html")


# @app.route('/login')
# def login():
#     return render_template("login.html")
@app.route('/about')
def about():
    return render_template("about.html")

@app.route("/category")
def category():

    logged_in = "user" in session

    cart_count = 0
    wishlist_count = 0

    if logged_in:
        cart_count = get_cart_count(session["user"])
        wishlist_count = get_wishlist_count(session["user"])

    return render_template(
        "category.html",
        logged_in=logged_in,
        cart_count=cart_count,
        wishlist_count=wishlist_count
    )

@app.route('/living_room')
def livingroom():
       logged_in="user" in session
     
       return render_template("living_room.html",logged_in=logged_in)

@app.route('/bedroom')
def bedroom():
     logged_in="user" in session
     return render_template("bedroom.html",logged_in=logged_in)
    

@app.route('/dining_room')
def diningroom():
    logged_in="user" in session
    return render_template("dining_room.html",logged_in=logged_in)
    

@app.route('/office')
def office():
    logged_in="user" in session
    return render_template("office.html",logged_in=logged_in)
    

@app.route('/kids')
def kids():
    logged_in="user" in session
    return render_template("kids.html",logged_in=logged_in)
    
   

@app.route('/bookshelves')
def bookshelves():
    logged_in="user" in session
    return render_template("bookshelves.html",logged_in=logged_in)
    

@app.route('/accent')
def accent():
    logged_in="user" in session
    return render_template("accent.html",logged_in=logged_in)
    

@app.route('/product')
def product():
    logged_in="user" in session
    return render_template("product.html",logged_in=logged_in)

@app.route("/checkout")
def checkout():

    if "user" not in session:
        return redirect(url_for("login", next="/checkout"))

    cart_items = get_cart_items(session["user"])

    grand_total = 0

    for item in cart_items:
        grand_total += item["price"] * item["qty"]

    if len(cart_items) == 0:
        return redirect("/cart")

    return render_template(
        "checkout.html",
        cart_items=cart_items,
        grand_total=grand_total
    )
    
@app.route("/place_order", methods=["POST"])
def place_order():

    if "user" not in session:
        return redirect(url_for("login"))
    
    # print("Place order route called")
    
    user_email=session["user"]
    fullname = request.form["fullname"]
    email = request.form["email"]
    mobile = request.form["mobile"]
    address = request.form["address"]
    city = request.form["city"]
    state = request.form["state"]
    pincode = request.form["pincode"]
    payment = request.form["payment"]
    total = request.form["total"]
    print("Total received:",request.form["total"])
    
    save_order(
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
    )
    clear_cart(session["user"])
    
    # print("Order Placed Successfully!")
    flash("Order Placed Successfully!")

    return redirect("/")

@app.route("/cart")
def cart():

    if "user" not in session:
        return redirect(url_for("login", next="/cart"))

    cart_items = get_cart_items(session["user"])

    grand_total = 0

    for item in cart_items:
        grand_total += item["price"] * item["qty"]

    return render_template(

        "cart.html",

        cart_items=cart_items,

        grand_total=grand_total,

        logged_in=True

    )

@app.route('/customer')
def customer():
    return render_template("customer.html")




# @app.route("/sucess",methods =["POST"])
# def sucess():
#      if request.method == 'POST':
#          name= request.form['nm']
#          email=request.form['em']
#          number=request.form['num']
#          password=request.form['pswd']
#          add_text(name,email,number,password)
#          return render_template("/login")

# @app.route("/login", methods=["GET", "POST"])
# def login():

#     if request.method == "POST":

#         username = request.form["username"]
#         password = request.form["password"]

#         user = check_user(username, password)

#         if user:
#             session["user"] = user[2]
#             session["name"] = user[1]

#             next_page = request.form.get("next")

#             if next_page:
#                 return redirect(next_page)

#             return redirect(url_for("home"))

#         else:
#             return render_template(
#                 "login.html",
#                 error="Invalid Username or Password",
#                 next=request.form.get("next")
#             )

#     next_page = request.args.get("next")

#     return render_template(
#         "login.html",
#         next=next_page
#     )
@app.route("/login", methods=["GET", "POST"])
def login():

    if "user" in session:
        return redirect(url_for("home"))

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = check_user(username, password)

        if user:
            session["user"] = user[2]
            session["name"] = user[1]

            next_page = request.form.get("next", "")

            if next_page.startswith("/") and not next_page.startswith("//"):
                return redirect(next_page)

            return redirect(url_for("home"))

        return render_template(
            "login.html",
            error="Invalid Username or Password",
            next=request.form.get("next", "")
        )

    return render_template(
        "login.html",
        next=request.args.get("next", "")
    )


@app.route("/sucess", methods=["POST"])
def sucess():

    name = request.form['nm']
    email = request.form['em']
    number = request.form['num']
    password = request.form['pswd']

    add_text(name, email, number, password)
    next_page=request.form.get("next","/")
    return redirect( url_for("login", next=next_page))
    
    
# @app.route("/admin_orders")
# def admin_orders():

#     orders = get_orders()

#     return render_template(
#         "admin_orders.html",
#         orders=orders
#     ) 
    
# @app.route("/delete_order/<int:id>")
# def delete_order_route(id):

#     delete_order(id)

#     return redirect("/admin_orders")
@app.route('/logged_out')
def logout():
       session.clear()
       return render_template("logged_out.html")
    
@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():

    if "user" not in session:
        return jsonify({"login": False})

    data = request.get_json()

    add_cart_db(
        session["user"],
        data["name"],
        data["price"]
    )

    return jsonify({
        "login": True,
        "count": get_cart_count(session["user"])
    })

    
@app.route("/change_qty", methods=["POST"])
def change_qty():

    if "user" not in session:
        return jsonify({"login": False})

    data = request.get_json()

    change_qty_db(
        session["user"],
        data["name"],
        data["change"]
    )

    return jsonify({
         "login":True,
        "count": get_cart_count(session["user"]),
        "qty": get_product_qty(session["user"], data["name"])
    })


@app.route("/get_product_qty", methods=["POST"])
def product_qty():

    if "user" not in session:
        return jsonify({"qty": 0})

    data = request.get_json()

    return jsonify({
        "qty": get_product_qty(session["user"], data["name"])
    })


@app.route("/cart_count")
def cart_count():

    if "user" not in session:
        return jsonify({"count": 0})

    return jsonify({
        "count": get_cart_count(session["user"])
    })

@app.route("/wishlist")
def wishlist():

    logged_in="user" in session
    if not logged_in:
    
        return redirect(url_for("login", next="/wishlist"))

    items = get_wishlist_items(session["user"])

    return render_template(
        "wishlist.html",
        wishlist=items,
        logged_in=True
    )
    
@app.route("/add_wishlist", methods=["POST"])
def wishlist_api():

    if "user" not in session:
        return jsonify({"login": False})

    data = request.get_json()

    status = toggle_wishlist(
        session["user"],
        data["name"],
        data["price"],
        data["image"]
    )

    return jsonify({
        "login": True,
        "status": status,
        "count": get_wishlist_count(session["user"])
    })

@app.route("/wishlist_count")
def wishlist_count():

    if "user" not in session:
        return jsonify({"count": 0})

    return jsonify({
        "count": get_wishlist_count(session["user"])
    })


@app.route("/wishlist_items")
def wishlist_items():

    if "user" not in session:
        return jsonify([])

    return jsonify(get_wishlist_items(session["user"]))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
