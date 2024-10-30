from tkinter import *
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

# Colors
LIGHT_BG = "MintCream"  # Light mode color for root, frames, etc.
DARK_BG = "gray20"      # Dark mode color for root, frames, etc.
FRAME_LIGHT_COLOR = "white"  # Light mode color for frames
FRAME_DARK_COLOR = "black"     # Dark mode color for frames

# Checks if the script is running in a "frozen" state
if getattr(sys, 'frozen', False):
    CURRENT_DIR = os.path.dirname(sys.executable)
else:
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Button Text
BUTTON_TEXTS = ["ADD", "UPDATE", "DELETE", "SEARCH"]
BUTTON_COLORS = ["lightgreen", "lightblue", "salmon", "lightyellow"]

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
    root = tk.Tk()
    root.title("FoodConnect")
    root.geometry('600x800')
    root.config(bg=LIGHT_BG)  

    # Adding light and dark mode images
    light = PhotoImage(file="light.png")
    dark = PhotoImage(file="dark.png")

    switch_value = True

    def toggle(panel, frame):
        nonlocal switch_value

        # Dark theme
        if switch_value:
            switch.config(image=dark, bg=DARK_BG, activebackground=DARK_BG)
            root.config(bg=DARK_BG)
            panel.config(bg=FRAME_DARK_COLOR)
            frame.config(bg=FRAME_DARK_COLOR)

            # Change all children in frame and panel to dark mode color
            for widget in frame.winfo_children():
                widget.config(bg=FRAME_DARK_COLOR)

            for widget in panel.winfo_children():
                widget.config(bg=FRAME_DARK_COLOR)

            switch_value = False
            
        # Light theme
        else:
            switch.config(image=light, bg=LIGHT_BG, activebackground=LIGHT_BG)
            root.config(bg=LIGHT_BG)
            panel.config(bg=FRAME_LIGHT_COLOR)
            frame.config(bg=FRAME_LIGHT_COLOR)

            # Change all children in frame and panel to light mode color
            for widget in frame.winfo_children():
                widget.config(bg=FRAME_LIGHT_COLOR)

            for widget in panel.winfo_children():
                widget.config(bg=FRAME_LIGHT_COLOR)

            switch_value = True
            
    # Toggle Button
    switch = Button(root, image=light, bd=0, bg=LIGHT_BG, activebackground=LIGHT_BG,
                    command=lambda: toggle(panel, frame))
    switch.place(relx=0.9, rely=0.9, anchor='se')  # Position at bottom-right corner

    # Create frames for buttons and content
    frame = tk.Frame(root, bg=FRAME_LIGHT_COLOR)
    frame.pack(side=tk.TOP, pady=20)
    
    panel = tk.Frame(root, bg=FRAME_LIGHT_COLOR)
    panel.pack(side=tk.TOP, pady=20)

    # Create buttons and pass the panel for content display
    create_buttons(frame, panel, switch_value)  # Pass switch_value

    return root

# Load Products
def load_prod():
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
    # Iterating over all buttons, find the one that is clicked, adjust size
    for index, button in enumerate(buttons):
        if index == clicked_index:
            button.config(height=HEIGHT, width=WIDTH)
        else:
            button.config(height=HEIGHT, width=WIDTH)

    create_panel(clicked_index, panel)  # Call create_panel with the clicked index

# Create the Buttons
def create_buttons(frame, panel, switch_value):  # Accept switch_value as a parameter
    buttons = []
    for i, text in enumerate(BUTTON_TEXTS):
        button_color = "lightgreen" if switch_value else "darkgreen"  # Adjust as needed
        btn = tk.Button(frame, bg=button_color, text=text, height=HEIGHT, width=WIDTH,
                        command=lambda i=i: on_button_click(i, buttons, panel))
        btn.grid(row=1, column=i, sticky="s")
        buttons.append(btn)
    
    buttons[0].config(height=HEIGHT, width=WIDTH)  # Default Button
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
        delete_prod(panel)
    else:               # Search for product
        search_prod(panel)

# Check for Special Characters
def check_special_chars(entry):
    content = entry.get()
    # Check if there are any special characters in the content using regex
    if re.search(r'[^a-zA-Z0-9 ]', content):  # Matches anything not alphanumeric or space
        entry.config(bg="lightcoral")
    else:
        entry.config(bg="white")

# Formating for date MM/DD/YY
def format_date(entry_widget, event=None):
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
    return qty.isdigit() and int(qty) > 0
        
def add_prod(panel):
    sub_frame = tk.Frame(panel, bg=panel.cget('bg'))
    sub_frame.pack(pady=20)

    instructions = tk.Label(sub_frame, text="Fill in the information for the NEW product.") #HERE: , bg=sub_frame.cget('bg') <-issue???
    instructions.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

    # Product Name Input
    prod_name_label = tk.Label(sub_frame, text="Product Name:")
    prod_name_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
    prod_name_input = tk.Entry(sub_frame, bg="white")  
    prod_name_input.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    prod_name_input.bind("<FocusOut>", lambda event, entry=prod_name_input: check_special_chars(entry))

    # Quantity Input
    qty_label = tk.Label(sub_frame, text="Quantity:")
    qty_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
    qty_input = tk.Entry(sub_frame, bg="white")  
    qty_input.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

    # Food Group (Radio buttons)
    group_label = tk.Label(sub_frame, text="Food Group:")
    group_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

    var1 = tk.IntVar()
    food_groups = ["Dairy", "Fruits", "Vegetables", "Grains", "Protein", "Other"]
    for i, group in enumerate(food_groups, start=1):
        radio = tk.Radiobutton(sub_frame, text=group, variable=var1, value=i)
        radio.grid(row=3 + (i - 1) // 2, column=1 + (i - 1) % 2, padx=5, pady=5, sticky=tk.W)

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
        check.grid(row=6 + (i - 1) // 2, column=1 + (i - 1) % 2, padx=5, pady=5, sticky=tk.W)

    # Expiration Date
    exp_date_label = tk.Label(sub_frame, text="Exp Date (MM/DD/YY):")
    exp_date_label.grid(row=10, column=0, padx=5, pady=5, sticky=tk.E)
    exp_date_entry = tk.Entry(sub_frame, bg="white")  
    exp_date_entry.grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)
    exp_date_entry.bind("<FocusOut>", lambda event: format_date(exp_date_entry))

    # Date Added
    add_date_label = tk.Label(sub_frame, text="Date Added (MM/DD/YY):")
    add_date_label.grid(row=11, column=0, padx=5, pady=5, sticky=tk.E)
    add_date_entry = tk.Entry(sub_frame, bg="white")  
    add_date_entry.grid(row=11, column=1, padx=5, pady=5, sticky=tk.W)
    add_date_entry.bind("<FocusOut>", lambda event: format_date(add_date_entry))

    # User Name Input
    user_name_label = tk.Label(sub_frame, text="User Name:")
    user_name_label.grid(row=12, column=0, padx=5, pady=5, sticky=tk.E)
    user_name_input = tk.Entry(sub_frame, bg="white") 
    user_name_input.grid(row=12, column=1, padx=5, pady=5, sticky=tk.W)
    user_name_input.bind("<FocusOut>", lambda event, entry=user_name_input: check_special_chars(entry))

    # Collect and Store Data
    def store():
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

        # Message appears if information is added
        messagebox.showinfo("Success", "Product added successfully!")
        sub_frame.destroy()  # Clear the form after submission

    # Submit Button
    submit_btn = tk.Button(sub_frame, text="Submit", command=store, bg="gray50")  # Button color can be adjusted
    submit_btn.grid(row=13, column=1, padx=5, pady=5)

    return

# Update Existing Product 
def update_prod(panel):
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
    main_pane = tk.PanedWindow(panel, orient=tk.HORIZONTAL, bg=panel.cget('bg'))
    main_pane.pack(fill=tk.BOTH, expand=True)

    # Left side = Product List
    left_frame = tk.Frame(main_pane, bg=panel.cget('bg'))  # Use panel's bg color
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
    right_frame = tk.Frame(main_pane, bg=panel.cget('bg'))  # Use panel's bg color
    main_pane.add(right_frame)
    
    sub_frame = tk.Frame(right_frame, bg=right_frame.cget('bg'))  # Use right_frame's bg color
    sub_frame.pack(pady=20)

    # Update product widgets with background color
    prod_name_label = tk.Label(sub_frame, text="Product Name:")  
    prod_name_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

    prod_name_input = tk.Entry(sub_frame, bg="white")  
    prod_name_input.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    prod_name_input.bind("<FocusOut>", lambda event, entry=prod_name_input: check_special_chars(entry))

    qty_label = tk.Label(sub_frame, text="Quantity:")  
    qty_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
    qty_input = tk.Entry(sub_frame, bg="white")  
    qty_input.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

    group_label = tk.Label(sub_frame, text="Food Group:") 
    group_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

    var1 = tk.IntVar()
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

    # Date Added
    add_date_label = tk.Label(sub_frame, text="Date Added (MM/DD/YY):") 
    add_date_label.grid(row=11, column=0, padx=5, pady=5, sticky=tk.E)
    add_entry = tk.Entry(sub_frame)
    add_entry.grid(row=11, column=1, padx=5, pady=5, sticky=tk.W)

    # User Name
    user_name_label = tk.Label(sub_frame, text="User Name:")  
    user_name_label.grid(row=12, column=0, padx=5, pady=5, sticky=tk.E)
    user_name_input = tk.Entry(sub_frame) 
    user_name_input.grid(row=12, column=1, padx=5, pady=5, sticky=tk.W)

    # Update Button
    update_button = tk.Button(right_frame, text="Update Product", command=store)
    update_button.pack(pady=10)

    return

# Delete Existing Product
def delete_prod(panel):
    global my_prod

    my_prod = load_prod()  

    # Function to find a product by name
    def find_by_name():
        search_query = search_entry.get().lower()
        users_listbox.delete(0, tk.END) 
        for prod in my_prod:
            if search_query in prod["Name"].lower():
                # Show both Name and UniqueID in the Listbox
                users_listbox.insert(tk.END, f"{prod['Name']} (ID: {prod['UniqueID']})")

    # Function to remove the selected product
    def remove_selected():
        selected_product = users_listbox.get(tk.ACTIVE)
        if not selected_product:
            messagebox.showwarning("Selection Error", "No product selected!")
            return

        # Extract Name and UniqueID from the selection
        selected_name = selected_product.split(" (ID: ")[0]
        selected_id = selected_product.split(" (ID: ")[1][:-1]

        # Confirm deletion
        response = messagebox.askyesno("Delete Confirmation", f"Are you sure you want to delete '{selected_name}' with ID {selected_id}?")
        if response:
            global my_prod  # Ensure you're using the global variable
            # Filter out the product only if both Name and UniqueID match
            my_prod = [prod for prod in my_prod if not (prod["Name"] == selected_name and str(prod["UniqueID"]) == selected_id)]

            # Update the JSON file
            with open(PROD_JSON, 'w') as f:
                json.dump({"products": my_prod}, f, indent=4)

            # Refresh the listbox and show success message
            find_by_name()  # Refresh the search results
            messagebox.showinfo("Success", f"Product '{selected_name}' with ID {selected_id} deleted successfully!")

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
        users_listbox.insert(tk.END, f"{prod['Name']} (ID: {prod['UniqueID']})")

    # Delete button
    delete_btn = tk.Button(sub_frame, text="Delete", command=remove_selected)
    delete_btn.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    return

# Search for Product
def search_prod(panel):
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
    return    

# Open the HTML file in a web browser
def open_html(file_path):
    webbrowser.open(f'file://{os.path.realpath(file_path)}')

# Check Agreements
def check_agreements():
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

def main():
    # Checks if Agreement is true
    if not check_agreements():
        return
    root = main_window()  # Call main_window which already sets up `frame` and `panel`
    root.protocol("WM_DELETE_WINDOW", sys.exit)

    # Start the Tkinter main loop
    root.mainloop()

# Starting Point
if __name__ == "__main__":
    main()

