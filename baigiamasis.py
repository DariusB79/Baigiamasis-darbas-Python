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

from debug_functions import print_data_for_database, print_extracted_data
from klases import GoogleSheetsClient


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
]
HEADERS_CLIENTS = [
    "Klientas",
    "Code",
    "Vat_code",
    "Adresas",
    "Emailas",
    "Shipping_adress",
    "PVM",
    "Apmokejimo terminas",
    "Atsakingas",
    "Telefonas",
    "Bankas",
    "Išankstinis_mok",
]
HEADERS_BANK = ["Name", "Code", "SWIFT", "Account Nr"]
MY_DATABASE = "dotekas.db"

table_orders = "CREATE TABLE IF NOT EXISTS Uzsakymai (Customer text, Order_Nr text, Shipping_day text, Project text, Code text, Ver text, Description text, Description_LT text, Qty integer, Measure text, Discount integer, Price_Eur  float, Shipping_adress text)"

table_clients = "CREATE TABLE IF NOT EXISTS Klientai (Klientas text, Code text, Vat_code text, Adresas text, Emailas text, Shipping_adress text, PVM integer, Apmokejimo_terminas integer, Atsakingas text, Telefonas text, Bankas text, Išankstinis_mok integer)"

table_bank = "CREATE TABLE IF NOT EXISTS Bankai (Name text, Code text, SWIFT text, Account_Nr text)"

input_data_bank = """INSERT INTO Bankai (Name, Code, SWIFT, Account_Nr)
             VALUES ('{name}', '{code}', '{swift}', '{account_nr}')"""


# input_data_bank = """INSERT INTO Bankai (Name, Code, SWIFT, Account_Nr)
#              VALUES ('{row["Name"]}', '{row["Code"]}', '{row["WIFT"]}', '{row["Account_Nr"]}')"""


def execute_query(database_name, query):
    with sqlite3.connect(database_name) as conn:
        c = conn.cursor()
        c.execute(query)
        conn.commit()


def preparation_data_for_database(header, input_data):
    output_data = []
    for data in input_data:
        dict_data = {}
        for header, value in zip(HEADERS_ORDERS, data):
            dict_data[header] = value
        output_data.append(dict_data)
    return output_data


def create_database_table(database_name, table_data):
    with sqlite3.connect(database_name) as conn:
        c = conn.cursor()
        c.execute(table_data)


def check_data_in_database_table(database_name, table_name):
    with sqlite3.connect(database_name) as conn:
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table_name}")
        rows = c.fetchall()
        for row in rows:
            print(row)
        conn.close()


# Fetch data from Google Sheets
data_orders = sheets_client.get_sheet_data(spreadsheet_id_orders, range_name_orders)
data_clients = sheets_client.get_sheet_data(spreadsheet_id_clients, range_name_clients)
data_bank = sheets_client.get_sheet_data(spreadsheet_id_bank, range_name_bank)
print_extracted_data(extracted_data=data_orders)
print_extracted_data(extracted_data=data_clients)
print_extracted_data(extracted_data=data_bank)
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
                row[34],
            ]
        )
    else:
        print("Nera duomenu")


data_for_orders_database = preparation_data_for_database(
    header=HEADERS_ORDERS,
    input_data=sorted_orders,
)
print_data_for_database(data_for_database=data_for_orders_database)


data_for_clients_database = []
preparation_data_for_database(
    header=HEADERS_CLIENTS,
    input_data=data_clients,
    output_data=data_for_clients_database,
)
print_data_for_database(data_for_database=data_for_clients_database)


data_for_bank_database = []
preparation_data_for_database(
    header=HEADERS_BANK, input_data=data_bank, output_data=data_for_bank_database
)
print_data_for_database(data_for_database=data_for_bank_database)

create_database_table(database_name=MY_DATABASE, table_data=table_orders)
create_database_table(database_name=MY_DATABASE, table_data=table_clients)
create_database_table(database_name=MY_DATABASE, table_data=table_bank)


for row in data_for_bank_database:
    execute_query(
        database_name=MY_DATABASE,
        query=input_data_bank.format(
            name=row["Name"],
            code=row["Code"],
            swift=row["SWIFT"],
            account_nr=row["Account_Nr"],
        ),
    )


input_data_clients = f"""
INSERT INTO Klientai 
    (Klientas, Code, "Vat_code", Adresas, Emailas, "Shipping_adress", PVM, 
     "Apmokejimo_terminas", Atsakingas, Telefonas, Bankas, "Išankstinis_mok") 
VALUES 
    ('{row["Klientas"]}', '{row["Code"]}', '{row["Vat_code"]}', '{row["Adresas"]}', 
     '{row["Emailas"]}', '{row["Shipping_adress"]}', '{row["PVM"]}', '{row["Apmokejimo_terminas"]}', 
     '{row["Atsakingas"]}', '{row["Telefonas"]}', '{row["Bankas"]}', '{row["Išankstinis_mok"]}')
"""

for row in data_for_clients_database:
    execute_query(database_name=MY_DATABASE, query=input_data_clients)


input_data_orders = f"""
INSERT INTO Uzsakymai (
    customer, order_Nr, shipping_day, project, 
    code, ver, description, description_LT, 
    qty, measure, discount, price_Eur, shipping_adress
) 
VALUES (
    '{row["customer"]}', '{row["order_Nr"]}', '{row["shipping_day"]}', '{row["project"]}', 
    '{row["code"]}', '{row["ver"]}', '{row["description"]}', '{row["description_LT"]}', 
    '{row["qty"]}', '{row["measure"]}', '{row["discount"]}', '{row["price_Eur"]}', 
    '{row["shipping_adress"]}'
)
"""

for row in data_for_orders_database:
    execute_query(database_name=MY_DATABASE, query=input_data_orders)


table_name_bank = "Bankai"
table_name_orders = "Uzsakymai"
table_name_clients = "Klientai"
check_data_in_database_table(database_name=MY_DATABASE, table_name=table_name_bank)
check_data_in_database_table(database_name=MY_DATABASE, table_name=table_name_orders)
check_data_in_database_table(database_name=MY_DATABASE, table_name=table_name_clients)
