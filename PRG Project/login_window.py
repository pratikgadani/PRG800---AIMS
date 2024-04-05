import pyodbc
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import main_window

def create_login_window():
    login_window = tk.Tk()
    login_window.title("Login to Automated Inventory Management System")
    login_window.geometry("500x400")    
    
    def connect_to_database():
        server = 'PRATIK\\SQLEXPRESS01'
        database = 'Temp_Project'
        username = ''  # For Windows authentication
        password = ''
        connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        return pyodbc.connect(connection_string)

    # Authenticate user
    def authenticate_user(username, password):
        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute("SELECT password, access_level FROM User_data WHERE id = ?", username)
            row = cursor.fetchone()
            if row:
                stored_password, access_level = row  # Fetch the stored password and access_level from the database
                if stored_password == password:  # Compare stored password with the entered password
                    if access_level == "Users":
                        main_window.create_main_window("User", login_window)
                    elif access_level == "Administrators":
                        main_window.create_main_window("Administrators",login_window)
            else:
                 status_label = login_window.children["status_label"]
                 status_label.config(text="Invalid username or password")
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"Database Error: {e}")
        finally:
            connection.close()
            
    def login_button_clicked():
        username = username_entry.get()
        password = password_entry.get()
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        authenticate_user(username, password)    
        
    def close_button_clicked():
        login_window.destroy()
         
    # Widgets for the login window
    frame1=tk.Frame(login_window)
    frame1.pack(expand=True)
    
    frame2=tk.Frame(login_window)
    ttk.Label(login_window, text="Welcome to Automated Inventory Manangement System").pack(anchor="center",pady=15)
    ttk.Label(login_window, text="Username:").pack()
    username_entry = ttk.Entry(login_window)
    username_entry.pack()
    
    ttk.Label(login_window, text="Password:").pack()
    password_entry = ttk.Entry(login_window, show="*")
    password_entry.pack()
    
    login_button = ttk.Button(login_window, text="Login",command=login_button_clicked)
    login_button.pack()

    ttk.Label(login_window, text="", name="status_label").pack()
    ttk.Label(login_window, text="Created by team Super6 for PRG800 Programming Project").pack(pady=10)
    frame2.pack(anchor="center")
    
    frame3=tk.Frame(login_window)
    frame3.pack(expand=True)
    
    close_button = ttk.Button(login_window, text="Close",command=close_button_clicked)
    close_button.pack(side='right',padx=10,pady=10)

    return login_window


if __name__ == "__main__":
    create_login_window().mainloop()
