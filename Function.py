
import json

#load and save data

def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def load_json(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f" Error loading '{filename}': {e}")
        return []

#Load initial data
books = load_json("books.json")
cakes = load_json("cakes.json")
coffee = load_json("coffee.json")
users = load_json("users.json")
employees = load_json("employees.json")
1

cart = []
current_user = None


#customer function
def register_user():
    print("\n--- Customer Registration ---")
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = input("Create a password: ")
    address = input("Enter your delivery address: ")

    user_list = load_json("users.json")

    # Check if email exists
    if any(u["email"] == email for u in user_list):
        print(" Email already registered. Please log in.")
        return None

    new_user = {
        "name": name,
        "email": email,
        "password": password,
        "address": address,
        "purchases": 0
    }

    user_list.append(new_user)
    save_json("users.json", user_list)
    print(f" Welcome, {name}! You're now registered.")
    return new_user

def login_customer():
    print("\n--- Customer Login ---")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    user_list = load_json("users.json")
    for user in user_list:
        if user["email"] == email and user["password"] == password:
            print(f" Welcome back, {user['name']}!")
            return user
    print(" Invalid email or password.")
    return None

def update_user_purchases(email):
    user_list = load_json("users.json")
    for user in user_list:
        if user["email"] == email:
            user["purchases"] += 1
            save_json("users.json", user_list)
            return user["purchases"]
    return None

def check_loyalty_discount(user):
    return user["purchases"] != 0 and user["purchases"] % 10 == 0

#Retrive customers by email
def get_user_by_email(email):
    user_list = load_json('users.json')
    for user in user_list:
        if user['email'] == email:
            return user
    return None

def guest_checkout():
    print("\n--- Guest Checkout ---")
    name = input("Enter your name: ")
    address = input("Enter your delivery address: ")
    print(f" Thanks {name}, your order will be delivered to {address}.")
    print("Note: As a guest, you won’t earn loyalty rewards.")

def login_employee():
    print("\n--- Employee Login ---")
    username = input("Enter employee username: ")
    password = input("Enter employee password: ")

    emp_list = load_json("employees.json")
    for emp in emp_list:
        if emp["username"] == username and emp["password"] == password:
            print(f" Employee {username} logged in.")
            return emp
    print(" Invalid credentials.")
    return None


def check_stock():
    print("\n--- Stock Check ---")
    books = load_json("books.json")
    cakes = load_json("cakes.json")
    coffee = load_json("coffee.json")

    print("\nBooks in stock:")
    for b in books:
        print(f"  {b['title']} - {b['stock']} left")

    print("\nCakes in stock:")
    for c in cakes:
        print(f"  {c['name']} - {c['stock']} left")

    print("\nCoffee in stock:")
    for cf in coffee:
        print(f"  {cf['type']} - {cf['stock']} left")


def apply_employee_discount(total_price):
    discount = 0.2  # 20% discount
    return total_price * (1 - discount)


# Main program
# -----------------------------
if __name__ == "__main__":
    print("Welcome to Brew & Books!")
    role = input("Are you a customer or employee? (c/e): ").lower()

    if role == "c":
        print("\n1. Login")
        print("2. Register")
        print("3. Continue as Guest")
        choice = input("Choose an option (1/2/3): ").strip()

        current_user = None
        if choice == "1":
            current_user = login_customer()
        elif choice == "2":
            current_user = register_user()
        elif choice == "3":
            guest_checkout()
        else:
            print(" Invalid choice. Exiting.")
            exit()

        if current_user:  # logged-in customers
            purchases = update_user_purchases(current_user["email"])
            print(f"You now have {purchases} purchases.")
            if check_loyalty_discount(current_user):
                print(" Loyalty discount applied!")
            else:
                print("Keep shopping to earn your next discount!")

    elif role == "e":
        employee = login_employee()
        if employee:
            action = input("Choose action: (1) Check Stock, (2) Apply Discount: ")
            if action == "1":
                check_stock()
            elif action == "2":
                total = float(input("Enter total price: "))
                discounted = apply_employee_discount(total)
                print(f"Discounted price: {discounted:.2f}")
            else:
                print(" Invalid option.")


