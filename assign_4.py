class CompanyAccount:
    def __init__(self):
        self.balance = 0.0
        self.warehouse = {}
        self.operations = []

    def display_commands(self):
        print("\nAvailable Commands:")
        print("1. balance - Add or subtract from account balance")
        print("2. sale - Record a sale")
        print("3. purchase - Record a purchase")
        print("4. account - Display current account balance")
        print("5. list - Display total inventory in warehouse")
        print("6. warehouse - Check status of a product in warehouse")
        print("7. review - Review recorded operations")
        print("8. end - Terminate the program")

    def update_balance(self, amount):
        self.balance += amount
        operation = f"{'Added' if amount > 0 else 'Subtracted'} ${amount} from account."
        self.operations.append(operation)

    def record_sale(self, product, price, quantity):
        if price < 0 or quantity <= 0:
            print("Price and quantity must be positive.")
            return

        if product not in self.warehouse or self.warehouse[product]['quantity'] < quantity:
            print("Insufficient product quantity in warehouse.")
            return

        total_sale = price * quantity
        self.balance += total_sale
        self.warehouse[product]['quantity'] -= quantity

        operation = f"Sale: {product} - Price: ${price}, Quantity: {quantity}."
        self.operations.append(operation)

    def record_purchase(self, product, price, quantity):
        if price < 0 or quantity <= 0:
            print("Price and quantity must be positive.")
            return

        total_purchase = price * quantity
        if self.balance < total_purchase:
            print("Insufficient funds for this purchase.")
            return

        self.balance -= total_purchase

        if product in self.warehouse:
            self.warehouse[product]['quantity'] += quantity
        else:
            self.warehouse[product] = {'price': price, 'quantity': quantity}

        operation = f"Purchase: {product} - Price: ${price}, Quantity: {quantity}."
        self.operations.append(operation)

    def display_balance(self):
        print(f"Current account balance: ${self.balance:.}")

    def list_inventory(self):
        if not self.warehouse:
            print("Warehouse is empty.")
            return

        print("\nWarehouse Inventory:")
        for product, details in self.warehouse.items():
            print(f"Product: {product}, Price: ${details['price']:.2f}, Quantity: {details['quantity']}")

    def check_warehouse(self, product):
        if product in self.warehouse:
            details = self.warehouse[product]
            print(f"Product: {product}, Price: ${details['price']:.2f}, Quantity: {details['quantity']}")
        else:
            print(f"Product '{product}' not found in warehouse.")

    def review_operations(self, from_index=None, to_index=None):
        if not self.operations:
            print("No operations recorded.")
            return

        from_index = from_index if from_index is not None else 0
        to_index = to_index if to_index is not None else len(self.operations)

        if from_index < 0 or to_index > len(self.operations):
            print("Indices out of range.")
            return

        range_operations = self.operations[from_index:to_index]

        if not range_operations:
            print("No operations found in the specified range.")
            return

        print("\nRecorded Operations:")
        for index, operation in enumerate(range_operations, start=from_index):
            print(f"{index}: {operation}")


def main():
    account = CompanyAccount()
    account.display_commands()

    while True:
        command = input("\nEnter a command: ").strip().lower()

        if command == 'balance':
            try:
                amount = float(input("Enter amount to add/subtract (use negative for subtraction): "))
                account.update_balance(amount)
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        elif command == 'sale':
            try:
                product = input("Enter product name: ")
                price = float(input("Enter product price: "))
                quantity = int(input("Enter quantity sold: "))
                account.record_sale(product, price, quantity)
            except ValueError:
                print("Invalid input.")

        elif command == 'purchase':
            try:
                product = input("Enter product name: ")
                price = float(input("Enter product price: "))
                quantity = int(input("Enter quantity purchased: "))
                account.record_purchase(product, price, quantity)
            except ValueError:
                print("Invalid input.")

        elif command == 'account':
            account.display_balance()

        elif command == 'list':
            account.list_inventory()

        elif command == 'warehouse':
            product = input("Enter product name to check: ")
            account.check_warehouse(product)

        elif command == 'review':
            try:
                from_index = input("Enter 'from' index (leave blank for 0): ")
                to_index = input("Enter 'to' index (leave blank for end): ")

                from_index = int(from_index) if from_index else None
                to_index = int(to_index) if to_index else None

                account.review_operations(from_index, to_index)
            except ValueError:
                print("Invalid index input.")

        elif command == 'end':
            print("Program terminated.")
            break

        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()