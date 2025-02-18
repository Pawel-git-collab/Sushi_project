import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Sushi project")
root.geometry("400x400")

sushi_types = ["Nigiri", "Maki", "Sashimi", "Temaki"]
sushi_var = tk.StringVar(value=sushi_types[0])

tk.Label(root, text="Select Sushi Type:").pack()
sushi_menu = tk.OptionMenu(root, sushi_var, *sushi_types)
sushi_menu.pack()

addons = {
    "Wasabi": tk.BooleanVar(),
    "Soy Sauce": tk.BooleanVar(),
    "Pickled Ginger": tk.BooleanVar(),
    "Futomaki Philadelphia": tk.BooleanVar(),
    "Futomaki Griladelphia": tk.BooleanVar()
}

tk.Label(root, text="Choose Add-ons:").pack()
for addon, var in addons.items():
    tk.Checkbutton(root, text=addon, variable=var).pack()

tk.Label(root, text="Enter Quantity:").pack()
quantity_var = tk.IntVar(value=1)
quantity_entry = tk.Entry(root, textvariable=quantity_var)
quantity_entry.pack()


def quantity(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result

    return wrapper


@quantity
def quantity_plus():
    return quantity_var.get()


def bonus_price(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result - 3 if result is not None else None

    return wrapper


@bonus_price
def discount(price):
    return price


def addon_price(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result * 1 if result is not None else None

    return wrapper


def tip(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result + 2 if result is not None else None

    return wrapper


@tip
@addon_price
def extra_charge(price):
    return price


def calculate_price():
    base_prices = {"Nigiri": 3, "Maki": 5, "Sashimi": 7, "Temaki": 6}

    sushi = sushi_var.get()
    selected_addons = [a for a, v in addons.items() if v.get()]

    if quantity_plus() < 1:
        messagebox.showerror("Error", "Quantity must be at least 1")
        return

    total_price = (base_prices[sushi] + len(selected_addons)) * quantity_plus() + extra_charge(0)
    if len(selected_addons) >= 4:
        total_price += discount(0)

    summary = f"Sushi: {sushi}\nAdd-ons: {', '.join(selected_addons) if selected_addons else 'None'}" \
              f"\nQuantity: {quantity_plus()}\nTip: $2 \nTotal: ${total_price:.2f} "
    messagebox.showinfo("Order Summary", summary)

    return total_price


tk.Button(root, text="Place Order", command=calculate_price).pack()

root.mainloop()
