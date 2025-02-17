import os
import os.path
import gspread
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import sqlite3
from tabulate import tabulate
from IPython.display import HTML
import logging
import pdfkit
from debug_helpers import print_data_for_database, print_extracted_data
from helpers import (
    preparation_data_for_database,
    create_database_table,
    check_data_in_database_table,
    get_data_for_invoice,
    get_clients_names,
)
from klases import GoogleSheetsClient, GmailClient


load_dotenv()

spreadsheet_id_orders = os.getenv("spreadsheet_id_orders")
range_name_orders = os.getenv("range_name_orders")
spreadsheet_id_clients = os.getenv("spreadsheet_id_clients")
range_name_clients = os.getenv("range_name_clients")
spreadsheet_id_bank = os.getenv("spreadsheet_id_bank")
range_name_bank = os.getenv("range_name_bank")

# Create a Google Sheets client instance
sheets_client = GoogleSheetsClient()
logging.warning("Google Sheets API authenticated successfully!")

MY_DATABASE = "dotekas.db"

table_orders = "CREATE TABLE IF NOT EXISTS Uzsakymai (Customer text, Order_Nr text, Shipping_day text, Project text, Code text, Ver text, Description text, Description_LT text, Qty integer, Measure text, Discount integer, Price_Eur  float, Shipping_adress text, Invoice integer)"

table_clients = "CREATE TABLE IF NOT EXISTS Klientai (Klientas text, Code text, Vat_code text, Adresas text, Emailas text, Shipping_adress text, PVM integer, Apmokejimo_terminas integer, Atsakingas text, Telefonas text, Bankas text, Išankstinis_mok integer)"

table_bank = "CREATE TABLE IF NOT EXISTS Bankai (Name text, Code text, SWIFT text, Account_Nr text)"

HEADERS_ORDERS = [
    "customer",
    "order_Nr",
    "shipping_day",
    "project",
    "code",
    "ver",
    "description",
    "description_LT",
    "qty",
    "measure",
    "discount",
    "price_Eur",
    "shipping_adress",
    "Invoice",
]
HEADERS_CLIENTS = [
    "Klientas",
    "Code",
    "Vat_code",
    "Adresas",
    "Emailas",
    "Shipping_adress",
    "PVM",
    "Apmokejimo_terminas",
    "Atsakingas",
    "Telefonas",
    "Bankas",
    "Išankstinis_mok",
]
HEADERS_BANK = ["Name", "Code", "SWIFT", "Account_Nr"]

# Fetch data from Google Sheets
data_orders = sheets_client.get_sheet_data(spreadsheet_id_orders, range_name_orders)
data_clients = sheets_client.get_sheet_data(spreadsheet_id_clients, range_name_clients)
data_bank = sheets_client.get_sheet_data(spreadsheet_id_bank, range_name_bank)
# print_extracted_data(extracted_data=data_orders)
# print_extracted_data(extracted_data=data_clients)
# print_extracted_data(extracted_data=data_bank)

sorted_orders = []
if data_orders:
    for row in data_orders:
        sorted_orders.append(
            [
                row[1],
                row[2],
                row[8],
                row[9],
                row[11],
                row[12],
                row[13],
                row[14],
                row[15],
                row[16],
                row[17],
                row[21],
                row[25],
            ]
        )
    else:
        print("Nera duomenu")

# print_extracted_data(sorted_orders)

data_for_orders_database = preparation_data_for_database(
    header=HEADERS_ORDERS, input_data=sorted_orders
)
# print_data_for_database(data_for_orders_database)


data_for_clients_database = preparation_data_for_database(
    header=HEADERS_CLIENTS, input_data=data_clients
)
# print_data_for_database(data_for_database=data_for_clients_database)


data_for_bank_database = preparation_data_for_database(
    header=HEADERS_BANK, input_data=data_bank
)
# print_data_for_database(data_for_database=data_for_bank_database)


create_database_table(database_name=MY_DATABASE, table_data=table_orders)
create_database_table(database_name=MY_DATABASE, table_data=table_clients)
create_database_table(database_name=MY_DATABASE, table_data=table_bank)


for row in data_for_bank_database:
    input_data_bank = f"""INSERT INTO Bankai (Name, Code, SWIFT, Account_Nr)
                VALUES ('{row["Name"]}', '{row["Code"]}', '{row["SWIFT"]}', '{row["Account_Nr"]}')"""
    print(input_data_bank)  # Tikriname, ar teisingai sugeneruoti SQL įrašai
    create_database_table(database_name=MY_DATABASE, table_data=input_data_bank)


for row in data_for_clients_database:
    input_data_clients = input_data_clients = f"""
INSERT INTO Klientai
   (Klientas, Code, "Vat_code", Adresas, Emailas, "Shipping_adress", PVM,
    "Apmokejimo_terminas", Atsakingas, Telefonas, Bankas, "Išankstinis_mok")
 VALUES
   ('{row.get("Klientas", "")}', '{row.get("Code", "")}', '{row.get("Vat_code", "")}', '{row.get("Adresas", "")}',
    '{row.get("Emailas", "")}', '{row.get("Shipping_adress", "")}', '{row.get("PVM", "")}', '{row.get("Apmokejimo_terminas", "")}',
    '{row.get("Atsakingas", "")}', '{row.get("Telefonas", "")}', '{row.get("Bankas", "")}', '{row.get("Išankstinis_mok", "")}')
 """
    create_database_table(database_name=MY_DATABASE, table_data=input_data_clients)


for row in data_for_orders_database:
    input_data_orders = f"""
    INSERT INTO Uzsakymai (
       customer, order_Nr, shipping_day, project,
       code, ver, description, description_LT,
       qty, measure, discount, price_Eur, shipping_adress, Invoice
    )
    VALUES (
       '{row.get("customer", "")}', '{row.get("order_Nr", "")}', '{row.get("shipping_day", "")}', '{row.get("project", "")}',
       '{row.get("code", "")}', '{row.get("ver", "")}', '{row.get("description", "")}', '{row.get("description_LT", "")}',
       '{row.get("qty", "")}', '{row.get("measure", "")}', '{row.get("discount", "")}', '{row.get("price_Eur", "")}',
       '{row.get("shipping_adress", "")}', '{row.get("Invoice", "")}'
    )
    """
    create_database_table(database_name=MY_DATABASE, table_data=input_data_orders)

table_name_bank = "Bankai"
table_name_orders = "Uzsakymai"
table_name_clients = "Klientai"
check_data_in_database_table(database_name=MY_DATABASE, table_name=table_name_bank)
check_data_in_database_table(database_name=MY_DATABASE, table_name=table_name_orders)
check_data_in_database_table(database_name=MY_DATABASE, table_name=table_name_clients)

# shipping_date = input(str("Iveskite norimo isvezimo data"))
data_for_invoice = get_data_for_invoice(database_name=MY_DATABASE, date="2025/02/07")

duomenys = get_data_for_invoice(database_name=MY_DATABASE, date="2025/02/07")
for n in duomenys:
    print(n)

gmail_client = GmailClient()
gmail_client.send_email_with_attachment(
    to_email="d.balsevicius@gmail.com",
    subject="Please find atached invoice for your orders",
    content="Hello,\n \n Please find atached invoice for your orders \n\n Have a nice day \n BR, \n Darius Balsevicius",
    file_path=r"C:\Users\HP\OneDrive\Desktop\phyton_mokymai\Paskaitos\_baigiamasis_darbas\invoice.pdf",
)
