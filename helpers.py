import sqlite3

SELECT_FROM_UZSAKYMAI_QUERY = "SELECT * FROM Uzsakymai WHERE Shipping_day = '{date}'"


def execute_sql_query(database_name, query, as_dict=False):
    with sqlite3.connect(database_name) as conn:
        if as_dict:
            conn.row_factory = sqlite3.Row  # Leidžia gauti duomenis kaip žodyną
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        if "SELECT" in query.upper():
            return c.fetchall()


def get_data_for_invoice(database_name, date, as_dict=False):
    r = execute_sql_query(
        database_name=database_name,
        query=SELECT_FROM_UZSAKYMAI_QUERY.format(date=date),
        as_dict=True,
    )
    return [dict(row) for row in r] if as_dict else r


def get_client_data_for_invoice(database_name, name):
    return execute_sql_query(
        database_name=database_name,
        query=f"SELECT * From  Klientai WHERE Klientas = '{name}' ",
    )

def preparation_data_for_database(header, input_data):
    output_data = []
    for data in input_data:
        dict_data = {}
        for head, value in zip(header, data):
            dict_data[head] = value
        output_data.append(dict_data)
    return output_data


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


def get_invoice_data_by_client_name(data, name):
    data_for_invoice = []
    for d in data:
        customer_name = d.get("Customer")
        if name == customer_name:
            data_for_invoice.append(d)
    return data_for_invoice
