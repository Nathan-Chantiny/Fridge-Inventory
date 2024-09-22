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
        add_new_user_panel(panel)
    elif index == 1:    # Update existing product
        add_update_panel(panel)
    elif index == 2:    # Delete existing product
        add_display_panel(panel)
    else:               # Search for product
        add_search_panel(panel)

# Add new product
def add_prod(panel):
    """
    Set up:
    Name [ Input ]
    QTY [ Input ]
    Type [ Radio Button ]
    Nutrition [ Check Button ]
    Exp Date [ MM/DD/YY ]
    Date Added [ MM/DD/YY ]
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

        


#### I LEFT OFF OVER HERE WILL FINISH TOMORROW ###

