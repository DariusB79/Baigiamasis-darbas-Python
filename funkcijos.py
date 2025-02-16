import sqlite3


def execute_query(database_name, query):
    with sqlite3.connect(database_name) as conn:
        c = conn.cursor()
        c.execute(query)
        conn.commit()


def preparation_data_for_database(header, input_data):
    output_data = []  # Sąrašas, kuris saugos žodynus
    for data in input_data:
        dict_data = {}
        for head, value in zip(header, data):  # Sujungiam antraštes su duomenimis
            dict_data[head] = value
        output_data.append(dict_data)  # Pridedame žodyną į sąrašą
    return output_data  # Grąžiname sąrašą su žodynais


def create_database_table(database_name, table_data):
    with sqlite3.connect(database_name) as conn:
        c = conn.cursor()
        c.execute(table_data)


def check_data_in_database_table(database_name, table_name):
    print(database_name)
    print(table_name)
    with sqlite3.connect(database_name) as conn:
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table_name}")
        rows = c.fetchall()
        for row in rows:
            print(row)
    #   conn.close()


def get_data_for_invoice(database_name, date):
    with sqlite3.connect(database_name) as conn:
        c = conn.cursor()
        data_shipping_date = c.execute(
            f"SELECT * From  Uzsakymai WHERE shipping_day = '{date}' "
        ).fetchall()
        return data_shipping_date


def get_clients_names(shipping_data):
    client_names_list = []
    for data in shipping_data:
        customer_name = data.get('Customer')  # Gauname 'Customer' reikšmę iš žodyno
        if customer_name and customer_name not in client_names_list:
            client_names_list.append(customer_name)
    return client_names_list


def get_data_for_invoice_list(database_name, date):
    with sqlite3.connect(database_name) as conn:
        conn.row_factory = sqlite3.Row  # Leis gauti duomenis kaip žodyną
        c = conn.cursor()
        c.execute(f"SELECT * FROM Uzsakymai WHERE Shipping_day = '{date}'")
        data = c.fetchall()
        return [dict(row) for row in data]  # Konvertuojam į dict sąrašą
    
def get_client_data_for_invoice(database_name, name):
  with sqlite3.connect(database_name) as conn:
        c = conn.cursor()
        data = c.execute(
            f"SELECT * From  Klientai WHERE Klientas = '{name}' "
        ).fetchall()
        return data
  
def get_invoice_data_by_client_name(data, name):
    data_for_invoice = []
    for d in data:
        customer_name = d.get("Customer")
        if name == customer_name :
            data_for_invoice.append(d)
    return data_for_invoice


