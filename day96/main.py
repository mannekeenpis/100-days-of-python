from flask import Flask, render_template, flash, redirect, url_for, request, session, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegisterForm
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import stripe
import os


app = Flask(__name__)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = "BlahBlahBlah"

# Connect to database for items to sell
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Products.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #prevents some warnings
db = SQLAlchemy(app)


class Product(UserMixin, db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), nullable=False)
    product_description = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_volume = db.Column(db.Integer, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    emailaddress = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

# class Order(UserMixin, db.Model):
#     __tablename__ = "orders"
#     order_id = db.Column(db.Integer, primary_key=True)
#     customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     customer = relationship("User", back_populates="orders")
#     order_items = relationship("Product", back_populates="orders")

db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=["GET", "POST"])
def home():
    basket_items = 0
    if "cart" in session:
        basket_items = len(session["cart"])
    products = db.session.query(Product).filter(Product.stock_volume >=1).all()
    return render_template('Index.html', basketitems=basket_items,products=products)


@app.route('/login', methods=["GET", "POST"])
def login():
    basket_items = 0
    if "cart" in session:
        basket_items = len(session["cart"])
    session["logged_in"] = False
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(emailaddress=loginform.emailaddress.data).first()
        if not user:
            flash("No user exists with this email address. Maybe you need to register first?")
            return redirect(url_for('register'))
        elif not check_password_hash(user.password, loginform.password.data):
            flash("Password is incorrect. Please try again.")
            return redirect(url_for('login'))
        else:
            login_user(user)
            session["logged_in"] = True
            session["user"] = loginform.emailaddress.data
            return redirect(url_for('home'))
    return render_template("login.html", basketitems=basket_items,form=loginform)


@app.route('/register', methods=["GET", "POST"])
def register():
    basket_items = 0
    if "cart" in session:
        basket_items = len(session["cart"])
    registerform = RegisterForm()
    if registerform.validate_on_submit():
        user = User.query.filter_by(emailaddress=registerform.emailaddress.data).first()
        if not user:
            NewUser = User(name=registerform.name.data,
                           emailaddress=registerform.emailaddress.data,
                           password=generate_password_hash(registerform.password.data, method="pbkdf2:sha256", salt_length=8)
                           )
            db.session.add(NewUser)
            db.session.commit()
            login_user(NewUser)
            flash(f"Your account has been created {current_user.name}. Now please login.")
            return redirect(url_for('login'))
        else:
            flash("An account already exists for that email address, please try again.")
            return redirect(url_for('register'))
    else:
        return render_template("register.html", basketitems=basket_items, form=registerform)


@app.route('/addtoCart', methods=["GET", "POST"])
def addtoCart():
    if request.method == "GET":
        if "cart" not in session:
            session["cart"] = []
        session["cart"].append(request.args.get('id'))
        flash("Item added to cart")
    return redirect(url_for('home'))


@app.route('/RemovefromCart', methods=["GET", "POST"])
def removefromCart():
    NewCart = []
    ID_ToRemove = request.args.get('id')
    for item in session["cart"]:
        if item != ID_ToRemove:
            NewCart.append(item)
    session["cart"] = []
    session["cart"] = NewCart
    return redirect(url_for('ShoppingCart'))


@app.route('/ShoppingCart', methods=["GET", "POST"])
def ShoppingCart():
    TotalPrice = 0.0
    basket_items = 0
    if "cart" in session:
        # basket_items = len(session["cart"])
        dict_of_items = {}
        for item in session["cart"]:
            product = Product.query.get(item)
            TotalPrice += product.price
            if product.id in dict_of_items:
                dict_of_items[product.id]["qty"] += 1
            else:
                dict_of_items[product.id] = {"product_ID": product.id, "img_url": product.img_url, "qty": 1, "name": product.product_name, "price": product.price}
        for item in session["cart"]:
            product = Product.query.get(item)
            if dict_of_items[product.id]["qty"] > product.stock_volume:
                difference = dict_of_items[product.id]["qty"] - product.stock_volume
                TotalPrice -= difference * dict_of_items[product.id]["price"]
                dict_of_items[product.id]["qty"] = product.stock_volume
                flash("Not enough items in stock. Basket items adjusted to maximum available!")
        session["cart"] = []
        for item in dict_of_items:
            session["cart"].append(dict_of_items[item]["product_ID"])
        basket_items = len(session["cart"])
        TotalPrice = round(TotalPrice, 2)
    else:
        dict_of_items = {}
        flash("You have no items in your cart!")
    return render_template('ShoppingCart.html', cart=dict_of_items, basketitems=basket_items, baskettotal=TotalPrice)


@app.route('/create-checkout-session', methods=["POST"])
def create_checkout_session():
    stripe.api_key = os.environ.get("Stripe_APIKEY")
    dict_of_items = {}
    for item in session["cart"]:
        product = Product.query.get(item)
        priceInt = str(product.price).split('.')
        price = int(f"{int(priceInt[0])}{int(priceInt[1])}")
        if product.id in dict_of_items:
            dict_of_items[product.id]["quantity"] += 1
        else:
            dict_of_items[product.id] = {
                "name": product.product_name,
                "amount": price,
                "quantity": 1,
                "currency": "gbp"
                }
    item_list = []
    for item in dict_of_items:
        item_list.append(dict_of_items[item])
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=item_list,
        mode='payment',
        success_url="http://127.0.0.1:5000/Success",
        cancel_url="http://127.0.0.1:5000/Paymentfail.html",
    )
    return jsonify(id=checkout_session.id)


@app.route('/Success')
def payment_success():
    for item in session["cart"]:
        product = Product.query.get(item)
        product.stock_volume -= 1
        db.session.commit()
    # newOrder = Order(customer=current_user,
    #     )
    # db.session.add(newOrder)
    # db.session.commit()
    session.pop('cart', None)
    return render_template('Success.html')


@app.route('/logout')
def logout():
    logout_user()
    session.pop('cart', None)
    session["logged in"] = False
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)