import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import Text
import os
import json
import string
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

# JSON Path
PROD_JSON = os.path.join(CURRENT_DIR, "products.json") # Create JSON file

# User Agreements
EULA_TEXT = os.path.join(CURRENT_DIR, "EULA.txt")
EULA_VERIFICATION = os.path.join(CURRENT_DIR, "Agreement.txt")

# Main Window
def main_window():
    root = tk.Tk()
    root.title("Group 6 - Project 1")
    root.geometry('600x800')
    return root

# Load Products
def load_prod():
    with open(PROD_JSON, 'r') as f:
        data = json.load(f)
    return data["products"] # Print Data from JSON file

# Create the Buttons
def create_buttons(frame, panel):
    buttons = []
    for i, text in enumerate(BUTTON_TEXTS):
        btn = tk.Button(frame, text=text, height=HEIGHT, width=WIDTH,
                        command=lambda i=i: on_button_click(i, buttons, panel))
        btn.grid(row=1, column=i,sticky="s")
        buttons.append(btn)
    buttons[0].config(height=HEIGHT, width=WIDTH)  # default button
    return buttons

# Button Panel
def create_panel(index, panel):
    for widget in panel.winfo_children():
        widget.destroy()
    if index == 0:      # Add new product
        add_prod(panel)
    elif index == 1:    # Update existing product
        update_prod(panel)
    elif index == 2:    # Delete existing product
        add_display_panel(panel)
    else:               # Search for product
        add_search_panel(panel)

# Add new product
def add_prod(panel):
    """
    Set up:
    Name [ Input ] ✓
    QTY [ Input ] ✓
    Type [ Radio Button ] ✓
    Nutrition [ Check Button ] ✓
    Exp Date [ MM/DD/YY ] ✓
    Date Added [ MM/DD/YY ] ✓
    """

    def format_date(event=None):
        content = date_entry.get()
        # Remove any hyphens that the user might have entered
        clean_content = content.replace("-", "")

        if len(clean_content) == 6 and clean_content.isdigit():
            # Format the date as MM/DD/YY
            formatted_date = clean_content[:2] + "/" + clean_content[2:4] + "/" + clean_content[4:]
            date_entry.delete(0, tk.END)
            date_entry.insert(0, formatted_date)
            date_entry.config(bg="white")  # Reset to normal background color
        elif content:
            date_entry.config(bg="lightcoral")  # Invalid input

    # Create a sub-frame to contain the labels and input
    sub_frame = tk.Frame(panel, bg=panel.cget('bg'))
    sub_frame.pack(pady=20)

    instructions = tk.Label(sub_frame, text="Fill in the information for the NEW product.")
    instructions.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

    # PRODUCT NAME INPUT
    prod_name_label = tk.Label(sub_frame, text="Product Name:")
    prod_name_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
    prod_name_input = tk.Entry(sub_frame)
    prod_name_input.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

    # QUANTITY INPUT
    qty_label = tk.Label(sub_frame, text="Quantity:")
    qty_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
    qty_input = tk.Entry(sub_frame)
    qty_input.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

    # FOOD GROUP
    group_label = tk.Label(sub_frame, text="Food Group:")
    group_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

    # Variable for radio buttons
    var1 = tk.IntVar()

    # Radio buttons
    group_R1 = tk.Radiobutton(sub_frame, text="Dairy", variable=var1, value=1)
    group_R1.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

    group_R2 = tk.Radiobutton(sub_frame, text="Fruits", variable=var1, value=2)
    group_R2.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

    group_R3 = tk.Radiobutton(sub_frame, text="Vegetables", variable=var1, value=3)
    group_R3.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

    group_R4 = tk.Radiobutton(sub_frame, text="Grains", variable=var1, value=4)
    group_R4.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)

    group_R5 = tk.Radiobutton(sub_frame, text="Protein", variable=var1, value=5)
    group_R5.grid(row=4, column=2, padx=5, pady=5, sticky=tk.W)

    # NUTRITIONAL INFORMATION
    info_label = tk.Label(sub_frame, text="Nutritional Information:")
    info_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)

    # Variable for check buttons
    veg_var = tk.IntVar()
    vegan_var = tk.IntVar()
    gluten_var = tk.IntVar()
    lactose_var = tk.IntVar()
    eggs_var = tk.IntVar()
    nuts_var = tk.IntVar()
    halal_var = tk.IntVar()
    kosher_var = tk.IntVar()

    # Check buttons
    check_R1 = tk.Checkbutton(sub_frame, text="Vegetarian", variable=veg_var, value=1)
    check_R1.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

    check_R2 = tk.Checkbutton(sub_frame, text="Vegan", variable=vegan_var, value=2)
    check_R2.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)

    check_R3 = tk.Checkbutton(sub_frame, text="Gluten", variable=gluten_var, value=3)
    check_R3.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)

    check_R4 = tk.Checkbutton(sub_frame, text="Lactose", variable=lactose_var, value=4)
    check_R4.grid(row=9, column=1, padx=5, pady=5, sticky=tk.W)

    check_R5 = tk.Checkbutton(sub_frame, text="Eggs", variable=eggs_var, value=5)
    check_R5.grid(row=6, column=2, padx=5, pady=5, sticky=tk.W)

    check_R6 = tk.Checkbutton(sub_frame, text="Nuts", variable=nuts_var, value=6)
    check_R6.grid(row=7, column=2, padx=5, pady=5, sticky=tk.W)

    check_R7 = tk.Checkbutton(sub_frame, text="Halal", variable=halal_var, value=7)
    check_R7.grid(row=8, column=2, padx=5, pady=5, sticky=tk.W)

    check_R8 = tk.Checkbutton(sub_frame, text="Kosher", variable=kosher_var, value=8)
    check_R8.grid(row=9, column=2, padx=5, pady=5, sticky=tk.W)

    # EXPIRATION DATE
    exp_date_label = tk.Label(sub_frame, text="Exp Date (MM/DD/YY):")
    exp_date_label.grid(row=10, column=0, padx=5, pady=5, sticky=tk.E)
    date_entry = tk.Entry(sub_frame)
    date_entry.grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)
    date_entry.bind("<FocusOut>", format_date)

    # DATE ADDED
    add_date_label = tk.Label(sub_frame, text="Date Added (MM/DD/YY):")
    add_date_label.grid(row=11, column=0, padx=5, pady=5, sticky=tk.E)
    add_entry = tk.Entry(sub_frame)
    add_entry.grid(row=11, column=1, padx=5, pady=5, sticky=tk.W)
    add_entry.bind("<FocusOut>", format_date)

    # Collect and Store Data
    def store():
        new_prod = {
            "Name": prod_name_input.get(),
            "Quantity": qty_input.get(),
            "Group": var1.get(),  # The selected radio button value
            "Info": {
                "Vegetarian": veg_var.get(),
                "Vegan": vegan_var.get(),
                "Gluten": gluten_var.get(),
                "Lactose": lactose_var.get(),
                "Eggs": eggs_var.get(),
                "Nuts": nuts_var.get(),
                "Halal": halal_var.get(),
                "Kosher": kosher_var.get()
            },
            "Exp": date_entry.get(),
            "Add": add_entry.get()
        }

        with open(PROD_JSON, 'r+') as f:
            data = json.load(f)
            data["products"].append(new_prod)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    submit_btn = tk.Button(sub_frame, text="Submit", command=store)
    submit_btn.grid(row=12, column=1, padx=5, pady=5)

    messagebox.showinfo("Success", "Product added successfully!")

    return
    
# Update Existing Product
def update_prod(panel):
    """
    Set up: [Left - Product Info] [Right - Same as ADD info]
    """
    my_prod = load_prod()

    def get_prod_data(name, products):
        for product in products:
            if product["Name"] == name:
                return product


    def find_by_name():
        search_query = search_entry.get().lower()
        users_listbox.delete(0, tk.END)  # Clear current list
        for prod in my_prod:
            if search_query in prod["Name"].lower():  # Ensure the field names match your JSON
                users_listbox.insert(tk.END, str(prod["Name"]))


    def grab_data():
        product = get_prod_data(selected_product)  # assuming selected_product is passed in correctly

        # Populate the text fields with the product's data
        prod_name_input.delete(0, tk.END)
        prod_name_input.insert(0, product["Name"])

        qty_input.delete(0, tk.END)
        qty_input.insert(0, product["Quantity"])

        # Set the food group radio button
        var1.set(product["Group"])

        # Set the check buttons for nutritional information
        var2.set(product["Info"])

        # Set expiration date
        date_entry.delete(0, tk.END)
        date_entry.insert(0, product["Exp"])

        # Set the date added
        add_entry.delete(0, tk.END)
        add_entry.insert(0, product["Add"])

    def format_date(event=None):
        content = date_entry.get()
        # Remove any hyphens that the user might have entered
        clean_content = content.replace("-", "")

        if len(clean_content) == 6 and clean_content.isdigit():
            # Format the date as MM/DD/YY
            formatted_date = clean_content[:2] + "/" + clean_content[2:4] + "/" + clean_content[4:]
            date_entry.delete(0, tk.END)
            date_entry.insert(0, formatted_date)
            date_entry.config(bg="white")  # Reset to normal background color
        elif content:
            date_entry.config(bg="lightcoral")  # Invalid input

    



#### I LEFT OFF OVER HERE STILL WORKING ON IT ###

# Example usage:
# root = tk.Tk()
# add_prod(root)
# root.mainloop()

