from tkinter import *
from tkinter import messagebox # Pop-up messages for user
import tkinter as tk # Shortcut to typing
from tkinter import ttk # Modern style widgets
from PIL import ImageTk, Image  # PIL library for image handling
import pyodbc
import time

def setup_database_connection():
    global connection, cursor
    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};SERVER=X230\\SQLEXPRESS;DATABASE=Cards;UID=Bob;PWD=password;Encrypt=No;')
        cursor = connection.cursor()
    except pyodbc.Error as e:
        print(f"Database connection error: {e}")


def execute_query(query, params=None, commit=False):
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if commit:
            connection.commit()
            return True

        return cursor.fetchall()

    except pyodbc.Error as e:
        print(f"Error executing query: {e}")
        return []


def sign_up():
    pop = Toplevel(window) # pop is a popup window for sign-up
    pop.geometry("400x200")
    pop.title("Sign up page")
    global name_var, address_var, new_email_var
    ttk.Label(pop, text="Enter User Details:").grid(row=1, column=0, pady=10)
    ttk.Label(pop, text="Name:").grid(row=2, column=0, pady=5)
    name_var = tk.StringVar()
    ttk.Entry(pop, textvariable=name_var).grid(row=2, column=1)
    ttk.Label(pop, text="Address:").grid(row=3, column=0, pady=5)
    address_var = tk.StringVar()
    ttk.Entry(pop, textvariable=address_var).grid(row=3, column=1)
    ttk.Label(pop, text="Email:").grid(row=4, column=0, pady=5)
    new_email_var = tk.StringVar()
    ttk.Entry(pop, textvariable=new_email_var).grid(row=4, column=1)
    ttk.Button(pop, text="Submit", command=lambda: submit_new_user(pop)).grid(row=5, column=1, pady=10)

def error_popup(ErrorMsg):
    messagebox.showwarning(title="Error", message=ErrorMsg)

def success_popup(PositiveMsg):
    messagebox.showinfo(title="Information", message=PositiveMsg)

def create_widgets():
    global user_label, email_var, logout_button
    user_label = ttk.Label(window, text="User: Not logged in",background="red")
    user_label.grid(row=0, column=0, pady=20)

    ttk.Label(window, text="Enter email to log-in:").grid(row=1, column=0, pady=10)
    email_var = tk.StringVar()
    ttk.Entry(window, textvariable=email_var).grid(row=1, column=1)

    ttk.Button(window, text="Log-in", command=login).grid(row=2, column=1, pady=10)
    logout_button = ttk.Button(window, text="Log-out", command=logout, state=tk.DISABLED)
    logout_button.grid(row=3, column=1, pady=10)

    ttk.Button(window, text="Sign-up", command=sign_up).grid(row=2, column=0, pady=10)

def card_selection_widgets():
    global occasion_var, occasion_menu, card_menu, quantity_var, size_var, size_menu
    ttk.Label(window, text="Select occasion to load cards:").grid(row=0, column=3, columnspan=2, pady=10)

    occasion_var = tk.StringVar()
    occasion_menu = ttk.Combobox(window, textvariable=occasion_var, state="readonly")
    occasion_menu.grid(row=1, column=3, columnspan=2, pady=5)
    occasion_menu.bind("<<ComboboxSelected>>", on_occasion_change)

    ttk.Label(window, text="Select a card:").grid(row=2, column=3, columnspan=2, pady=10)

    card_menu = tk.Listbox(window, height=5, width=60)  # Adjust width as needed
    card_menu.grid(row=3, column=3, columnspan=2, padx=10, pady=5)
    card_menu.bind("<<ListboxSelect>>", load_card_image)  # Bind selection event

    ttk.Label(window, text="Enter quantity:").grid(row=4, column=3, pady=5)
    quantity_var = tk.IntVar()
    ttk.Entry(window, textvariable=quantity_var).grid(row=4, column=4)

    ttk.Label(window, text="Select card size:").grid(row=5, column=3, pady=5)
    size_var = tk.StringVar()
    size_menu = ttk.Combobox(window, textvariable=size_var, values=["A4", "A5", "A6"], state="readonly")
    size_menu.grid(row=5, column=4)
    ttk.Button(window, text="Add to Orders", command=add_order).grid(row=6, column=3, columnspan=2, pady=10)

def create_image_display():
    global image_label
    image_label = ttk.Label(window, text="Card Image", wraplength=400)
    image_label.grid(row=0, column=6, rowspan=12, padx=20, pady=10,sticky=N+S+W+E)

def login():
    global current_user
    email = email_var.get()
    result = execute_query("SELECT customer_id, name FROM Customers WHERE email = ?", [email])
    if result:
        current_user = result[0]
        quantity_var.set(1)
        user_label.config(text=f"User: {current_user[1]}")
        logout_button.config(state=tk.NORMAL)
        user_label.config(background="lightgreen")
        email_var.set("")  # Clear the entry after successful login
        load_occasions()
        success_popup("Welcome back " + current_user[1])
    else:
        error_popup("Email not found. Try again.")

def logout():
    global current_user
    current_user = None
    user_label.config(text="User: Not logged in",background="red")
    logout_button.config(state=tk.DISABLED)
    occasion_menu['values'] = []
    card_menu.delete(0, tk.END)  # Clear card menu
    quantity_var.set(0)
    size_var.set("A4")
    image_label.config(text="Card Image")

def submit_new_user(pop):
    name = name_var.get()
    address = address_var.get()
    email = new_email_var.get()
    if any(character.isdigit() for character in name):
        error_popup("You cannot have numbers in a name, please try again")
        return
    if len(address) < 10:
        error_popup("Address must be at least 10 characters long, please try again")
        return
    if len(email) < 5:
        error_popup("E-mail address must be at least 5 characters long, please try again")
        return
    if "@" not in email:
        error_popup("You must have an @ in your email address, please try again")
        return
    if name and address and email:
        try:
            execute_query("INSERT INTO Customers (name, address, email) VALUES (?, ?, ?)", [name, address, email], commit=True)
            success_popup("New user submitted.")
            pop.destroy()  # Close the pop window
        except:
            error_popup("ERROR, user not added")

def load_occasions():
    occasions = execute_query("SELECT DISTINCT occasion FROM Cards")
    if occasions:
        occasion_menu['values'] = [occasion[0] for occasion in occasions]
        occasion_var.set(occasions[0][0])
        load_cards()
    else:
        error_popup("No occasions found.")

def load_cards():
    start_time = time.perf_counter()
    occasion = occasion_var.get()
    if occasion:
        cards = execute_query("SELECT Cards.variant_id, Card_Message.message FROM Cards INNER JOIN Card_Message ON Cards.card_message_id=Card_Message.card_message_id WHERE occasion LIKE ?", [occasion])
        if cards:
            card_menu.delete(0, tk.END)
            for card in cards:
                card_menu.insert(tk.END, f"Card ID: {card[0]}, Message: {card[1]}")
        else:
            card_menu.delete(0, tk.END)
            card_menu.insert(tk.END, "No cards available")
            error_popup("No cards found for this occasion.")
    else:
        error_popup("Please select an occasion.")
    execution_time = time.perf_counter()
    print(f"the program took {execution_time - start_time:0.4f} second(s) to load cards list from {occasion}")

def load_card_image(event):
    selected_index = card_menu.curselection()
    if selected_index:
        selected_card = card_menu.get(selected_index)
        if selected_card and selected_card != "No cards available":
            card_id = selected_card.split()[2]  # Extract the variant_id from the selected card string
            card_id = int(card_id[:-1])  # Convert to integer and remove the trailing comma

            occasion = occasion_var.get()

            cards = execute_query("SELECT variant_id FROM Cards WHERE occasion = ?", [occasion])
            if cards:
                # Get the index of the card_id within the list of cards for this occasion
                card_index = [card[0] for card in cards].index(card_id) + 1

                image_path = f"./{occasion}/{card_index}.jpg"  # Construct path to the image

                # Load the image and display
                try:
                    image = Image.open(image_path)
                    image = image.resize((400, 400))  # Resize the image as needed (antialiasing is automatic)
                    photo = ImageTk.PhotoImage(image)

                    # Update image label
                    image_label.config(image=photo, text="")
                    image_label.image = photo  # keep a reference
                except FileNotFoundError:
                    error_popup(f"Image file not found: {image_path}")
                    image_label.config(text="Image not found")
            else:
                image_label.config(text="No cards available")
        else:
            image_label.config(text="No card selected")
    else:
        image_label.config(text="No card selected")

def add_order():
    if not current_user:
        error_popup("Please log in to place an order.")
        return
    quantity = quantity_var.get()
    if quantity < 1 or quantity > 1000:
        error_popup("Quantity must be between 1 and 1000")
        return
    selected_index = card_menu.curselection()
    if selected_index:
        selected_card = card_menu.get(selected_index)
        if selected_card and selected_card != "No cards available":
            card_id = selected_card.split()[2]  # Extract the variant_id from the selected card string
            card_id = int(card_id[:-1])  # Convert to integer and remove the trailing comma

            card_size = size_var.get()
            customer_id = current_user[0]

            execute_query("INSERT INTO Orders (customer_id, variant_id, quantity, card_size) VALUES (?, ?, ?, ?)",
                          [customer_id, card_id, quantity, card_size], commit=True)
            # Get latest order created to get order_id
            order_id = execute_query("SELECT TOP 1 order_id FROM Orders ORDER BY order_id DESC")
            success_popup("Order added successfully. Your order number is: " + str(order_id[0][0]))
        else:
            error_popup("Please select a card.")
    else:
        error_popup("Please select a card.")

def on_occasion_change(event):
    load_cards()

# Main code execution
if __name__ == "__main__":
    current_user = None

    window = tk.Tk()
    window.title("Card Store Application")
    window.state('zoomed')
    window.option_add("*Font","Arial", 20)

    setup_database_connection()
    create_widgets()
    card_selection_widgets()
    create_image_display()

    load_occasions()
    s = ttk.Style()
    # UI styling
    s.theme_use('xpnative')
    # print(s.theme_names(),s.theme_use())

    window.mainloop()