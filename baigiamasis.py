import os
import os.path
import gspread
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import sqlite3
from tabulate import tabulate
from IPython.display import HTML

from klases import GoogleSheetsClient 

# Create a Google Sheets client instance
sheets_client = GoogleSheetsClient()
print("Google Sheets API authenticated successfully!")

# Correct Spreadsheet ID (without the full URL)
spreadsheet_id_orders = "1bIfOXOcBFOyKEDqLav5xDHQ5XNf8eIONm754RDT0WJk"
range_name_orders = "ORDERS!A13802:AJ"

spreadsheet_id_clients = "1MTZece9viYPeK0mdfUXcFbZEgsgv4xojsEbveGxAT84"
range_name_clients = "Imones!A2:L"

spreadsheet_id_bank = "1MTZece9viYPeK0mdfUXcFbZEgsgv4xojsEbveGxAT84"
range_name_bank = "Bankai!A1:D"

# Fetch data from Google Sheets
data_orders = sheets_client.get_sheet_data(spreadsheet_id_orders, range_name_orders)
data_clients = sheets_client.get_sheet_data(spreadsheet_id_clients, range_name_clients)
data_bank = sheets_client.get_sheet_data(spreadsheet_id_bank, range_name_bank)


def print_extracted_data(extracted_data):
   if extracted_data:
    print("Pradedu spausdinti rezultatus :-) ")
    for row in extracted_data:
     print(row)
    else:
     print("Nera duomenu")
   
print_extracted_data(extracted_data=data_orders)

print_extracted_data(extracted_data=data_clients)

print_extracted_data(extracted_data=data_bank)


def print_data_for_database(data_for_database):
   print("Suvedimui skirtu duomenu spausdinimas")
   for data in data_for_database:
    print(data)
    print()

def preparation_data_for_database(header, input_data, output_data ):
    for data in input_data:
     dict_data = {}
     for header, value in zip(headers_orders, data):
        dict_data[header] = value
     output_data.append(dict_data)
    return output_data

def create_database_table(database_name, table_data):
    with sqlite3.connect(database_name) as conn:
      c = conn.cursor()
      c.execute( table_data )

def check_data_in_database_table(database_name, table_name):
    with sqlite3.connect(database_name) as conn:
       c = conn.cursor()
       c.execute(f"SELECT * FROM {table_name}")
       rows = c.fetchall()
       for row in rows:
         print(row)
       conn.close()

def add_data_in_data_base(database_name, input_data, input_information):
 with sqlite3.connect(database_name) as conn:
    c = conn.cursor()
    for data in input_data:
        c.execute(f"{input_information}")
    conn.commit()  


sorted_orders = []
if data_orders:
    for row in data_orders:
        sorted_orders.append([row[1], row[2], row[8],row[9], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[21], row[34]])
    else:
      print("Nera duomenu")

headers_orders = ['customer', 'order_Nr', 'shipping_day', 'project', 'code', 'ver', 'description', 'description_LT', 'qty', 'measure', 'discount', 'price_Eur', 'shipping_adress']
data_for_orders_database = []
preparation_data_for_database(header=headers_orders, input_data=sorted_orders, output_data=data_for_orders_database)
print_data_for_database(data_for_database=data_for_orders_database)

headers_clients = ['Klientas', 'Code', 'Vat_code', 'Adresas', 'Emailas', 'Shipping_adress', 'PVM', 'Apmokejimo terminas', 'Atsakingas', 'Telefonas', 'Bankas', 'Išankstinis_mok']
data_for_clients_database = []
preparation_data_for_database(header=headers_clients, input_data=data_clients, output_data=data_for_clients_database)
print_data_for_database(data_for_database=data_for_clients_database)

headers_bank = ['Name', 'Code', 'SWIFT', 'Account Nr']
data_for_bank_database =[]
preparation_data_for_database(header=headers_bank, input_data=data_bank, output_data=data_for_bank_database)
print_data_for_database(data_for_database=data_for_bank_database)

my_database = "dotekas.db"
table_orders = "CREATE TABLE IF NOT EXISTS Uzsakymai (Customer text, Order_Nr text, Shipping_day text, Project text, Code text, Ver text, Description text, Description_LT text, Qty integer, Measure text, Discount integer, Price_Eur  float, Shipping_adress text)"
table_clients= "CREATE TABLE IF NOT EXISTS Klientai (Klientas text, Code text, Vat_code text, Adresas text, Emailas text, Shipping_adress text, PVM integer, Apmokejimo_terminas integer, Atsakingas text, Telefonas text, Bankas text, Išankstinis_mok integer)"
table_bank= "CREATE TABLE IF NOT EXISTS Bankai (Name text, Code text, SWIFT text, Account_Nr text)"
create_database_table(database_name=my_database, table_data=table_orders)
create_database_table(database_name=my_database, table_data=table_clients)
create_database_table(database_name=my_database, table_data=table_bank)



input_data_clients = f'''INSERT INTO Klientai 
    (Klientas, Code, "Vat_code", Adresas, Emailas, "Shipping_adress", PVM, "Apmokejimo_terminas", Atsakingas, Telefonas, Bankas, "Išankstinis_mok") 
    VALUES ('{data["Klientas"]}', '{data["Code"]}', '{data["Vat_code"]}', '{data["Adresas"]}', 
            '{data["Emailas"]}', '{data["Shipping_adress"]}', '{data["PVM"]}', '{data["Apmokejimo_terminas"]}', 
            '{data["Atsakingas"]}', '{data["Telefonas"]}', '{data["Bankas"]}', '{data["Išankstinis_mok"]}')'''


input_data_bank = f'''INSERT INTO Bankai (Name, Code, SWIFT, Account_Nr)
             VALUES ('{data["Name"]}', '{data["Code"]}', '{data["WIFT"]}', '{data["Account_Nr"]}')'''


input_data_orders = f'''INSERT INTO Uzsakymai (customer, order_Nr, shipping_day, project, 
            code, ver, description, description_LT, qty, measure, discount, price_Eur, shipping_adress)
 VALUES  ('{data["customer"]}', '{data["order_Nr"]}', '{data["shipping_day"]}', '{data["project"]}', 
            '{data["code"]}', '{data["ver"]}', '{data["description"]}', '{data["description_LT"]}', 
            '{data["qty"]}', '{data["measure"]}', '{data["discount"]}', '{data["price_Eur"]}', '{data["shipping_adress"]}')'''



add_data_in_data_base(database_name=my_database, input_data=data_for_bank_database, input_information=input_data_bank)
add_data_in_data_base(database_name=my_database, input_data=data_for_clients_database, input_information=input_data_clients)
add_data_in_data_base(database_name=my_database, input_data=data_for_orders_database, input_information=input_data_orders)


table_name_bank = "Bankai"
table_name_orders = "Uzsakymai"
table_name_clients = "Klientai"
check_data_in_database_table(database_name=my_database, table_name=table_name_bank)
check_data_in_database_table(database_name=my_database, table_name=table_name_orders)
check_data_in_database_table(database_name=my_database, table_name=table_name_clients)






