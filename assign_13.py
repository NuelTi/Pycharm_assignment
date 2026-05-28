# --------- Implementing database in Accounting Web Application--------

from flask import Flask
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy


# ---------- CREATE APP ----------
app = Flask(__name__)


# ---------- DATABASE SETTINGS ----------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///accounting.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# create database object
db = SQLAlchemy(app)


# ---------- TABLES ----------
# products table
class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    amount = db.Column(db.Integer)


# balance table
class Balance(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    value = db.Column(db.Float)


# history table
class History(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.String(200))


# ---------- CREATE DATABASE ----------
with app.app_context():

    db.create_all()

    # create first balance if empty
    if Balance.query.first() is None:

        first_balance = Balance(value=1000)

        db.session.add(first_balance)

        db.session.commit()


# ---------- MAIN PAGE ----------
@app.route("/")
def index():

    text = ""

    # get balance
    balance = Balance.query.first()

    text += "<h1>Accounting System</h1>"

    text += "<h2>Balance: "

    text += str(balance.value)

    text += "</h2>"


    # ---------- SHOW PRODUCTS ----------
    text += "<h2>Warehouse</h2>"

    products = Product.query.all()

    for product in products:

        text += product.name

        text += " : "

        text += str(product.amount)

        text += "<br>"


    # ---------- BALANCE FORM ----------
    text += """
    <h2>Change Balance</h2>

    <form action="/balance" method="POST">

        <input type="text" name="value">

        <button type="submit">Save</button>

    </form>
    """


    # ---------- PURCHASE FORM ----------
    text += """
    <h2>Purchase</h2>

    <form action="/purchase" method="POST">

        Product:
        <input type="text" name="product">

        Amount:
        <input type="text" name="amount">

        Price:
        <input type="text" name="price">

        <button type="submit">Buy</button>

    </form>
    """


    # ---------- SALE FORM ----------
    text += """
    <h2>Sale</h2>

    <form action="/sale" method="POST">

        Product:
        <input type="text" name="product">

        Amount:
        <input type="text" name="amount">

        Price:
        <input type="text" name="price">

        <button type="submit">Sell</button>

    </form>
    """


    text += "<br>"

    text += '<a href="/history/">History</a>'

    return text


# ---------- CHANGE BALANCE ----------
@app.route("/balance", methods=["POST"])
def change_balance():

    try:

        value = float(request.form["value"])

        balance = Balance.query.first()

        balance.value += value

        history = History(text="Balance changed")

        db.session.add(history)

        db.session.commit()

    except Exception as e:

        return "Error: " + str(e)

    return redirect("/")


# ---------- PURCHASE ----------
@app.route("/purchase", methods=["POST"])
def purchase():

    try:

        product_name = request.form["product"]

        amount = float(request.form["amount"])

        price = float(request.form["price"])

        total = amount * price


        balance = Balance.query.first()

        # check money
        if balance.value < total:

            return "Not enough money"


        # update balance
        balance.value -= total


        # check if product exists
        product = Product.query.filter_by(name=product_name).first()

        if product:

            product.amount += amount

        else:

            new_product = Product(
                name=product_name,
                amount=amount
            )

            db.session.add(new_product)


        history = History(
            text="Bought " + product_name
        )

        db.session.add(history)

        db.session.commit()

    except Exception as e:

        return "Error: " + str(e)

    return redirect("/")


# ---------- SALE ----------
@app.route("/sale", methods=["POST"])
def sale():

    try:

        product_name = request.form["product"]

        amount = float(request.form["amount"])

        price = float(request.form["price"])


        product = Product.query.filter_by(
            name=product_name
        ).first()


        # check product
        if product is None:

            return "Product does not exist"


        # check amount
        if product.amount < amount:

            return "Not enough products"


        # update product
        product.amount -= amount


        # update balance
        balance = Balance.query.first()

        balance.value += amount * price


        history = History(
            text="Sold " + product_name
        )

        db.session.add(history)

        db.session.commit()

    except Exception as e:

        return "Error: " + str(e)

    return redirect("/")


# ---------- HISTORY ----------
@app.route("/history/")
@app.route("/history/<line_from>/<line_to>/")
def history(line_from=None, line_to=None):

    text = "<h1>History</h1>"


    history_list = History.query.all()


    # show all history
    if line_from is None or line_to is None:

        for item in history_list:

            text += item.text

            text += "<br>"


    # show selected history
    else:

        try:

            line_from = int(line_from)

            line_to = int(line_to)

            selected = history_list[line_from:line_to]

            for item in selected:

                text += item.text

                text += "<br>"

        except:

            return "Wrong history range"


    text += "<br>"

    text += "<a href='/'>Back</a>"

    return text


# ---------- START APP ----------
if __name__ == "__main__":

    app.run(debug=True)
