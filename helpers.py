import sqlite3


def create_database_table(database_name, table_data):
    with sqlite3.connect(database_name) as conn:
        c = conn.cursor()
        c.execute(table_data)


def preparation_data_for_database(header, input_data):
    output_data = []  
    for data in input_data:
        dict_data = {}
        for head, value in zip(header, data):  
            dict_data[head] = value
        output_data.append(dict_data) 
    return output_data 

def check_data_in_database_table(database_name, table_name):
    with sqlite3.connect(database_name) as conn:
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table_name}")
        rows = c.fetchall()
        for row in rows:
            print(row)
   

def get_data_for_invoice(database_name, date, as_dict=False):
    with sqlite3.connect(database_name) as conn:
        if as_dict:
            conn.row_factory = sqlite3.Row  # Leidžia gauti duomenis kaip žodyną
        c = conn.cursor()
        c.execute(f"SELECT * FROM Uzsakymai WHERE Shipping_day = ?", (date,))
        data = c.fetchall()
        return [dict(row) for row in data] if as_dict else data


def get_clients_names(shipping_data):
    client_names_list = []
    for data in shipping_data:
        if isinstance(data, dict): 
            customer_name = data.get("Customer")
        elif (
            isinstance(data, tuple) and len(data) > 0
        ):  # Jei tuple, imame pirmą elementą
            customer_name = data[0]
        else:
            continue  # Jei neatitinka nė vieno varianto, praleidžiame
        if customer_name and customer_name not in client_names_list:
            client_names_list.append(customer_name)
    return client_names_list


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
        if name == customer_name:
            data_for_invoice.append(d)
    return data_for_invoice
