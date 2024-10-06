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
import webbrowser
import os
import json
import re
import sys

# Constants
HEIGHT = 3
WIDTH = 20

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

# Main Window
def main_window():
    """
    Initializes and configures the main window for the Tkinter application.

    This function creates the root window with a title "FoodConnect" and 
    sets the dimensions of the window to 600x800 pixels.

    Returns:
        Tk: The root Tkinter window object that serves as the main application window.
    """
    root = tk.Tk()
    root.title("FoodConnect")
    root.geometry('600x800')
    return root

# Load Products
def load_prod():
    """
    Loads the list of products from a JSON file.

    This function checks if the specified product JSON file exists. If the file does not exist, 
    it creates the file with a default structure, including an empty "products" list. It then 
    reads the contents of the file and returns the list of products.

    Returns:
        list: A list of products loaded from the JSON file.
    """
    # Check if the file exists
    if not os.path.exists(PROD_JSON):
        # Create the file with a default structure if it doesn't exist
        with open(PROD_JSON, 'w') as f:
            json.dump({"products": []}, f)  # Create an empty product list
    with open(PROD_JSON, 'r') as f:
        data = json.load(f)
    return data["products"]  # Return the list of products

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
def create_buttons(frame, panel):
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
        btn = tk.Button(frame, text=text, height=HEIGHT, width=WIDTH,
                        command=lambda i=i: on_button_click(i, buttons, panel))
        btn.grid(row=1, column=i, sticky="s")
        buttons.append(btn)
    buttons[0].config(height=HEIGHT, width=WIDTH)  # Default Button
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
    # Set up for the Add Panel
    sub_frame = tk.Frame(panel, bg=panel.cget('bg'))
    sub_frame.pack(pady=20)

    instructions = tk.Label(sub_frame, text="Fill in the information for the NEW product.")
    instructions.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

    # Product Name Input
    prod_name_label = tk.Label(sub_frame, text="Product Name:")
    prod_name_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
    prod_name_input = tk.Entry(sub_frame)
    prod_name_input.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    prod_name_input.bind("<FocusOut>", lambda event, entry=prod_name_input: check_special_chars(entry))

    # Quantity Input
    qty_label = tk.Label(sub_frame, text="Quantity:")
    qty_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
    qty_input = tk.Entry(sub_frame)
    qty_input.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

    # Food Group (Radio buttons)
    group_label = tk.Label(sub_frame, text="Food Group:")
    group_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

    var1 = tk.IntVar()
    food_groups = ["Dairy", "Fruits", "Vegetables", "Grains", "Protein", "Other"]
    for i, group in enumerate(food_groups, start=1):
        radio = tk.Radiobutton(sub_frame, text=group, variable=var1, value=i)
        radio.grid(row=3 + (i-1)//2, column=1 + (i-1)%2, padx=5, pady=5, sticky=tk.W)

    # Nutritional Information (Check buttons)
    info_label = tk.Label(sub_frame, text="Nutritional Information:")
    info_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)

    nutrition_vars = {
        "Vegetarian": tk.IntVar(),
        "Vegan": tk.IntVar(),
        "Gluten": tk.IntVar(),
        "Lactose": tk.IntVar(),
        "Eggs": tk.IntVar(),
        "Nuts": tk.IntVar(),
        "Halal": tk.IntVar(),
        "Kosher": tk.IntVar()
    }

    for i, (text, var) in enumerate(nutrition_vars.items(), start=1):
        check = tk.Checkbutton(sub_frame, text=text, variable=var, onvalue=1, offvalue=0)
        check.grid(row=6 + (i-1)//2, column=1 + (i-1)%2, padx=5, pady=5, sticky=tk.W)

    # Experation Date
    exp_date_label = tk.Label(sub_frame, text="Exp Date (MM/DD/YY):")
    exp_date_label.grid(row=10, column=0, padx=5, pady=5, sticky=tk.E)
    exp_date_entry = tk.Entry(sub_frame)
    exp_date_entry.grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)
    exp_date_entry.bind("<FocusOut>", lambda event: format_date(exp_date_entry))

    # Date Added
    add_date_label = tk.Label(sub_frame, text="Date Added (MM/DD/YY):")
    add_date_label.grid(row=11, column=0, padx=5, pady=5, sticky=tk.E)
    add_date_entry = tk.Entry(sub_frame)
    add_date_entry.grid(row=11, column=1, padx=5, pady=5, sticky=tk.W)
    add_date_entry.bind("<FocusOut>", lambda event: format_date(add_date_entry))

    # User Name Input
    user_name_label = tk.Label(sub_frame, text="User Name:")
    user_name_label.grid(row=12, column=0, padx=5, pady=5, sticky=tk.E)
    user_name_input = tk.Entry(sub_frame)
    user_name_input.grid(row=12, column=1, padx=5, pady=5, sticky=tk.W)
    user_name_input.bind("<FocusOut>", lambda event, entry=user_name_input: check_special_chars(entry))

    # Collect and Store Data
    def store():
        """
        Saves a new product entry to the JSON file.

        This function collects the input data from the form (e.g., product name, quantity, 
        expiration date, etc.), validates the quantity, and stores the product details in a 
        JSON file (`PROD_JSON`). If the file does not exist or is corrupted, it initializes a 
        new one. It also ensures the data structure is correct before appending new entries.

        Args:
            None

        Returns:
            None
        """
        # Validates the quantity input
        if not validate_qty(qty_input.get()):
            messagebox.showerror("Input Error", "Quantity must be a positive number.")
            return
        
        # Create the unique identifier by concatenating Name and Exp
        unique_id = prod_name_input.get() + exp_date_entry.get()

        # The information that will be stored
        new_prod = {
            "UniqueID": unique_id,
            "Name": prod_name_input.get(),
            "Quantity": qty_input.get(),
            "Group": var1.get(),  
            "Info": {key: var.get() for key, var in nutrition_vars.items()},
            "Exp": exp_date_entry.get(),
            "Add": add_date_entry.get(),
            "User": user_name_input.get()
        }

        # Load the existing data and append new product
        with open(PROD_JSON, 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"products": []}  # Initialize if file is empty or corrupted

            # Ensure that 'data' is a dictionary
            if not isinstance(data, dict):
                data = {"products": []}  # Reinitialize to correct structure if it's not a dictionary

            if "products" not in data:
                data["products"] = []  # Ensure "products" key exists

            data["products"].append(new_prod)

            # Write back the updated data
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

        # Message apears if information is added
        messagebox.showinfo("Success", "Product added successfully!")
        sub_frame.destroy()  # Clear the form after submission

    # Submit Button
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
    my_prod = load_prod()

    # Looks for the product
    def get_prod_data(name, products):
        for product in products:
            if product["Name"] == name:
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
        
        selected_name = users_listbox.get(selection[0])  # Get the selected name
        product = get_prod_data(selected_name, my_prod)
        
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
        # Get the current values from the input fields
        name = prod_name_input.get()
        quantity = qty_input.get()
        food_group = var1.get()
        exp_date = date_entry.get()
        add_date = add_entry.get()
        user = user_name_input.get()

        # Collect nutritional information
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

        # Load existing products
        with open(PROD_JSON, 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"products": []}  # Initialize if file is empty or corrupted

            # Find the product to update
            product_found = False
            for product in data["products"]:
                if product["Name"] == name:
                    # Update product data
                    product["Quantity"] = quantity
                    product["Group"] = food_group
                    # product["Exp"] = exp_date
                    product["Add"] = add_date
                    product["Info"] = nutritional_info
                    product["User"] = user
                    product_found = True
                    break

            if not product_found:
                # Message apears if information is not updated
                messagebox.showwarning("Fail", f"Product '{name}' not found.")
                return

            # Move the file cursor to the beginning and overwrite the file
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate() 

        # Message apears if information is updated
        messagebox.showinfo("Success", f"Product '{name}' updated successfully.")

    # Divide screen
    main_pane = tk.PanedWindow(panel, orient=tk.HORIZONTAL)
    main_pane.pack(fill=tk.BOTH, expand=True)

    # Left side = Product List
    left_frame = tk.Frame(main_pane)
    main_pane.add(left_frame, width=200)

    # "Click to Grab Produce" button
    grab_button = tk.Button(left_frame, text="Click to Grab Information", command=grab_data)
    grab_button.pack(pady=10, padx=10)

    # Screen to display the products
    users_listbox = tk.Listbox(left_frame)
    users_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    users_listbox.bind("<<ListboxSelect>>", on_select) 

    # Existing Product Information
    for prod in my_prod:
        users_listbox.insert(tk.END, str(prod["Name"]))

    # Right side = Product Information
    right_frame = tk.Frame(main_pane)
    main_pane.add(right_frame)
    
    sub_frame = tk.Frame(right_frame, bg=right_frame.cget('bg'))
    sub_frame.pack(pady=20)

    # Product Name Input
    prod_name_label = tk.Label(sub_frame, text="Product Name:")
    prod_name_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
    prod_name_input = tk.Entry(sub_frame)
    prod_name_input.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    prod_name_input.bind("<FocusOut>", lambda event, entry=prod_name_input: check_special_chars(entry))

    # Quantity Input
    qty_label = tk.Label(sub_frame, text="Quantity:")
    qty_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
    qty_input = tk.Entry(sub_frame)
    qty_input.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

    # Food Group (Radio buttons)
    group_label = tk.Label(sub_frame, text="Food Group:")
    group_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

    var1 = tk.IntVar()
    food_groups = ["Dairy", "Fruits", "Vegetables", "Grains", "Protein", "Other"]
    for i, group in enumerate(food_groups, start=1):
        radio = tk.Radiobutton(sub_frame, text=group, variable=var1, value=i)
        radio.grid(row=3 + (i-1)//2, column=1 + (i-1)%2, padx=5, pady=5, sticky=tk.W)

    # Nutritional Information (Check buttons)
    info_label = tk.Label(sub_frame, text="Nutritional Information:")
    info_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)

    veg_var, vegan_var, gluten_var, lactose_var, eggs_var, nuts_var, halal_var, kosher_var = (tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar())
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
        check = tk.Checkbutton(sub_frame, text=text, variable=var, onvalue=1, offvalue=0)
        check.grid(row=6 + (i-1)//2, column=1 + (i-1)%2, padx=5, pady=5, sticky=tk.W)

    # Expiration Date
    exp_date_label = tk.Label(sub_frame, text="Exp Date (MM/DD/YY):")
    exp_date_label.grid(row=10, column=0, padx=5, pady=5, sticky=tk.E)
    date_entry = tk.Entry(sub_frame)
    date_entry.grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)
    date_entry.bind("<FocusOut>", lambda e: format_date(date_entry)) 

    # Date Added
    add_date_label = tk.Label(sub_frame, text="Add Date (MM/DD/YY):")
    add_date_label.grid(row=11, column=0, padx=5, pady=5, sticky=tk.E)
    add_entry = tk.Entry(sub_frame)
    add_entry.grid(row=11, column=1, padx=5, pady=5, sticky=tk.W)
    add_entry.bind("<FocusOut>", lambda e: format_date(add_entry)) 

    # User Name Input
    user_name_label = tk.Label(sub_frame, text="User Name:")
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
    Creates a GUI interface in the provided panel to search for and delete products.

    This function provides a form that allows users to search for products by name and delete them 
    from the system. The product list is displayed in a listbox, and the user can search for a 
    specific product by entering the name in the search bar. When a product is selected, the user 
    can delete it after confirming the action. The product is removed from the JSON file that stores 
    product data.

    Key Features:
    - A search bar to filter products by name.
    - A listbox to display matching products.
    - A delete button to remove the selected product, with confirmation dialogs for safety.

    Args:
        panel (Tkinter Frame): The frame where the form and product list will be displayed.

    Returns:
        None
    """
    global my_prod 

    my_prod = load_prod()  

    # Function to find a product by name
    def find_by_name():
        search_query = search_entry.get().lower()
        users_listbox.delete(0, tk.END) 
        for prod in my_prod:
            if search_query in prod["Name"].lower():
                users_listbox.insert(tk.END, str(prod["Name"]))

    # Function to remove the selected product
    def remove_selected():
        selected_product = users_listbox.get(tk.ACTIVE)
        if not selected_product:
            messagebox.showwarning("Selection Error", "No product selected!")
            return

        # Confirm deletion
        response = messagebox.askyesno("Delete Confirmation", f"Are you sure you want to delete '{selected_product}'?")
        if response:
            global my_prod  # Ensure you're using the global variable
            my_prod = [prod for prod in my_prod if prod["Name"] != selected_product]

            # Update the JSON file
            with open(PROD_JSON, 'w') as f:
                json.dump({"products": my_prod}, f, indent=4)

            # Refresh the listbox and show success message
            find_by_name()  # Refresh the search results
            messagebox.showinfo("Success", f"Product '{selected_product}' deleted successfully!")

    # Layout for delete
    sub_frame = tk.Frame(panel, bg=panel.cget('bg'))
    sub_frame.pack(pady=20)

    instructions = tk.Label(sub_frame, text="Search for the product to delete:")
    instructions.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    search_entry = tk.Entry(sub_frame)
    search_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

    search_btn = tk.Button(sub_frame, text="Search", command=find_by_name)
    search_btn.grid(row=1, column=1, padx=5, pady=5)

    # Listbox to display the search results
    users_listbox = tk.Listbox(sub_frame, height=10, width=50)
    users_listbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

    # Populate the Listbox with all products initially
    for prod in my_prod:
        users_listbox.insert(tk.END, str(prod["Name"]))

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
    my_prod = load_prod() 

    # Function to display search results
    def display_results(filtered_products):
        result_text.delete('1.0', tk.END)
        if filtered_products:
            for prod in filtered_products:
                # Format the output
                group_name = food_groups[prod['Group'] - 1]  # Assuming group is an index starting from 1
                nutritional_info = []
                for key, value in prod['Info'].items():
                    if value == 1:
                        nutritional_info.append(key)
                
                nutritional_info_str = ", ".join(nutritional_info) if nutritional_info else "None"
                result_text.insert(tk.END, f"ID: {prod['UniqueID']}\n {prod['Name']} - {prod['Quantity']} QTY - {group_name} - {nutritional_info_str}\n Expiration date: {prod['Exp']} - Added Date: {prod['Add']} - {prod['User']}\n")
        else:
            result_text.insert(tk.END, "No products found.\n")

    # Function to search by name
    def search_by_name():
        search_query = name_entry.get().lower()
        filtered_products = [prod for prod in my_prod if search_query in prod['Name'].lower()]
        display_results(filtered_products)

    # Layout for search options
    top_frame = tk.Frame(panel, bg=panel.cget('bg'))
    top_frame.pack(pady=10)

    # Search by name
    name_label = tk.Label(top_frame, text="Search by Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    name_entry = tk.Entry(top_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

    search_name_btn = tk.Button(top_frame, text="Search", command=search_by_name)
    search_name_btn.grid(row=0, column=2, padx=5, pady=5)

    # Bottom half = search results
    bottom_frame = tk.Frame(panel, bg=panel.cget('bg'))
    bottom_frame.pack(pady=10)

    result_label = tk.Label(bottom_frame, text="Search Results:")
    result_label.pack(pady=5)

    result_text = tk.Text(bottom_frame, height=15, width=80)
    result_text.pack(pady=5)

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
    # Checks if Agreement is true
    if not check_agreements():
        return
    root = main_window()
    root.protocol("WM_DELETE_WINDOW", sys.exit)

    # Create a frame for buttons and panel for content
    frame = tk.Frame(root)
    frame.pack(side=tk.TOP, pady=20)

    panel = tk.Frame(root)
    panel.pack(side=tk.TOP, pady=20)

    # Create buttons and pass the panel for content display
    create_buttons(frame, panel)

    # Start the Tkinter main loop
    root.mainloop()

# Starting Point
if __name__ == "__main__":
    main()
