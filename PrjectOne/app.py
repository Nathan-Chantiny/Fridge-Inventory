import tkinter as tk
import tkinter.messagebox as messagebox
import os
import json
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
    # Check if the file exists
    if not os.path.exists(PROD_JSON):
        # Create the file with a default structure if it doesn't exist
        with open(PROD_JSON, 'w') as f:
            json.dump({"products": []}, f)  # Create an empty product list
    with open(PROD_JSON, 'r') as f:
        data = json.load(f)
    return data["products"]  # Return the list of products

def on_button_click(clicked_index, buttons, panel):
    # Iterating over all buttons, find the one that is clicked, adjust size
    for index, button in enumerate(buttons):
        if index == clicked_index:
            button.config(height=HEIGHT, width=WIDTH)
        else:
            button.config(height=HEIGHT, width=WIDTH)

    create_panel(clicked_index, panel)  # Call create_panel with the clicked index

# Create the Buttons
def create_buttons(frame, panel):
    buttons = []
    for i, text in enumerate(BUTTON_TEXTS):
        btn = tk.Button(frame, text=text, height=HEIGHT, width=WIDTH,
                        command=lambda i=i: on_button_click(i, buttons, panel))
        btn.grid(row=1, column=i, sticky="s")
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
        delete_prod(panel)
    else:               # Search for product
        search_prod(panel)

# Add New Product
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

    # Formating for date MM/DD/YY
    def format_date(entry_widget, event=None):
        content = entry_widget.get()
        clean_content = content.replace("-", "")

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

    # FOOD GROUP (Radio buttons)
    group_label = tk.Label(sub_frame, text="Food Group:")
    group_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

    var1 = tk.IntVar()
    food_groups = ["Dairy", "Fruits", "Vegetables", "Grains", "Protein", "Other"]
    for i, group in enumerate(food_groups, start=1):
        radio = tk.Radiobutton(sub_frame, text=group, variable=var1, value=i)
        radio.grid(row=3 + (i-1)//2, column=1 + (i-1)%2, padx=5, pady=5, sticky=tk.W)

    # NUTRITIONAL INFORMATION (Check buttons)
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

    # EXPIRATION DATE
    exp_date_label = tk.Label(sub_frame, text="Exp Date (MM/DD/YY):")
    exp_date_label.grid(row=10, column=0, padx=5, pady=5, sticky=tk.E)
    exp_date_entry = tk.Entry(sub_frame)
    exp_date_entry.grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)
    exp_date_entry.bind("<FocusOut>", lambda event: format_date(exp_date_entry))

    # DATE ADDED
    add_date_label = tk.Label(sub_frame, text="Date Added (MM/DD/YY):")
    add_date_label.grid(row=11, column=0, padx=5, pady=5, sticky=tk.E)
    add_date_entry = tk.Entry(sub_frame)
    add_date_entry.grid(row=11, column=1, padx=5, pady=5, sticky=tk.W)
    add_date_entry.bind("<FocusOut>", lambda event: format_date(add_date_entry))

    # Collect and Store Data
    def store():
        if not validate_qty(qty_input.get()):
            messagebox.showerror("Input Error", "Quantity must be a positive number.")
            return

        new_prod = {
            "Name": prod_name_input.get(),
            "Quantity": qty_input.get(),
            "Group": var1.get(),  # The selected radio button value
            "Info": {key: var.get() for key, var in nutrition_vars.items()},
            "Exp": exp_date_entry.get(),
            "Add": add_date_entry.get()
        }

        # Load the existing data and append new product
        with open(PROD_JSON, 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"products": []}  # Initialize if file is empty or corrupted

            # Ensure that 'data' is a dictionary
            if not isinstance(data, dict):
                data = {"products": []}  # Reinitialize to correct structure if it's not a dict

            if "products" not in data:
                data["products"] = []  # Ensure "products" key exists

            data["products"].append(new_prod)

            # Write back the updated data
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

        messagebox.showinfo("Success", "Product added successfully!")
        sub_frame.destroy()  # Clear the form after submission


    submit_btn = tk.Button(sub_frame, text="Submit", command=store)
    submit_btn.grid(row=12, column=1, padx=5, pady=5)

    return

# Update Existing Product 
def update_prod(panel):
    """
    Set up: [Left - Product Info]✓ [Right - Same as ADD info]✓
    """    
    my_prod = load_prod()

    # Formating for date MM/DD/YY
    def format_date(entry_widget, event=None):
        content = entry_widget.get()
        clean_content = content.replace("-", "")

        if len(clean_content) == 6 and clean_content.isdigit():
            formatted_date = clean_content[:2] + "/" + clean_content[2:4] + "/" + clean_content[4:]
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, formatted_date)
            entry_widget.config(bg="white")
        elif content:
            entry_widget.config(bg="lightcoral")

    def get_prod_data(name, products):
        for product in products:
            if product["Name"] == name:
                return product
        return None  # Return None if product is not found

    def on_select(event):
        # Get the selected product name from the listbox
        selection = event.widget.curselection()
        if selection:
            selected_name = event.widget.get(selection[0])  # Get the selected name
            # You could also immediately grab data here if needed
            # grab_data(selected_name)

    def grab_data():
        selection = users_listbox.curselection()  # Get current selection
        if not selection:
            messagebox.showwarning("No Selection", "Please select a product to grab.")
            return
        
        selected_name = users_listbox.get(selection[0])  # Get the selected name
        product = get_prod_data(selected_name, my_prod)
        
        if product:
            # Populate the text fields with the product's data
            prod_name_input.delete(0, tk.END)
            prod_name_input.insert(0, product["Name"])

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

            # Set the date added
            add_entry.delete(0, tk.END)
            add_entry.insert(0, product["Add"])
    
    def store():
        # Get the current values from the input fields
        name = prod_name_input.get()
        quantity = qty_input.get()
        food_group = var1.get()
        exp_date = date_entry.get()
        add_date = add_entry.get()

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
                    product["Exp"] = exp_date
                    product["Add"] = add_date
                    product["Info"] = nutritional_info
                    product_found = True
                    break

            if not product_found:
                messagebox.showwarning("Update Failed", f"Product '{name}' not found.")
                return

            # Move the file cursor to the beginning and overwrite the file
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()  # Truncate the file to avoid leftover data

        messagebox.showinfo("Update Successful", f"Product '{name}' updated successfully.")

    # Divide screen
    main_pane = tk.PanedWindow(panel, orient=tk.HORIZONTAL)
    main_pane.pack(fill=tk.BOTH, expand=True)

    # Left side = Product List
    left_frame = tk.Frame(main_pane)
    main_pane.add(left_frame, width=200)

    # Add "Click to Grab Produce" button
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

    # FOOD GROUP (Radio buttons)
    group_label = tk.Label(sub_frame, text="Food Group:")
    group_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

    var1 = tk.IntVar()
    food_groups = ["Dairy", "Fruits", "Vegetables", "Grains", "Protein", "Other"]
    for i, group in enumerate(food_groups, start=1):
        radio = tk.Radiobutton(sub_frame, text=group, variable=var1, value=i)
        radio.grid(row=3 + (i-1)//2, column=1 + (i-1)%2, padx=5, pady=5, sticky=tk.W)

    # NUTRITIONAL INFORMATION (Check buttons)
    info_label = tk.Label(sub_frame, text="Nutritional Information:")
    info_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)

    # Create IntVars for each nutrition checkbox
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

    # EXPIRATION DATE
    exp_date_label = tk.Label(sub_frame, text="Exp Date (MM/DD/YY):")
    exp_date_label.grid(row=10, column=0, padx=5, pady=5, sticky=tk.E)
    date_entry = tk.Entry(sub_frame)
    date_entry.grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)
    date_entry.bind("<FocusOut>", lambda e: format_date(date_entry))  # Bind date formatting

    # DATE ADDED
    add_date_label = tk.Label(sub_frame, text="Add Date (MM/DD/YY):")
    add_date_label.grid(row=11, column=0, padx=5, pady=5, sticky=tk.E)
    add_entry = tk.Entry(sub_frame)
    add_entry.grid(row=11, column=1, padx=5, pady=5, sticky=tk.W)
    add_entry.bind("<FocusOut>", lambda e: format_date(add_entry))  # Bind date formatting

    # Update button
    update_btn = tk.Button(sub_frame, text="Update", command=store)
    update_btn.grid(row=12, column=1, padx=5, pady=5)

    return


# Delete Existing Product
def delete_prod(panel):
    """
    Set up: [Top - Search]✓ [Bottom - Show Information]✓
    """  
    global my_prod  # Declare my_prod as global

    my_prod = load_prod()  # Load product data from the JSON file

    # Function to find a product by name
    def find_by_name():
        search_query = search_entry.get().lower()
        users_listbox.delete(0, tk.END)  # Clear current list
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
    Set up: [Top - Search]✓ [Bottom - Show Information]✓
    """  
    my_prod = load_prod()  # Load product data

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
                result_text.insert(tk.END, f"{prod['Name']} - {prod['Quantity']} QTY - {group_name} - {nutritional_info_str}\n")
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

# Starting point
if __name__ == "__main__":
    root = main_window()
    
    # Create a frame for buttons and panel for content
    frame = tk.Frame(root)
    frame.pack(side=tk.TOP, pady=20)
    
    panel = tk.Frame(root)
    panel.pack(side=tk.TOP, pady=20)
    
    # Create buttons and pass the panel for content display
    create_buttons(frame, panel)

    # Start the Tkinter main loop
    root.mainloop()
