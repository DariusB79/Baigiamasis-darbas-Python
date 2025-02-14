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


class GoogleSheetsClient:
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
    ]
    TOKEN_PATH = r"C:\Users\HP\OneDrive\Desktop\phyton_mokymai\Paskaitos\_baigiamasis_darbas\creds\token.json"  # Save token here
    CREDENTIALS_PATH = r"C:\Users\HP\OneDrive\Desktop\phyton_mokymai\Paskaitos\_baigiamasis_darbas\creds\client_secret.json"

    def __init__(self):
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Authenticate user and get Gmail API service."""
        if os.path.exists(self.TOKEN_PATH):
            self.creds = Credentials.from_authorized_user_file(
                filename=self.TOKEN_PATH, scopes=self.SCOPES
            )

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDENTIALS_PATH, self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)

            # Save credentials for the next run
            with open(self.TOKEN_PATH, "w") as token:
                token.write(self.creds.to_json())

        # Initialize Gmail API service
        self.service = build("sheets", "v4", credentials=self.creds)

    def get_sheet_data(self, spreadsheet_id, sheet_range):
        """Fetch data from a specific Google Sheet."""
        try:
            sheet = self.service.spreadsheets()
            result = (
                sheet.values()
                .get(spreadsheetId=spreadsheet_id, range=sheet_range)
                .execute()
            )
            values = result.get("values", [])

            if not values:
                print("No data found.")
                return []

            return values

        except HttpError as err:
            print(f"Error fetching Google Sheet data: {err}")
            return []


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

# Print the results
sorted_orders = []
if data_orders:
    print("Pradedu spausdinti rezultatus :-) ")
    print()
    for row in data_orders:
        # print(f"{row[1]}, {row[2]}, {row[8]},{row[9]}, {row[11]}, {row[12]}, {row[13]}, {row[14]}, {row[15]}, {row[16]}, {row[17]} {row[21]}, {row[34]}")
        # print(f"{row[1]}, {row[2]}, {row[34]}")
        # print(row)
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
        # print()
    else:
        print("Nera duomenu")

for data in sorted_orders:
    print(data)
    print()

# Print the results Clients
# if data_clients:
# print("Pradedu spausdinti rezultatus :-) ")
# for row in data_clients:
## print(row)
# else:
#  print("Nera duomenu")

# if data_bank:
# print("Pradedu spausdinti rezultatus :-) ")
# for row in data_bank:
#  print(row)
# else:
# print("Nera duomenu")


# headers_clients = ['Klientas', 'Code', 'Vat_code', 'Adresas', 'Emailas', 'Shipping_adress', 'PVM', 'Apmokejimo terminas', 'Atsakingas', 'Telefonas', 'Bankas', 'Išankstinis_mok']


# data_for_clients_database = []

# for data in data_clients:
# dict_clients = {}
# for header, value in zip(headers_clients, data):
# dict_clients[header] = value
# data_for_clients_database.append(dict_clients)

# print("Spausdiname Klientu duomenu bazes duomenis")

# for data in data_for_clients_database:
# print(data)
# print()


# headers_bank = ['Name', 'Code', 'SWIFT', 'Account Nr']

# data_for_bank_database =[]

# for data in data_bank:
# dict_bank = {}
# for header, value in zip(headers_bank, data):
#  dict_bank[header] = value
# data_for_bank_database.append(dict_bank)

# print("Spausdiname Banko duomenu bazes duomenis")

# for data in data_for_bank_database:
# print(data)
# print()

# headers_orders = ['customer', 'order_Nr', 'shipping_day', 'project', 'code', 'ver', 'description', 'description_LT', 'qty', 'measure', 'discount', 'price_Eur', 'shipping_adress']

# data_for_orders_database = []

# for data in sorted_orders:
# dict_orders = {}
# for header, value in zip(headers_orders, data):
# dict_orders[header] = value
# print(dict_orders)
# data_for_orders_database.append(dict_orders)

# print("Spausdiname Uzsakymu duomenu bazes duomenis")

# for data in data_for_orders_database:
# print(data)
# print()


with sqlite3.connect("dotekas.db") as conn:  # context manager
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS Uzsakymai (Customer text, Order_Nr text, Shipping_day text, Project text, Code text, Ver text, Description text, Description_LT text, Qty integer, Measure text, Discount integer, Price_Eur  float, Shipping_adress text)"
    )

# with sqlite3.connect("dotekas.db") as conn: # context manager
# c = conn.cursor()
# c.execute(
#   "CREATE TABLE IF NOT EXISTS Bankai (Name text, Code text, SWIFT text, Account_Nr text)"
# )

# with sqlite3.connect("dotekas.db") as conn: # context manager
# c = conn.cursor()
# c.execute(
#    "CREATE TABLE IF NOT EXISTS Klientai (Klientas text, Code text, Vat_code text, Adresas text, Emailas text, Shipping_adress text, PVM integer, Apmokejimo_terminas integer, Atsakingas text, Telefonas text, Bankas text, Išankstinis_mok integer)"
# )


# with sqlite3.connect("dotekas.db") as conn: # context manager
# c = conn.cursor()
# for data in data_for_bank_database:
# c.execute("INSERT INTO Bankai  (Name, Code, SWIFT, Account_Nr) VALUES (?, ?, ?, ?)",
#            (data["Name"], data["Code"], data["SWIFT"], data["Account Nr"]))
# conn.commit()

# Patikriname, ar duomenys įkelti
# c.execute("SELECT * FROM Bankai")
# rows = c.fetchall()
# for row in rows:
#  print(row)
# Uždaryti prisijungimą
# conn.close()

# print(type(data_for_bank_database))
# print(data_for_bank_database)

# print(data.keys())

# with sqlite3.connect("dotekas.db") as conn: # context manager
# c = conn.cursor()
# for data in data_for_clients_database:
# try:
#  data["Išankstinis_mok"]
# except Exception:
# print(data)
# c.execute('''INSERT INTO Klientai
# (Klientas, Code, "Vat_code", Adresas, Emailas, "Shipping_adress", PVM, "Apmokejimo_terminas", Atsakingas, Telefonas, Bankas, "Išankstinis_mok")
# VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
# (data.get("Klientas", ""), data.get("Code", ""), data.get("Vat_code", ""), data.get("Adresas", ""),
# data.get("Emailas", ""), data.get("Shipping_adress", ""), data.get("PVM", ""), data.get("Apmokejimo_terminas", ""),
# data.get("Atsakingas", ""), data.get("Telefonas", ""), data.get("Bankas", ""), data.get("Išankstinis_mok", ""))
# )
# conn.commit()









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
    "Invoice"
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
                row[25],
            ]
        )
    else:
        print("Nera duomenu")

print_extracted_data(sorted_orders)

data_for_orders_database = preparation_data_for_database(
    header=HEADERS_ORDERS, input_data=sorted_orders
)
print_data_for_database(data_for_orders_database)


data_for_clients_database = preparation_data_for_database(
    header=HEADERS_CLIENTS, input_data=data_clients
)
print_data_for_database(data_for_database=data_for_clients_database)


data_for_bank_database = preparation_data_for_database(
    header=HEADERS_BANK, input_data=data_bank
)
print_data_for_database(data_for_database=data_for_bank_database)


create_database_table(database_name=MY_DATABASE, table_data=table_orders)
create_database_table(database_name=MY_DATABASE, table_data=table_clients)
create_database_table(database_name=MY_DATABASE, table_data=table_bank)


for row in data_for_bank_database:
    input_data_bank = f"""INSERT INTO Bankai (Name, Code, SWIFT, Account_Nr)
                VALUES ('{row["Name"]}', '{row["Code"]}', '{row["SWIFT"]}', '{row["Account_Nr"]}')"""
    print(input_data_bank)  # Tikriname, ar teisingai sugeneruoti SQL įrašai
    execute_query(database_name=MY_DATABASE, query=input_data_bank)


for row in data_for_clients_database:
    input_data_clients = (
        input_data_clients
    ) = f"""
INSERT INTO Klientai
   (Klientas, Code, "Vat_code", Adresas, Emailas, "Shipping_adress", PVM,
    "Apmokejimo_terminas", Atsakingas, Telefonas, Bankas, "Išankstinis_mok")
 VALUES
   ('{row.get("Klientas", "")}', '{row.get("Code", "")}', '{row.get("Vat_code", "")}', '{row.get("Adresas", "")}',
    '{row.get("Emailas", "")}', '{row.get("Shipping_adress", "")}', '{row.get("PVM", "")}', '{row.get("Apmokejimo_terminas", "")}',
    '{row.get("Atsakingas", "")}', '{row.get("Telefonas", "")}', '{row.get("Bankas", "")}', '{row.get("Išankstinis_mok", "")}')
 """
    execute_query(database_name=MY_DATABASE, query=input_data_clients)


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
    execute_query(database_name=MY_DATABASE, query=input_data_orders)

table_name_bank = "Bankai"
table_name_orders = "Uzsakymai"
table_name_clients = "Klientai"
check_data_in_database_table(database_name=MY_DATABASE, table_name=table_name_bank)
check_data_in_database_table(database_name=MY_DATABASE, table_name=table_name_orders)
check_data_in_database_table(database_name=MY_DATABASE, table_name=table_name_clients)







#class GmailClient:
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.send",
    ]
    TOKEN_PATH = r"C:\Users\HP\OneDrive\Desktop\phyton_mokymai\Paskaitos\_baigiamasis_darbas\creds\token_gmail.json"  # Save token here
    CREDENTIALS_PATH = r"C:\Users\HP\OneDrive\Desktop\phyton_mokymai\Paskaitos\_baigiamasis_darbas\creds\client_secret.json"

    def __init__(self):
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        if os.path.exists(self.TOKEN_PATH):
            self.creds = Credentials.from_authorized_user_file(
                filename=self.TOKEN_PATH, scopes=self.SCOPES
            )
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secrets_file=self.CREDENTIALS_PATH, scopes=self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            with open(self.TOKEN_PATH, "w") as token:
                token.write(self.creds.to_json())

        self.service = build(serviceName="gmail", version="v1", credentials=self.creds)

    def send_email(self, to_email, subject, content):
        try:
            message = EmailMessage()
            message.set_content(content)
            message["To"] = to_email
            message["Subject"] = subject

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {"raw": encoded_message}

            send_message = (
                self.service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
            print(f'Message Id: {send_message["id"]}')

        except HttpError as error:
            print(f"An error occurred: {error}")


