"""
This script creates a Tkinter-based GUI application for managing food-related data inputs.

The application allows the user to input various attributes of food items, such as:
- Product name
- Quantity
- Food group (via radio buttons)
- Nutritional information (via checkboxes for dietary options like Vegan, Vegetarian, etc.)
- Expiration date
- Date added

Additionally, the application displays agreement dialogs for End User License Agreement (EULA), Privacy Policy, and Terms and Conditions before proceeding to the main window.

Key Functions:
- `main_window()`: Initializes and configures the main application window.
- `create_buttons()`: Sets up buttons for navigating or executing certain features within the app.
- `check_agreements()`: Ensures the user agrees to the legal terms before using the application.
- `main()`: The entry point for starting the application, calling the main Tkinter event loop.

Usage:
    Run the script to launch the GUI, and follow the prompts to input food-related data.
"""

import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import Label
from PIL import Image, ImageTk
import webbrowser
import os
import re
import sys
import sqlite3
import sys
import bcrypt

# Constants
HEIGHT = 3
WIDTH = 20

# Colors
LIGHT_BG = "alice blue"  # Light mode color for root, frames, etc.
DARK_BG = "gray20"      # Dark mode color for root, frames, etc.
FRAME_LIGHT_COLOR = "white"  # Light mode color for frames
FRAME_DARK_COLOR = "gray15"     # Dark mode color for frames
TEXT_LIGHT_COLOR = "black"  # Text color for light theme
TEXT_DARK_COLOR = "dodger blue"  # Text color for dark theme

# Checks if the script is running in a "frozen" state
if getattr(sys, 'frozen', False):
    CURRENT_DIR = os.path.dirname(sys.executable)
else:
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Button Text
BUTTON_TEXTS = ["ADD", "UPDATE", "DELETE", "SEARCH"]

# Ensure you have a list of food groups
food_groups = ["Dairy", "Fruits", "Vegetables", "Grains", "Protein", "Other"]

# JSON Path
PROD_JSON = os.path.join(CURRENT_DIR, "fridge_products_full.json")

# User Agreement Path
EULA_AGREEMENT = os.path.join(CURRENT_DIR, "EULA.html")
PRIVACY_POLICY = os.path.join(CURRENT_DIR, "Privacy_Policy.html")
TERMS_CONDITIONS = os.path.join(CURRENT_DIR, "Terms_Conditions.html")
VERIFICATION = os.path.join(CURRENT_DIR, "agreement.html")

# Userid to identify user currently active
global logged_in_user_id
logged_in_user_id = None

# hopefully fixes a problem
root = None

# Connect to the database (if it doesn't exist, it will be created)
def connect_db(db_name='products.db'):
    conn = sqlite3.connect(db_name)
    return conn

# Function to create a 'products' table if it doesn't already exist
def create_products(conn):
    with conn:
        #conn.execute('''DROP TABLE IF EXISTS products''')
        conn.execute('''CREATE TABLE IF NOT EXISTS products (
                            name TEXT,
                            quantity INTEGER,
                            "group" INTEGER,
                            expiration DATE,
                            "add" DATE,
                            user_id TEXT,
                            vegetarian BOOLEAN,
                            vegan BOOLEAN,
                            gluten BOOLEAN,
                            lactose BOOLEAN,
                            eggs BOOLEAN,
                            nuts BOOLEAN,
                            halal BOOLEAN,
                            kosher BOOLEAN,
                            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE)''')

# Function to fill products table
def fill_products(conn):
    with conn:
        conn.execute('''INSERT INTO products (name, quantity, "group", expiration, "add", user_id, vegetarian, vegan, gluten, lactose, eggs, nuts, halal, kosher) VALUES
                    ('Eggs', 3, 5, '2024/10/22', '2024/09/24', '1', 0, 0, 0, 0, 1, 0, 0, 0),
                    ('Cheese', 4, 1, '2024/10/01', '2024/09/24', '1', 0, 0, 0, 1, 0, 0, 0, 0),
                    ('Butter', 3, 1, '2025/02/24', '2024/09/24', '1', 0, 0, 0, 1, 0, 0, 0, 0),
                    ('Yogurt', 6, 1, '2024/10/01', '2024/09/24', '1', 1, 0, 0, 1, 0, 0, 0, 0),
                    ('Lettuce', 8, 3, '2024/10/04', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Carrots', 9, 3, '2024/10/15', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Tomatoes', 1, 3, '2024/09/29', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Apples', 8, 2, '2024/10/01', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Oranges', 4, 2, '2024/10/01', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Chicken', 3, 5, '2024/09/26', '2024/09/24', '1', 0, 0, 0, 0, 0, 0, 1, 1),
                    ('Beef', 2, 5, '2024/09/27', '2024/09/24', '1', 0, 0, 0, 0, 0, 0, 1, 1),
                    ('Pork', 10, 5, '2024/09/26', '2024/09/24', '1', 0, 0, 0, 0, 0, 0, 0, 0),
                    ('Tofu', 8, 5, '2024/10/01', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Almonds', 9, 4, '2026/09/24', '2024/09/24', '1', 1, 1, 0, 0, 0, 1, 0, 0),
                    ('Peanut Butter', 4, 5, '2025/03/24', '2024/09/24', '1', 1, 1, 0, 0, 0, 1, 0, 0),
                    ('Orange Juice', 2, 6, '2024/10/02', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Soda', 3, 6, '2025/06/24', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Spinach', 6, 3, '2024/10/01', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Broccoli', 1, 3, '2024/09/29', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Cucumber', 6, 3, '2024/10/08', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Bread', 10, 4, '2024/09/26', '2024/09/24', '1', 1, 1, 1, 0, 1, 0, 0, 0),
                    ('Jam', 5, 2, '2025/04/24', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Hummus', 2, 4, '2024/11/24', '2024/09/24', '1', 1, 1, 0, 0, 0, 1, 1, 1),
                    ('Olives', 4, 3, '2026/09/24', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Pickles', 3, 3, '2024/12/07', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Pasta', 6, 4, '2026/09/24', '2024/09/24', '1', 1, 1, 1, 0, 0, 0, 0, 0),
                    ('Rice', 3, 4, '2026/09/24', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Mushrooms', 8, 3, '2024/10/04', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Bell Peppers', 10, 3, '2026/09/24', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Salmon', 2, 5, '2024/09/28', '2024/09/24', '1', 0, 0, 0, 0, 0, 0, 0, 0),
                    ('Tuna', 7, 5, '2029/09/24', '2024/09/24', '1', 0, 0, 0, 0, 0, 0, 0, 0),
                    ('Shrimp', 5, 5, '2024/12/24', '2024/09/24', '1', 0, 0, 0, 0, 0, 0, 0, 0),
                    ('Sausage', 2, 5, '2024/09/28', '2024/09/24', '1', 0, 0, 0, 0, 0, 0, 0, 0),
                    ('Bacon', 5, 5, '2024/10/01', '2024/09/24', '1', 0, 0, 0, 0, 0, 0, 0, 0),
                    ('Frozen Pizza', 6, 6, '2026/03/24', '2024/09/24', '1', 0, 0, 0, 0, 0, 0, 0, 0),
                    ('Ice Cream', 8, 1, '2024/11/05', '2024/09/24', '1', 1, 0, 0, 1, 1, 1, 0, 0),
                    ('Nut Butter', 8, 5, '2024/11/24', '2024/09/24', '1', 0, 1, 0, 1, 0, 1, 1, 1),
                    ('Mayonnaise', 3, 1, '2024/10/24', '2024/09/24', '1', 0, 0, 0, 1, 0, 0, 0, 0),
                    ('Mustard', 4, 6, '2025/09/24', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Ketchup', 2, 6, '2025/03/24', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Soy Sauce', 6, 6, '2025/03/24', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Grapes', 4, 2, '2024/10/08', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Bananas', 6, 2, '2024/09/29', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Potatoes', 7, 3, '2024/11/24', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Onions', 3, 3, '2024/12/24', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Garlic', 10, 3, '2025/03/24', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Peas', 5, 3, '2024/09/27', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Corn', 10, 3, '2024/09/27', '2024/09/24', '1', 1, 1, 0, 0, 0, 0, 0, 0),
                    ('Snap Peas', 7, 3, '2024/10/02', '2024/09/29', '1', 1, 1, 0, 0, 0, 0, 1, 1);''')

# Function to create a 'users' table if it doesn't already exist        
def create_users(conn):
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email TEXT NOT NULL UNIQUE,
                            username TEXT NOT NULL UNIQUE,
                            password_hash TEXT NOT NULL)''')

# Class for handling products in the database
class Product:
    def __init__(self, name, quantity, group, expiration, add, user, info=None):
        self.name = name
        self.quantity = quantity
        self.group = group
        self.expiration = expiration
        self.add = add
        self.user = user
        self.info = info if info else {
            "Vegetarian": 0,
            "Vegan": 0,
            "Gluten": 0,
            "Lactose": 0,
            "Eggs": 0,
            "Nuts": 0,
            "Halal": 0,
            "Kosher": 0
        }

    # Add a new product to the database
    def add_product(self, conn):
        with conn:
            conn.execute('''INSERT INTO products 
                            (name, quantity, "group", expiration, "add", user, vegetarian, vegan, gluten, lactose, eggs, nuts, halal, kosher)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                         (self.name, self.quantity, self.group, self.expiration, self.add, self.user, 
                          self.info["Vegetarian"], self.info["Vegan"], self.info["Gluten"], self.info["Lactose"],
                          self.info["Eggs"], self.info["Nuts"], self.info["Halal"], self.info["Kosher"]))

    # Load a product from the database by name and expiration
    @staticmethod
    def load_product(conn, name, expiration):
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE name = ? AND expiration = ?", (name, expiration))
        row = cur.fetchone()
        if row:
            info = {
                "Vegetarian": row[6],
                "Vegan": row[7],
                "Gluten": row[8],
                "Lactose": row[9],
                "Eggs": row[10],
                "Nuts": row[11],
                "Halal": row[12],
                "Kosher": row[13]
            }
            return Product(row[0], row[1], row[2], row[3], row[4], row[5], info)
        else:
            return None

    # Update a product in the database
    def update_product(self, conn):
        with conn:
            conn.execute('''UPDATE products SET 
                            quantity = ?, "group" = ?, "add" = ?, user = ?, vegetarian = ?, vegan = ?, gluten = ?, lactose = ?, eggs = ?, nuts = ?, halal = ?, kosher = ?
                            WHERE name = ? AND expiration = ?''',
                         (self.quantity, self.group, self.add, self.user, 
                          self.info["Vegetarian"], self.info["Vegan"], self.info["Gluten"], self.info["Lactose"],
                          self.info["Eggs"], self.info["Nuts"], self.info["Halal"], self.info["Kosher"],
                          self.name, self.expiration))

    # Delete a product from the database
    @staticmethod
    def delete_product(conn, name, expiration):
        with conn:
            conn.execute("DELETE FROM products WHERE name = ? AND expiration = ?", (name, expiration))

    # Search for products in the database by name (partial search)
    @staticmethod
    def search_product(conn, search_term):
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + search_term + '%',))
        rows = cur.fetchall()
        return rows

# Simple login screen
def login_window():
    login_root = tk.Tk()
    login_root.title("FoodConnect")
    login_root.geometry('700x600')

    # Ensure that closing the window exits the program
    def on_close():
        sys.exit()  # Exit the entire application if login window is closed

    def on_register(): 
        login_root.iconify()
        sign_up()

    login_root.protocol("WM_DELETE_WINDOW", on_close)  # Handle window close event

    conn = connect_db()  # Connect to the database
    create_users(conn)   # Ensure users table exists

    # Show application logo
    image = Image.open('FC_LOGO.png')
    image = ImageTk.PhotoImage(image)

    image_label = tk.Label(login_root, image=image)
    image_label.pack()

    # Labels and entries for both login and sign-up
    tk.Label(login_root, text="Username:").pack(pady=5)
    username_entry = tk.Entry(login_root)
    username_entry.pack(pady=5)

    tk.Label(login_root, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_root, show='*')
    password_entry.pack(pady=5)

    # A status label to display login or sign-up messages
    status_label = tk.Label(login_root, text="")
    status_label.pack(pady=5)

    # Function to handle login
    def login():
        username = username_entry.get()
        password = password_entry.get()

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT password_hash, user_id FROM users WHERE username = ?", (username,))
        row = cur.fetchone()

        if row and bcrypt.checkpw(password.encode(), row[0]):
            global logged_in_user_id
            logged_in_user_id = row[1]  # Store the logged-in user's ID
            status_label.config(text="Login successful!", fg="green")
            login_root.after(1000, login_root.destroy)  # Close login window after success
            main()  # Launch the main app after successful login
        else:
            status_label.config(text="Invalid username or password", fg="red")

    # Function to handle sign-up
    def sign_up():

        def on_close_register():
            result = messagebox.askquestion('Exit',"Are you sure you wish to cancel?")
            if result == 'yes':
                registration.destroy()
                login_root.deiconify()

        def on_submit():
            email_pattern = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
            email = email_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            
            # Validate user input
            if not username or not password or not email or not confirm_password:
                messagebox.showerror("Missing fields!", "All fields are required!")
            elif not re.match(email_pattern, email):
                messagebox.showerror("Invalid Email!", "Enter a valid email address!")
            elif password != confirm_password:
                messagebox.showerror("Password mismatch!", "Passwords do not match!")
            else:                
                conn = connect_db()
                cur = conn.cursor()

                # Check if the username already exists
                cur.execute("SELECT * FROM users WHERE username = ?", (username,))
                if cur.fetchone():
                    messagebox.showerror("Username!", "Username already exists!")
                else:
                    # Hash the password before storing it
                    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

                    # Insert the new user into the database
                    cur.execute("INSERT INTO users (email, username, password_hash) VALUES (?, ?, ?)", (email, username, hashed_password))
                    conn.commit()

                    messagebox.showinfo("Success!", "Account created successfully!")
                    registration.destroy()
                    login_root.deiconify()
                
        
        # Create the registration window
        registration = tk.Tk()
        registration.title("FoodConnect")
        registration.geometry("300x400")
        registration.protocol("WM_DELETE_WINDOW", on_close_register)

        # Label and entry for Email
        email_label = tk.Label(registration, text="Email:")
        email_label.pack(pady=5)

        email_entry = tk.Entry(registration)
        email_entry.pack(pady=5)

        # Label and entry for username
        username_label = tk.Label(registration, text="Username:")
        username_label.pack(pady=5)

        username_entry = tk.Entry(registration)
        username_entry.pack(pady=5)

        # Label and entry for password
        password_label = tk.Label(registration, text="Password:")
        password_label.pack(pady=5)

        password_entry = tk.Entry(registration, show='*')
        password_entry.pack(pady=5)

        confirm_password_label = tk.Label(registration, text="Confirm Password:")
        confirm_password_label.pack(pady=5)

        confirm_password_entry = tk.Entry(registration, show='*')
        confirm_password_entry.pack(pady=5)

        # Submit button
        submit_button = tk.Button(registration, text="Submit", command=on_submit)
        submit_button.pack(pady=20)

        # Cancel Button
        cancel_button = tk.Button(registration, text="Cancel", command=on_close_register)
        cancel_button.pack(pady=5)

    # Buttons for login and sign-up
    tk.Button(login_root, text="Login", command=login).pack(side=tk.TOP, padx=20, pady=10)
    tk.Button(login_root, text="Register", command=on_register).pack(side=tk.TOP, padx=20, pady=10)

    login_root.mainloop()

# Main Window
def main_window():
    """
    Initializes and configures the main window for the Tkinter application.

    This function creates the root window with a title "FoodConnect" and 
    sets the dimensions of the window to 600x800 pixels.

    Returns:
        Tk: The root Tkinter window object that serves as the main application window.
    """
    global root
    root = tk.Tk()
    root.title("FoodConnect")
    root.geometry('600x800')
    root.config(bg=LIGHT_BG)

    light = Image.open(os.path.join(CURRENT_DIR, "light.png"))
    dark = Image.open(os.path.join(CURRENT_DIR, "dark.png"))
    root.light_image = ImageTk.PhotoImage(light, master=root)
    root.dark_image = ImageTk.PhotoImage(dark, master=root)

    switch_value = True

    # Frames must be created before the toggle function
    frame = tk.Frame(root, bg=FRAME_LIGHT_COLOR)
    frame.pack(side=tk.TOP, pady=20)
    
    panel = tk.Frame(root, bg=FRAME_LIGHT_COLOR)
    panel.pack(side=tk.TOP, pady=20)

    def apply_theme(widget, bg_color, fg_color):
        """
        Apply the background and foreground colors to the widget and all its children recursively.
        """
        # Apply background color
        widget.config(bg=bg_color)

        # Apply text color for widgets that support the 'fg' option
        if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.Text, tk.Checkbutton, tk.Radiobutton)):
            widget.config(fg=fg_color)
            
            # Set additional options for Checkbutton and Radiobutton widgets
            if isinstance(widget, (tk.Checkbutton, tk.Radiobutton)):
                widget.config(selectcolor=bg_color, activeforeground=fg_color)

        # Apply Listbox-specific colors
        elif isinstance(widget, tk.Listbox):
            widget.config(bg=bg_color, fg=fg_color)

        # Recursively set the colors for each child widget
        for child in widget.winfo_children():
            apply_theme(child, bg_color, fg_color)

    def toggle():
        nonlocal switch_value

        # Dark theme
        if switch_value:
            switch.config(image=root.dark_image, bg=DARK_BG, activebackground=DARK_BG)
            root.config(bg=DARK_BG)
            apply_theme(panel, FRAME_DARK_COLOR, TEXT_DARK_COLOR)
            apply_theme(frame, FRAME_DARK_COLOR, TEXT_DARK_COLOR)
            switch_value = False
        
        # Light theme
        else:
            switch.config(image=root.light_image, bg=LIGHT_BG, activebackground=LIGHT_BG)
            root.config(bg=LIGHT_BG)
            apply_theme(panel, FRAME_LIGHT_COLOR, TEXT_LIGHT_COLOR)
            apply_theme(frame, FRAME_LIGHT_COLOR, TEXT_LIGHT_COLOR)
            switch_value = True

    # Use root.light_image as the initial image for the switch button
    switch = tk.Button(root, image=root.light_image, bd=0, bg=LIGHT_BG, activebackground=LIGHT_BG, command=toggle)
    switch.place(relx=0.9, rely=0.9, anchor='se')

    # Pass switch_value to create_buttons
    create_buttons(frame, panel, switch_value) 

    return root

# Button Clicked
def on_button_click(clicked_index, buttons, panel):
    """
    Handles the event when a button is clicked in the GUI.

    This function iterates over a list of buttons and adjusts the size of the clicked button. 
    It ensures that the button corresponding to the `clicked_index` is highlighted (or resized) 
    while maintaining a consistent size for all other buttons. Once the button is clicked, it 
    calls the `create_panel` function to update the content of the specified panel based on 
    the index of the clicked button.

    Args:
        clicked_index (int): The index of the button that was clicked.
        buttons (list): A list of Tkinter button objects.
        panel (Tkinter Frame): The frame or panel where the content is displayed after a button click.

    Returns:
        None
    """
    # Iterating over all buttons, find the one that is clicked, adjust size
    for index, button in enumerate(buttons):
        if index == clicked_index:
            button.config(height=HEIGHT, width=WIDTH)
        else:
            button.config(height=HEIGHT, width=WIDTH)

    create_panel(clicked_index, panel)  # Call create_panel with the clicked index

# Create the Buttons
def create_buttons(frame, panel, switch_value): 
    """
    Creates a set of buttons within a specified frame and assigns click functionality.

    This function generates a series of buttons based on predefined text labels (from `BUTTON_TEXTS`), 
    places them in the specified frame, and binds each button to trigger the `on_button_click` 
    function when clicked. The buttons are arranged in a single row within the frame. By default, 
    the first button is given a preset size.

    Args:
        frame (Tkinter Frame): The frame where the buttons will be placed.
        panel (Tkinter Frame): The panel that will be updated based on button clicks.

    Returns:
        list: A list of Tkinter button objects created within the frame.
    """
    buttons = []
    for i, text in enumerate(BUTTON_TEXTS):
        # Set the button color based on the current theme
        button_color = "lightgreen" if switch_value else "darkgreen" 
        btn = tk.Button(frame, bg=button_color, text=text, height=HEIGHT, width=WIDTH,
                        command=lambda i=i: on_button_click(i, buttons, panel))
        btn.grid(row=1, column=i, sticky="s")
        buttons.append(btn)

    # Set the default button
    buttons[0].config(height=HEIGHT, width=WIDTH)  
    return buttons

# Button Panel
def create_panel(index, panel):
    """
    Updates the content of the given panel based on the selected button index.

    This function clears the existing content of the panel by destroying all its widgets. 
    It then dynamically updates the panel's content based on the `index` of the selected button. 
    Depending on the index, it calls one of the following functions:
    - `add_prod(panel)`: Adds a new product (index 0).
    - `update_prod(panel)`: Updates an existing product (index 1).
    - `delete_prod(panel)`: Deletes an existing product (index 2).
    - `search_prod(panel)`: Searches for a product (for any other index).

    Args:
        index (int): The index of the clicked button, determining the panel content.
        panel (Tkinter Frame): The panel where the dynamic content is displayed.

    Returns:
        None
    """
    for widget in panel.winfo_children():
        widget.destroy()
    if index == 0:      # Add new product
        add_prod(panel)
    elif index == 1:    # Update existing product
        update_prod(panel)
    elif index == 2:    # Delete existing product
        delete_prod(panel)
    else:               # Search for product
        search_prod(panel)

# Check for Special Characters
def check_special_chars(entry):
    """
    Validates the content of a Tkinter entry widget for special characters.

    This function retrieves the current content of the provided `entry` widget and uses a 
    regular expression to check for the presence of special characters (anything that is 
    not alphanumeric or a space). If any special characters are found, the background color 
    of the entry widget is changed to light coral to indicate invalid input. If no special 
    characters are found, the background is reset to white.

    Args:
        entry (Tkinter Entry): The entry widget whose content is being validated.

    Returns:
        None
    """
    content = entry.get()
    # Check if there are any special characters in the content using regex
    if re.search(r'[^a-zA-Z0-9 ]', content):  # Matches anything not alphanumeric or space
        entry.config(bg="lightcoral")
    else:
        entry.config(bg="white")

# Formating for date MM/DD/YY
def format_date(entry_widget, event=None):
    """
    Formats the content of a Tkinter entry widget for date.

    This function retrieves the current content of the provided `entry` widget and uses a 
    regular expression to check for the presence of non digit characters and incorrect formatting 
    of the date. If any special characters, letters or incorrect format are found, the background 
    color of the entry widget is changed to light coral to indicate invalid input. If no special 
    characters are found, the background is reset to white. Once the `entry` has been made the 
    formatting will be updated to match: MM/DD/YY

    Args:
        entry (Tkinter Entry): The entry widget whose content is being validated and formatted.

    Returns:
        None
    """
    content = entry_widget.get()
    clean_content = content.replace("-", "").replace("/", "")

    if len(clean_content) == 6 and clean_content.isdigit():
        formatted_date = clean_content[:2] + "/" + clean_content[2:4] + "/" + clean_content[4:]
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, formatted_date)
        entry_widget.config(bg="white")
    elif content:
        entry_widget.config(bg="lightcoral")

# Check Quantity is larger than 0 and an integer
def validate_qty(qty):
    """
    Validates a quantity value.

    This function checks whether the provided `qty` is a string representing a digit and 
    ensures it is greater than 0.

    Args:
        entry (Tkinter Entry): The quantity value to be validated.

    Returns:
        bool: True if the quantity is a positive integer, False otherwise.
    """
    return qty.isdigit() and int(qty) > 0

# Load Products
def load_prod(conn):
    """
    Loads the list of products from the database for the logged-in user.

    Args:
        conn (sqlite3.Connection): SQLite connection object.

    Returns:
        list: A list of products from the database.
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE user_id = ?", (logged_in_user_id,))
    rows = cur.fetchall()

    # Format the results into a list of dictionaries for easier usage in the GUI
    products = []
    for row in rows:
        product = {
            "Name": row[0],
            "Quantity": row[1],
            "Group": row[2],
            "Exp": row[3],
            "Add": row[4],
            "User": logged_in_user_id,
            "Info": {
                "Vegetarian": row[6],
                "Vegan": row[7],
                "Gluten": row[8],
                "Lactose": row[9],
                "Eggs": row[10],
                "Nuts": row[11],
                "Halal": row[12],
                "Kosher": row[13]
            }
        }
        products.append(product)
    
    return products

# Add New Product
def add_prod(panel):
    """
    Creates a form in the provided panel to add a new product with various details.

    This function generates a set of input fields in a `sub_frame` within the `panel` 
    for adding a new product. The form includes:
    - Product Name (text entry with validation for special characters)
    - Quantity (positive integer validation)
    - Food Group (radio buttons for selection)
    - Nutritional Information (checkboxes for various dietary restrictions)
    - Expiration Date (formatted as MM/DD/YY)
    - Date Added (formatted as MM/DD/YY)
    - User Name (text entry with validation for special characters)

    Upon submission, the product details are validated and stored in a JSON file (`PROD_JSON`).
    If the quantity is invalid, an error message is shown. After successfully adding the product, 
    a success message is displayed and the form is cleared.

    Args:
        panel (Tkinter Frame): The frame where the form will be displayed.

    Returns:
        None
    """
    global root

    # Set up for the Add Panel
    sub_frame = tk.Frame(panel, bg=panel.cget('bg'))
    sub_frame.pack(pady=20)

    instructions = tk.Label(sub_frame, text="Fill in the information for the NEW product.", bg=sub_frame.cget('bg'))
    instructions.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

    # Product Name Input
    prod_name_label = tk.Label(sub_frame, text="Product Name:", bg=sub_frame.cget('bg'))
    prod_name_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
    prod_name_input = tk.Entry(sub_frame)
    prod_name_input.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    prod_name_input.bind("<FocusOut>", lambda event, entry=prod_name_input: check_special_chars(entry))

    # Quantity Input
    qty_label = tk.Label(sub_frame, text="Quantity:", bg=sub_frame.cget('bg'))
    qty_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
    qty_input = tk.Entry(sub_frame)
    qty_input.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

    # Food Group (Radio buttons)
    group_label = tk.Label(sub_frame, text="Food Group:", bg=sub_frame.cget('bg'))
    group_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

    var1 = tk.IntVar(master=root)
    food_groups = ["Dairy", "Fruits", "Vegetables", "Grains", "Protein", "Other"]
    for i, group in enumerate(food_groups, start=1):
        radio = tk.Radiobutton(sub_frame, text=group, variable=var1, value=i, bg=sub_frame.cget('bg'))
        radio.grid(row=3 + (i-1)//2, column=1 + (i-1)%2, padx=5, pady=5, sticky=tk.W)

    # Nutritional Information (Check buttons)
    info_label = tk.Label(sub_frame, text="Nutritional Information:", bg=sub_frame.cget('bg'))
    info_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)

    nutrition_vars = {
        "Vegetarian": tk.IntVar(master=root),
        "Vegan": tk.IntVar(master=root),
        "Gluten": tk.IntVar(master=root),
        "Lactose": tk.IntVar(master=root),
        "Eggs": tk.IntVar(master=root),
        "Nuts": tk.IntVar(master=root),
        "Halal": tk.IntVar(master=root),
        "Kosher": tk.IntVar(master=root)
    }

    for i, (text, var) in enumerate(nutrition_vars.items(), start=1):
        check = tk.Checkbutton(sub_frame, text=text, variable=var, onvalue=1, offvalue=0, bg=sub_frame.cget('bg'))
        check.grid(row=6 + (i-1)//2, column=1 + (i-1)%2, padx=5, pady=5, sticky=tk.W)

    # Experation Date
    exp_date_label = tk.Label(sub_frame, text="Exp Date (MM/DD/YY):", bg=sub_frame.cget('bg'))
    exp_date_label.grid(row=10, column=0, padx=5, pady=5, sticky=tk.E)
    exp_date_entry = tk.Entry(sub_frame)
    exp_date_entry.grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)
    exp_date_entry.bind("<FocusOut>", lambda event: format_date(exp_date_entry))

    # Date Added
    add_date_label = tk.Label(sub_frame, text="Date Added (MM/DD/YY):", bg=sub_frame.cget('bg'))
    add_date_label.grid(row=11, column=0, padx=5, pady=5, sticky=tk.E)
    add_date_entry = tk.Entry(sub_frame)
    add_date_entry.grid(row=11, column=1, padx=5, pady=5, sticky=tk.W)
    add_date_entry.bind("<FocusOut>", lambda event: format_date(add_date_entry))

    # User Name Input
    user_name_label = tk.Label(sub_frame, text="User Name:", bg=sub_frame.cget('bg'))
    user_name_label.grid(row=12, column=0, padx=5, pady=5, sticky=tk.E)
    user_name_input = tk.Entry(sub_frame)
    user_name_input.grid(row=12, column=1, padx=5, pady=5, sticky=tk.W)
    user_name_input.bind("<FocusOut>", lambda event, entry=user_name_input: check_special_chars(entry))

    # Collect and Store Data
    def store():
        # Collect the data from the form
        name = prod_name_input.get()
        quantity = qty_input.get()
        group = var1.get()
        exp_date = exp_date_entry.get()
        add_date = add_date_entry.get()

        # Nutritional Information
        nutritional_info = {
            "Vegetarian": nutrition_vars["Vegetarian"].get(),
            "Vegan": nutrition_vars["Vegan"].get(),
            "Gluten": nutrition_vars["Gluten"].get(),
            "Lactose": nutrition_vars["Lactose"].get(),
            "Eggs": nutrition_vars["Eggs"].get(),
            "Nuts": nutrition_vars["Nuts"].get(),
            "Halal": nutrition_vars["Halal"].get(),
            "Kosher": nutrition_vars["Kosher"].get(),
        }

        # Validate quantity
        if not validate_qty(quantity):
            messagebox.showerror("Input Error", "Quantity must be a positive number.")
            return

        conn = connect_db()
        cur = conn.cursor()

        # Insert into the database
        cur.execute('''INSERT INTO products 
                       (name, quantity, "group", expiration, "add", user_id, vegetarian, vegan, gluten, lactose, eggs, nuts, halal, kosher)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (name, quantity, group, exp_date, add_date, logged_in_user_id,
                     nutritional_info["Vegetarian"], nutritional_info["Vegan"], nutritional_info["Gluten"],
                     nutritional_info["Lactose"], nutritional_info["Eggs"], nutritional_info["Nuts"],
                     nutritional_info["Halal"], nutritional_info["Kosher"]))

        conn.commit()
        messagebox.showinfo("Success", "Product added successfully!")
        sub_frame.destroy()

    submit_btn = tk.Button(sub_frame, text="Submit", command=store)
    submit_btn.grid(row=13, column=1, padx=5, pady=5)

    return

# Update Existing Product 
def update_prod(panel):
    """
    Provides a GUI form to update an existing product's details.

    This function creates a split-screen interface in the provided `panel`. On the left side, it 
    displays a list of existing products loaded from a JSON file. The user can select a product from 
    the list and the form on the right side will be populated with the product's details, including:
    - Product Name
    - Quantity
    - Food Group (via radio buttons)
    - Nutritional Information (via checkboxes)
    - Expiration Date (formatted as MM/DD/YY)
    - Date Added (formatted as MM/DD/YY)

    The user can edit the product's details and submit the updates. The changes are saved back 
    to the JSON file. If the product is not found, an error message is shown.

    Args:
        panel (Tkinter Frame): The frame where the form and product list will be displayed.

    Returns:
        None
    """
    products = load_prod(connect_db())

    # Looks for the product
    def get_prod_data(name, exp, products):
        for product in products:
            if product["Name"] == name and product["Exp"] == exp:
                return product
        return None  # Return None if product is not found


    # Get the selected product name from the listbox
    def on_select(event):
        selection = event.widget.curselection()
        if selection:
            selected_name = event.widget.get(selection[0])  # Get the selected name

    # Prints the selected product's information 
    def grab_data():
        selection = users_listbox.curselection()  # Get current selection
        if not selection:
            messagebox.showwarning("No Selection", "Please select a product to grab.")
            return
        
        selected = users_listbox.get(selection[0])  # Get the selected name
        selected = selected.split(" ")
        product = get_prod_data(selected[0], selected[1], products)
        
        if product:
            # Populate the text field with the product's name
            prod_name_input.delete(0, tk.END)
            prod_name_input.insert(0, product["Name"])
            prod_name_input.config(state='readonly')

            # Populate the text field with the product's qty
            qty_input.delete(0, tk.END)
            qty_input.insert(0, product["Quantity"])

            # Set the food group radio button
            var1.set(product["Group"])

            # Set the check buttons for nutritional information
            info = product.get("Info", {})
            veg_var.set(info.get("Vegetarian", 0))
            vegan_var.set(info.get("Vegan", 0))
            gluten_var.set(info.get("Gluten", 0))
            lactose_var.set(info.get("Lactose", 0))
            eggs_var.set(info.get("Eggs", 0))
            nuts_var.set(info.get("Nuts", 0))
            halal_var.set(info.get("Halal", 0))
            kosher_var.set(info.get("Kosher", 0))

            # Set expiration date
            date_entry.delete(0, tk.END)
            date_entry.insert(0, product["Exp"])
            date_entry.config(state='readonly')

            # Set the date added
            add_entry.delete(0, tk.END)
            add_entry.insert(0, product["Add"])

            # Populate the text field with the product's user
            user_name_input.delete(0, tk.END)
            user_name_input.insert(0, product["User"])

    # Stores the updated product into the JSON file with its updates    
    def store():
        name = prod_name_input.get()
        quantity = qty_input.get()
        group = var1.get()
        exp_date = date_entry.get()
        add_date = add_entry.get()

        nutritional_info = {
            "Vegetarian": veg_var.get(),
            "Vegan": vegan_var.get(),
            "Gluten": gluten_var.get(),
            "Lactose": lactose_var.get(),
            "Eggs": eggs_var.get(),
            "Nuts": nuts_var.get(),
            "Halal": halal_var.get(),
            "Kosher": kosher_var.get(),
        }

        conn = connect_db()
        cur = conn.cursor()

        # Update the product in the database
        cur.execute('''UPDATE products 
                       SET quantity = ?
                       WHERE name = ? AND expiration = ?''',
                    (quantity, name, exp_date))

        conn.commit()
        messagebox.showinfo("Success", "Product updated successfully!")

    # Divide screen
    main_pane = tk.PanedWindow(panel, orient=tk.HORIZONTAL, bg=panel.cget('bg'))
    main_pane.pack(fill=tk.BOTH, expand=True)

    # Left side = Product List
    left_frame = tk.Frame(main_pane, bg=panel.cget('bg'))
    main_pane.add(left_frame, width=200)

    # "Click to Grab Produce" button
    grab_button = tk.Button(left_frame, text="Click to Grab Information", command=grab_data)
    grab_button.pack(pady=10, padx=10)

    # Screen to display the products
    users_listbox = tk.Listbox(left_frame)
    users_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    users_listbox.bind("<<ListboxSelect>>", on_select) 

    # Existing Product Information
    for prod in products:
        users_listbox.insert(tk.END, str(prod["Name"] + " " + prod["Exp"]))

    # Right side = Product Information
    right_frame = tk.Frame(main_pane, bg=panel.cget('bg'))
    main_pane.add(right_frame)
    
    sub_frame = tk.Frame(right_frame, bg=right_frame.cget('bg'))
    sub_frame.pack(pady=20)

    # Product Name Input
    prod_name_label = tk.Label(sub_frame, text="Product Name:", bg=sub_frame.cget('bg'))
    prod_name_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
    prod_name_input = tk.Entry(sub_frame)
    prod_name_input.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    prod_name_input.bind("<FocusOut>", lambda event, entry=prod_name_input: check_special_chars(entry))

    # Quantity Input
    qty_label = tk.Label(sub_frame, text="Quantity:", bg=sub_frame.cget('bg'))
    qty_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
    qty_input = tk.Entry(sub_frame)
    qty_input.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

    # Food Group (Radio buttons)
    group_label = tk.Label(sub_frame, text="Food Group:", bg=sub_frame.cget('bg'))
    group_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

    var1 = tk.IntVar(master=root)
    food_groups = ["Dairy", "Fruits", "Vegetables", "Grains", "Protein", "Other"]
    for i, group in enumerate(food_groups, start=1):
        radio = tk.Radiobutton(sub_frame, text=group, variable=var1, value=i, bg=sub_frame.cget('bg'))
        radio.grid(row=3 + (i-1)//2, column=1 + (i-1)%2, padx=5, pady=5, sticky=tk.W)

    # Nutritional Information (Check buttons)
    info_label = tk.Label(sub_frame, text="Nutritional Information:", bg=sub_frame.cget('bg'))
    info_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)

    veg_var, vegan_var, gluten_var, lactose_var, eggs_var, nuts_var, halal_var, kosher_var = (tk.IntVar(master=root), tk.IntVar(master=root), tk.IntVar(master=root), tk.IntVar(master=root), tk.IntVar(master=root), tk.IntVar(master=root), tk.IntVar(master=root), tk.IntVar(master=root))
    check_vars = {
        "Vegetarian": veg_var,
        "Vegan": vegan_var,
        "Gluten": gluten_var,
        "Lactose": lactose_var,
        "Eggs": eggs_var,
        "Nuts": nuts_var,
        "Halal": halal_var,
        "Kosher": kosher_var
    }

    for i, (text, var) in enumerate(check_vars.items(), start=1):
        check = tk.Checkbutton(sub_frame, text=text, variable=var, onvalue=1, offvalue=0, bg=sub_frame.cget('bg'))
        check.grid(row=6 + (i-1)//2, column=1 + (i-1)%2, padx=5, pady=5, sticky=tk.W)

    # Expiration Date
    exp_date_label = tk.Label(sub_frame, text="Exp Date (MM/DD/YY):", bg=sub_frame.cget('bg'))
    exp_date_label.grid(row=10, column=0, padx=5, pady=5, sticky=tk.E)
    date_entry = tk.Entry(sub_frame)
    date_entry.grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)
    date_entry.bind("<FocusOut>", lambda e: format_date(date_entry)) 

    # Date Added
    add_date_label = tk.Label(sub_frame, text="Add Date (MM/DD/YY):", bg=sub_frame.cget('bg'))
    add_date_label.grid(row=11, column=0, padx=5, pady=5, sticky=tk.E)
    add_entry = tk.Entry(sub_frame)
    add_entry.grid(row=11, column=1, padx=5, pady=5, sticky=tk.W)
    add_entry.bind("<FocusOut>", lambda e: format_date(add_entry)) 

    # User Name Input
    user_name_label = tk.Label(sub_frame, text="User Name:", bg=sub_frame.cget('bg'))
    user_name_label.grid(row=12, column=0, padx=5, pady=5, sticky=tk.E)
    user_name_input = tk.Entry(sub_frame)
    user_name_input.grid(row=12, column=1, padx=5, pady=5, sticky=tk.W)
    user_name_input.bind("<FocusOut>", lambda event, entry=user_name_input: check_special_chars(entry))

    # Update button
    update_btn = tk.Button(sub_frame, text="Update", command=store)
    update_btn.grid(row=13, column=1, padx=5, pady=5)

    return

# Delete Existing Product
def delete_prod(panel):
    """
    Creates a GUI interface in the provided panel to search for and delete products from the SQLite database.

    Args:
        panel (Tkinter Frame): The frame where the form and product list will be displayed.

    Returns:
        None
    """
    conn = connect_db()

    # Function to refresh the listbox with current products
    def refresh_listbox():
        users_listbox.delete(0, tk.END)  # Clear the current listbox
        cur = conn.cursor()
        cur.execute("SELECT name, expiration FROM products WHERE user_id = ?", (logged_in_user_id,))
        products = cur.fetchall()

        for product in products:
            # Display product name and expiration date in the listbox
            display_text = f"{product[0]} {product[1]}"
            users_listbox.insert(tk.END, display_text)

    # Function to find a product by name
    def find_by_name():
        search_query = search_entry.get().lower()
        users_listbox.delete(0, tk.END)
        cur = conn.cursor()
        cur.execute("SELECT name, expiration FROM products WHERE name LIKE ? AND user_id = ?", ('%' + search_query + '%', logged_in_user_id))
        results = cur.fetchall()

        for result in results:
            # Display product name and expiration date in the listbox
            display_text = f"{result[0]} - Exp: {result[1]}"
            users_listbox.insert(tk.END, display_text)

    # Function to remove the selected product
    def remove_selected():
        selected_text = users_listbox.get(tk.ACTIVE)
        if not selected_text:
            messagebox.showwarning("Selection Error", "No product selected!")
            return

        # Extract the product name and expiration date from the selected text
        selected_product, selected_expiration = selected_text.split(" ")
        
        # Confirm deletion
        response = messagebox.askyesno("Delete Confirmation", f"Are you sure you want to delete '{selected_product}' with expiration date '{selected_expiration}'?")
        if response:
            cur = conn.cursor()
            cur.execute("DELETE FROM products WHERE name = ? AND expiration = ? AND user_id = ?", (selected_product, selected_expiration, logged_in_user_id))
            conn.commit()

            messagebox.showinfo("Success", f"Product '{selected_product}' with expiration date '{selected_expiration}' deleted successfully!")
            refresh_listbox()

    # Layout for delete
    sub_frame = tk.Frame(panel, bg=panel.cget('bg'))
    sub_frame.pack(pady=20)

    instructions = tk.Label(sub_frame, text="Search for the product to delete:", bg=sub_frame.cget('bg'))
    instructions.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    search_entry = tk.Entry(sub_frame)
    search_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

    search_btn = tk.Button(sub_frame, text="Search", command=find_by_name)
    search_btn.grid(row=1, column=1, padx=5, pady=5)

    # Listbox to display the search results
    users_listbox = tk.Listbox(sub_frame, height=10, width=50)
    users_listbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

    # Populate the Listbox with all products initially
    refresh_listbox()

    # Delete button
    delete_btn = tk.Button(sub_frame, text="Delete", command=remove_selected)
    delete_btn.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    return

# Search for Product
def search_prod(panel):
    """
    Creates a GUI interface in the provided panel to search for and display product information.

    This function allows users to search for products by name and displays the results in a 
    formatted text area. Users can input part or the full name of a product, and the matching 
    products are displayed with details such as product name, quantity, food group, and any relevant 
    nutritional information (e.g., vegetarian, vegan, etc.).

    Key Features:
    - Search by product name.
    - Display of product details including quantity, food group, and nutritional information.
    - Results are shown in a text widget in the panel.

    Args:
        panel (Tkinter Frame): The frame where the search form and results will be displayed.

    Returns:
        None
    """
    conn = connect_db()

    # Function to display search results
    def display_results(filtered_products):
        result_text.delete('1.0', tk.END)
        if filtered_products:
            for prod in filtered_products:
                group_name = food_groups[prod[2] - 1]  # Assuming group is an index starting from 1
                nutritional_info_str = ", ".join([key for key, value in {
                    "Vegetarian": prod[6],
                    "Vegan": prod[7],
                    "Gluten": prod[8],
                    "Lactose": prod[9],
                    "Eggs": prod[10],
                    "Nuts": prod[11],
                    "Halal": prod[12],
                    "Kosher": prod[13]
                }.items() if value == 1]) or "None"
                result_text.insert(tk.END, f"{prod[0]} - {prod[1]} QTY - {group_name} - {nutritional_info_str}\n Expiration: {prod[3]} - Added: {prod[4]}\n")
        else:
            result_text.insert(tk.END, "No products found.\n")

    # Function to search by name
    def search_by_name():
        search_query = name_entry.get().lower()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE name LIKE ? AND user_id = ?", ('%' + search_query + '%', logged_in_user_id))
        filtered_products = cur.fetchall()
        display_results(filtered_products)

    # Layout for search options
    top_frame = tk.Frame(panel, bg=panel.cget('bg'))
    top_frame.pack(pady=10)

    # Search by name
    name_label = tk.Label(top_frame, text="Search by Name:", bg=top_frame.cget('bg'))
    name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    name_entry = tk.Entry(top_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

    search_name_btn = tk.Button(top_frame, text="Search", command=search_by_name)
    search_name_btn.grid(row=0, column=2, padx=5, pady=5)

    # Bottom half = search results
    bottom_frame = tk.Frame(panel, bg=panel.cget('bg'))
    bottom_frame.pack(pady=10)

    result_label = tk.Label(bottom_frame, text="Search Results:", bg=bottom_frame.cget('bg'))
    result_label.pack(pady=5)

    result_text = tk.Text(bottom_frame, height=15, width=80)
    result_text.pack(pady=5)

    return

# Open the HTML file in a web browser
def open_html(file_path):
    """
    Opens an HTML file in the default web browser.

    This function takes a file path to an HTML file, converts it to an absolute path, 
    and opens it in the user's default web browser.

    Args:
        file_path (str): The relative or absolute path to the HTML file to be opened.

    Returns:
        None
    """
    webbrowser.open(f'file://{os.path.realpath(file_path)}')

# Check Agreements
def check_agreements():
    """
    Displays a user agreement dialog and checks if the user has accepted the terms.

    This function first checks if a verification file exists (`VERIFICATION`). If the file exists 
    and contains a valid response (e.g., "yes" or "true"), the function returns `True`, indicating 
    that the user has already agreed to the terms.

    If no valid verification exists, the function creates a Tkinter window displaying clickable 
    links for the End User License Agreement (EULA), Privacy Policy, and Terms and Conditions. 
    The user must either agree by clicking "Yes, I agree" or decline by clicking "No, I don't agree". 
    If the user agrees, the response is written to the `VERIFICATION` file, and the function returns `True`. 
    If the user declines, the application exits.

    Args:
        None

    Returns:
        bool: `True` if the user agrees to the terms, `False` otherwise.
    """
    # Checks verification if it exists
    if os.path.exists(VERIFICATION):
        with open(VERIFICATION, "r") as file:
            content = file.read().strip().lower()
            if content in ["yes", "true"]:
                return True

    # Screen for agreement
    agreement_root = tk.Tk()
    agreement_root.title("User Agreement")
    agreement_root.protocol("WM_DELETE_WINDOW", sys.exit)

    # Create a label with a clickable link for EULA
    eula_label = Label(agreement_root, text="EULA (click to view)", fg="blue")
    eula_label.pack(pady=10)
    eula_label.bind("<Button-1>", lambda e: open_html(EULA_AGREEMENT))

    # Create a label with a clickable link for Privacy Policy
    privacy_label = Label(agreement_root, text="Privacy Policy (click to view)", fg="blue")
    privacy_label.pack(pady=10)
    privacy_label.bind("<Button-1>", lambda e: open_html(PRIVACY_POLICY))

    # Create a label with a clickable link for Terms and Conditions
    terms_label = Label(agreement_root, text="Terms and Conditions (click to view)", fg="blue")
    terms_label.pack(pady=10)
    terms_label.bind("<Button-1>", lambda e: open_html(TERMS_CONDITIONS))

    # Agreement buttons
    def on_yes():
        with open(VERIFICATION, "w") as file:
            file.write("yes")
        agreement_root.destroy()

    def on_no():
        with open(VERIFICATION, "w") as file:
            file.write("no")
        sys.exit()

    # Buttons to Agree
    btn_yes = tk.Button(agreement_root, text="Yes, I agree", command=on_yes)
    btn_no = tk.Button(agreement_root, text="No, I don't agree", command=on_no)
    btn_yes.pack(side=tk.LEFT, padx=5, pady=10)
    btn_no.pack(side=tk.RIGHT, padx=5, pady=10)

    # Creates Verification
    agreement_root.mainloop()
    return os.path.exists(VERIFICATION) and open(VERIFICATION).read().strip() == "yes"

# Main Function
def main():
    """
    The main entry point of the application.

    This function first checks if the user has agreed to the terms using `check_agreements()`. 
    If the user has not agreed, the application will terminate. If the user agrees, the function 
    initializes the main Tkinter window using `main_window()`, and sets up the application's 
    interface.

    The interface consists of:
    - A frame that holds buttons for navigating different sections of the application.
    - A panel that updates its content based on the selected button.

    The function also sets up the window close behavior and starts the Tkinter main event loop 
    to keep the application running.

    Args:
        None

    Returns:
        None
    """
    global root

    # Checks if Agreement is true
    if not check_agreements():
        return
    root = main_window()
    root.protocol("WM_DELETE_WINDOW", sys.exit)

    conn = connect_db()   # Connect to the database
    create_users(conn)    # Ensure the table exists
    create_products(conn) # Ensure the table exists

    # Start the Tkinter main loop
    root.mainloop()

# Starting Point
if __name__ == "__main__":
    login_window()
    main()
