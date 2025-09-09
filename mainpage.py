mport json

# Load JSON data
def load_data(filename):
    with open(filename, "r") as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

books = load_data("books.json")
cakes = load_data("cakes.json")
coffee = load_data("coffee.json")
users = load_data("users.json")

cart = []
current_user = None

# Login system
def login():
    global current_user
    email = input("Enter email: ")
    password = input("Enter password: ")
    for user in users:
        if user["email"] == email and user["password"] == password:
            current_user = user
            print(f"\n✅ Welcome, {user['name']}! Role: {user['role']}\n")
            return True
    print("❌ Invalid email or password.")
    return False

# Show menu
def show_menu(items, category):
    print(f"\n--- {category} Menu ---")
    for i, item in enumerate(items, start=1):
        print(f"{i}. {item['name']} - €{item['price']}")
    print()

# Add item to cart
def add_to_cart(items):
    try:
        choice = int(input("Enter item number to add to cart (0 to cancel): "))
        if choice == 0:
            return
        item = items[choice - 1]
        cart.append(item)
        print(f"✅ Added {item['name']} to cart.")
    except (IndexError, ValueError):
        print("Invalid choice. Try again.")

# Review cart with optional discount
def review_cart():
    if not cart:
        print("\n🛒 Your cart is empty.")
        return
    print("\n--- Your Order ---")
    total = sum(item['price'] for item in cart)
    discount = 0

    # Apply loyalty discount for customers
    if current_user['role'] == "customer" and current_user.get("orders_count", 0) >= 10:
        discount = total * 0.1
        print(f"Loyalty discount applied: €{discount:.2f}")

    # Employees can apply extra discount
    if current_user['role'] == "employee":
        apply = input("Apply extra discount? (y/n): ")
        if apply.lower() == "y":
            try:
                extra = float(input("Enter discount %: "))
                discount += total * (extra / 100)
            except ValueError:
                print("Invalid discount, skipping.")

    total_after_discount = total - discount
    for item in cart:
        print(f"- {item['name']} (€{item['price']})")
    print(f"Total: €{total_after_discount:.2f}\n")
    return total_after_discount

# Main app
def main():
    print("📚☕ Welcome to the Bookshop & Cafe! 🍰📖")
    
    # Login loop
    while not login():
        pass

    while True:
        print("\nMain Menu:")
        print("1. View Books")
        print("2. View Cakes")
        print("3. View Coffee")
        print("4. Review Cart")
        print("5. Checkout & Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            show_menu(books, "Books")
            add_to_cart(books)
        elif choice == "2":
            show_menu(cakes, "Cakes")
            add_to_cart(cakes)
        elif choice == "3":
            show_menu(coffee, "Coffee")
            add_to_cart(coffee)
        elif choice == "4":
            review_cart()
        elif choice == "5":
            total = review_cart()
            if current_user['role'] == "customer":
                # Update order count for loyalty
                current_user["orders_count"] = current_user.get("orders_count", 0) + 1
                save_data("users.json", users)
            print("Thanks for your order! Goodbye 👋")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()