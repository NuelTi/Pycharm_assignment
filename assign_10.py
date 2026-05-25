# ---------- DECORATOR ---------- #
def log_operation(func):

    def wrapper(*args, **kwargs):

        print("\n--- Operation Started ---")

        result = func(*args, **kwargs)

        print("--- Operation Finished ---")

        return result

    return wrapper


# ---------- MANAGER CLASS ---------- #
class Manager:

    def __init__(self):

        self.balance = 0
        self.warehouse = {}
        self.history = []

        # dictionary for assign()
        self.actions = {
            "balance": self.change_balance,
            "purchase": self.purchase,
            "sale": self.sale,
            "warehouse": self.show_warehouse,
            "history": self.show_history }

    # ---------- ASSIGN METHOD ----------
    def assign(self, task):

        if task in self.actions:
            return self.actions[task]

        else:
            print("Task does not exist.")
            return None

    # ---------- BALANCE ---------- #
    @log_operation
    def change_balance(self):

        amount = float(input("Enter amount: "))

        self.balance += amount

        self.history.append(f"Balance changed by {amount}")

        print("Current balance:", self.balance)

    # ---------- PURCHASE ---------- #
    @log_operation
    def purchase(self):

        product = input("Product name: ")
        price = float(input("Price: "))
        quantity = int(input("Quantity: "))

        total = price * quantity

        if total > self.balance:
            print("Not enough money.")
            return

        self.balance -= total

        if product in self.warehouse:
            self.warehouse[product] += quantity
        else:
            self.warehouse[product] = quantity

        self.history.append(f"Purchased {quantity} {product}")

        print("Purchase completed.")

    # ---------- SALE ---------- #
    @log_operation
    def sale(self):

        product = input("Product name: ")
        price = float(input("Price: "))
        quantity = int(input("Quantity: "))

        if product not in self.warehouse:
            print("Product not found.")
            return

        if self.warehouse[product] < quantity:
            print("Not enough products. Check another time")
            return

        total = price * quantity

        self.balance += total
        self.warehouse[product] -= quantity

        self.history.append(f"Sold {quantity} {product}")

        print("Sale completed. Thank you! ")

    # ---------- SHOW WAREHOUSE ---------- #
    def show_warehouse(self):

        print("\nWarehouse:")

        if len(self.warehouse) == 0:
            print("Warehouse is empty. Restock! ")

        for product, quantity in self.warehouse.items():
            print(product, "=", quantity)

    # ---------- SHOW HISTORY ---------- #
    @log_operation
    def show_history(self):

        print("\nHistory:")

        if len(self.history) == 0:
            print("No history.")

        for item in self.history:
            print(item)


# ---------- MAIN PROGRAM ---------- #
manager = Manager()

while True:

    print("\nCommands:")
    print("balance")
    print("purchase")
    print("sale")
    print("warehouse")
    print("history")
    print("end")

    command = input("\nEnter command: ")

    if command == "end":
        print("Program ended.")
        break

    action = manager.assign(command)

    if action:
        action()