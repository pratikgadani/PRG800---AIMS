import pyodbc
import tkinter as tk
from tkinter import ttk

# Create the user window
def create_main_window(user_type,login_window):
    user_window = tk.Tk()
    user_window.geometry(user_window.geometry(f"+{login_window.winfo_x()}+{login_window.winfo_y()}"))
    user_window.title(f"AIMS - {user_type}")

        
    def add_product_quantity(barcode):
        # Increment Total_Quantity and Remaining_Quantity by 1 for the given barcode
        cursor.execute("SELECT * FROM dbo.Table_data WHERE Barcode_Number = ?", barcode)
            # Increment Total_Quantity and Remaining_Quantity by 1 for the given barcode
        if cursor.fetchone(): 
            cursor.execute("""
                UPDATE dbo.Table_data
                SET Total_Quantity = Total_Quantity + 1,
                    Remaining_Quantity = Remaining_Quantity + 1
                WHERE Barcode_Number = ?
            """, barcode)
            connection.commit()
            update_status(f"Quantity increased for barcode: {barcode}")
        else:
            update_status(f"Error: Item with barcode {barcode} not found in the database") 


    def remove_product_quantity(barcode):
        # Check if Remaining_Quantity is greater than 0 before decreasing it
        cursor.execute("SELECT Remaining_Quantity FROM dbo.Table_data WHERE Barcode_Number = ?", barcode)
        remaining_quantity = cursor.fetchone()[0]

        if remaining_quantity > 0:
            # Decrease Remaining_Quantity by 1 for the given barcode
            cursor.execute("""
                UPDATE dbo.Table_data
                SET Remaining_Quantity = Remaining_Quantity - 1
                WHERE Barcode_Number = ?
            """, barcode)
            connection.commit()
            update_status(f"Quantity decreased for barcode: {barcode}")
        else:
            update_status(f"Error: Quantity is already 0 for barcode: {barcode}")

#    def reset_total_quantity():
#        # Reset Total_Quantity and Remaining_Quantity to zero for all products
#        cursor.execute("""
#            UPDATE dbo.Table_data
#            SET Total_Quantity = 0,
#                Remaining_Quantity = 0
#        """)
#        connection.commit()
#        update_status("Total and Remaining quantities reset to zero for all products")

    def update_manual_quantity(barcode, total_quantity, remaining_quantity):
        # Update Total_Quantity and Remaining_Quantity manually for the given barcode
        cursor.execute("""
            UPDATE dbo.Table_data
            SET Total_Quantity = ?,
                Remaining_Quantity = ?
            WHERE Barcode_Number = ?
        """, total_quantity, remaining_quantity, barcode)
        connection.commit()
        update_status(f"Manual update for barcode: {barcode}")
        manual_entry_barcode.delete(0, tk.END)
        manual_entry_total_quantity.delete(0, tk.END)
        manual_entry_remaining_quantity.delete(0, tk.END)

    def toggle_action():
        # Toggle between 'add' and 'remove'
        action.set('add' if action.get() == 'remove' else 'remove')
        update_status(f"Action mode toggled to: {action.get()}")

    def update_status(message):
        status_label.config(text=message)

    def process_barcode(event):
        barcode = barcode_entry.get()

        if action.get() == 'add':
            add_product_quantity(barcode)
        elif action.get() == 'remove':
            remove_product_quantity(barcode)

        barcode_entry.delete(0, tk.END)  # Clear the barcode entry

        # Display product name for the scanned barcode
        cursor.execute("SELECT Product_Name FROM dbo.Table_data WHERE Barcode_Number = ?", barcode)
        result = cursor.fetchone()
        product_name_label.config(text=f"Product Name: {result[0] if result else 'Not Found'}")

    def process_manual_entry():
        barcode = manual_entry_barcode.get()
        total_quantity = manual_entry_total_quantity.get()
        remaining_quantity = manual_entry_remaining_quantity.get()

        update_manual_quantity(barcode, total_quantity, remaining_quantity)
    
    def logout_button_clicked():
        user_window.destroy()
        login_window.iconify()    
        login_window.deiconify()
        

    # Variables
    action = tk.StringVar(value='add')  
        
    
    # Set up the connection parameters
    server = 'PRATIK\\SQLEXPRESS01'
    database = 'Temp_Project'
    username = ''  # For Windows authentication
    password = ''

    # Create a connection string with Trusted_Connection=yes for Windows authentication
    connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

    # Establish the database connection
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()


    # Widgets
    frame = ttk.Frame(user_window, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame, text="Action:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    remove_radio = ttk.Radiobutton(frame, text="Remove", variable=action, value='remove', command=toggle_action)
    add_radio = ttk.Radiobutton(frame, text="Add", variable=action, value='add', command=toggle_action)
    remove_radio.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    add_radio.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

    ttk.Label(frame, text="Scan Barcode:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    barcode_entry = ttk.Entry(frame)
    barcode_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W + tk.E)

    product_name_label = ttk.Label(frame, text="Product Name:")
    product_name_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)

    # Reset button
    #reset_button = ttk.Button(frame, text="Reset Total and Remaining Quantity", command=reset_total_quantity)
    #reset_button.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

    # Manual entry section
    manual_entry_barcode_label = ttk.Label(frame, text="Barcode:")
    manual_entry_barcode_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
    manual_entry_barcode = ttk.Entry(frame)
    manual_entry_barcode.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

    manual_entry_total_quantity_label = ttk.Label(frame, text="Total Quantity:")
    manual_entry_total_quantity_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
    manual_entry_total_quantity = ttk.Entry(frame)
    manual_entry_total_quantity.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

    manual_entry_remaining_quantity_label = ttk.Label(frame, text="Remaining Quantity:")
    manual_entry_remaining_quantity_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
    manual_entry_remaining_quantity = ttk.Entry(frame)
    manual_entry_remaining_quantity.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W + tk.E)

    process_manual_button = ttk.Button(frame, text="Process Manual Entry", command=process_manual_entry)
    process_manual_button.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)

    status_label = ttk.Label(frame, text="")
    status_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)

    # Logout button
    logout_button = ttk.Button(user_window, text="Logout",command=logout_button_clicked)
    logout_button.grid(row=9, column=0, padx=5, pady=5, sticky=tk.E)

    # Bind the Enter key to the process_barcode function
    user_window.bind('<Return>', process_barcode)

    
    # Start the GUI event loop
    login_window.withdraw()
    user_window.mainloop()
    
    # Close the cursor and connection
    cursor.close()
    connection.close()