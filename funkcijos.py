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


