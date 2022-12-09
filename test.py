import tkinter as tk
from tkinter import ttk

# Create the root window
root = tk.Tk()

# Create the tree view widget
treeview = ttk.Treeview(root)

# Define the columns for the tree view
treeview["columns"] = ("col1", "col2")

# Set the column headings
treeview.heading("#0", text="Item")
treeview.heading("col1", text="Column 1")
treeview.heading("col2", text="Column 2")

# Add some data to the table
treeview.insert("", tk.END, text="Item 1", values=("Data 1", "Data 2"))
treeview.insert("", tk.END, text="Item 2", values=("Data 3", "Data 4"))

# Enable column resizing
treeview.column("#0", width=100, minwidth=100, stretch=tk.NO)
treeview.column("col1", width=100, minwidth=100, stretch=tk.NO)
treeview.column("col2", width=100, minwidth=100, stretch=tk.NO)

# Set the treeview widget to fill the root window
treeview.pack(fill=tk.BOTH, expand=True)
# Define the callback function
def on_row_double_click(event):
    # Get the selected item in the tree view
    selected_item = treeview.selection()[0]

    # Print the selected item's text and data
    print(treeview.item(selected_item, "text"))
    print(treeview.item(selected_item, "values"))

# Bind the double-click event to the tree view
treeview.bind("<Double-1>", on_row_double_click)
# Start the main event loop
root.mainloop()