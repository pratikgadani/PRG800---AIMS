import pyodbc
import pandas as pd
import os

# Function to fetch data from the database and export it to an Excel file
def export_to_excel():
    file_path = "D:\\College Material\\SEM 3\\PRG 800\\PRG800 - AIM\\table_data_report.xlsx"
    # Set up the connection parameters
    server = 'PRATIK\\SQLEXPRESS01'
    database = 'Temp_Project'
    username = ''  # For Windows authentication
    password = ''
    connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    connection = pyodbc.connect(connection_string)
    
    sql_query = "SELECT * FROM dbo.Table_data"

    df = pd.read_sql(sql_query, connection)

    connection.close()

    df.to_excel(file_path, index=False)

    print(f"Report exported successfully to: {file_path}")


