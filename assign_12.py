from flask import Flask
from flask import request
from flask import redirect

import json
import os


app = Flask(__name__)


# ---------- LOAD DATA ----------
FILE_NAME = "history.json"


# create default data
default_data = {
    "balance": 1000,
    "warehouse": {},
    "history": []
}


# check file
if os.path.exists(FILE_NAME):

    try:

        with open(FILE_NAME, "r") as file:

            data = json.load(file)

    except:

        print("Error reading JSON file.")

        data = default_data

else:

    data = default_data


# ---------- SAVE DATA ----------
def save_data():

    with open(FILE_NAME, "w") as file:

        json.dump(data, file)


# ---------- MAIN PAGE ----------
@app.route("/")
def index():

    text = ""

    text += "<h1>Accounting System</h1>"

    text += "<h2>Balance: "
    text += str(data["balance"])
    text += "</h2>"

    text += "<h2>Warehouse</h2>"

    # show products
    for product in data["warehouse"]:

        amount = data["warehouse"][product]

        text += product
        text += str(amount)
        text += " : "
        text += "<br>"

    # ---------- BALANCE FORM ----------
    text += """
    <h2>Change Balance</h2>

    <form action="/balance" method="POST">

        Value:
        <input type="text" name="value">

        <button type="submit">Save</button>

    </form>
    """

    # ---------- PURCHASE FORM ----------
    text += """
    <h2>Purchase Product</h2>

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
    <h2>Sell Product</h2>

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
def balance():

    try:

        value = float(request.form["value"])

        data["balance"] += value

        text = "Balance changed by "
        text += str(value)

        data["history"].append(text)

        save_data()

    except Exception as e:

        return "Wrong balance value: " + str(e)

    return redirect("/")


# ---------- PURCHASE ----------
@app.route("/purchase", methods=["POST"])
def purchase():

    try:

        product = request.form["product"]

        amount = int(request.form["amount"])

        price = float(request.form["price"])

        total = amount * price

        # check money
        if data["balance"] < total:

            return "Not enough money"

        # update balance
        data["balance"] -= total

        # add product
        if product in data["warehouse"]:

            data["warehouse"][product] += amount

        else:

            data["warehouse"][product] = amount

        text = "Bought "
        text += product

        data["history"].append(text)

        save_data()

    except Exception as e:

        return "Wrong purchase data: " + str(e)

    return redirect("/")


# ---------- SALE ----------
@app.route("/sale", methods=["POST"])
def sale():

    try:

        product = request.form["product"]

        amount = int(request.form["amount"])

        price = float(request.form["price"])

        # check product
        if product not in data["warehouse"]:

            return "Product does not exist"

        # check amount
        if data["warehouse"][product] < amount:

            return "Not enough product"

        # update warehouse
        data["warehouse"][product] -= amount

        # update balance
        data["balance"] += amount * price

        text = "Sold "
        text += product

        data["history"].append(text)

        save_data()

    except Exception as e:

        return "Wrong sale data: " + str(e)

    return redirect("/")


# ---------- HISTORY ----------
@app.route("/history/")
@app.route("/history/<line_from>/<line_to>/")
def history(line_from=None, line_to=None):

    text = "<h1>History</h1>"

    history_list = data["history"]

    # all history
    if line_from is None or line_to is None:

        for line in history_list:

            text += line
            text += "<br>"

    # selected history
    else:

        try:

            line_from = int(line_from)

            line_to = int(line_to)

            selected = history_list[line_from:line_to]

            for line in selected:

                text += line
                text += "<br>"

        except Exception as e:

            return "Wrong history range: " + str(e)

    text += "<br><a href='/'>Back</a>"

    return text


# ---------- START APP ----------
if __name__ == "__main__":

    app.run(debug=True)