#-----Simple accounting system / warehouse with a text database----

import os


class CompanyAccount:
    def __init__(self):
        self.balance = 0.0
        self.warehouse = {}
        self.operations = []

    # --- LOAD DATA ---
    def load_data(self, filename="data.txt"):
        if not os.path.exists(filename):
            print("No saved data found. Starting fresh.")
            return

        try:
            with open(filename, "r") as file:
                data = ast.literal_eval(file.read())

                self.balance = data.get("balance", 0.0)
                self.warehouse = data.get("warehouse", {})
                self.operations = data.get("operations", [])

            print("Data loaded successfully.")

        except Exception:
            print("Error loading data. Starting with empty data.")

    # --- SAVE DATA ---
    def save_data(self, filename="data.txt"):
        data = {
            "balance": self.balance,
            "warehouse": self.warehouse,
            "operations": self.operations }

        try:
            with open(filename, "w") as file:
                file.write(str(data))
            print("Data saved successfully.")

        except Exception:
            print("Error saving data.")

    # --- OTHER FUNCTIONS ---#
    def update_balance(self, amount):
        self.balance += amount
        self.operations.append(f"Balance change: {amount}")

    def record_purchase(self, product, price, quantity):
        total = price * quantity

        if self.balance < total:
            print("Not enough money.")
            return

        self.balance -= total

        if product in self.warehouse:
            self.warehouse[product]["quantity"] += quantity
        else:
            self.warehouse[product] = {"price": price, "quantity": quantity}

        self.operations.append(f"Purchase: {product} x {quantity}")

    def record_sale(self, product, price, quantity):
        if product not in self.warehouse or self.warehouse[product]["quantity"] < quantity:
            print("Not enough product in warehouse.")
            return

        total = price * quantity
        self.balance += total
        self.warehouse[product]["quantity"] -= quantity

        self.operations.append(f"Sale: {product} x {quantity}")

    def show_balance(self):
        print("Balance:", self.balance)

    def show_warehouse(self):
        if not self.warehouse:
            print("Warehouse empty.")
            return

        for a, b in self.warehouse.items():
            print(a, "| price:", b["price"], "| quantity:", b["quantity"])

    def show_operations(self):
        if not self.operations:
            print("No operations.")
            return

        for op in self.operations:
            print(op)


# --- MAIN PROGRAM ---
def main():
    account = CompanyAccount()

    # LOAD DATA AT START
    account.load_data()

    while True:
        print("\nCommands: balance | purchase | sale | warehouse | history | end")
        cmd = input("Enter command: ").lower()

        if cmd == "balance":
            try:
                amount = float(input("Enter amount (+ or -): "))
                account.update_balance(amount)
            except:
                print("Invalid number.")

        elif cmd == "purchase":
            try:
                p = input("Product: ")
                price = float(input("Price: "))
                q = int(input("Quantity: "))
                account.record_purchase(p, price, q)
            except:
                print("Invalid input.")

        elif cmd == "sale":
            try:
                p = input("Product: ")
                price = float(input("Price: "))
                q = int(input("Quantity: "))
                account.record_sale(p, price, q)
            except:
                print("Invalid input.")

        elif cmd == "warehouse":
            account.show_warehouse()

        elif cmd == "history":
            account.show_operations()

        # SAVE DATA BEFORE EXIT
        elif cmd == "end":

            account.save_data()
            print("Program ended.")
            break

        else:
            print("Unknown command.")


main()