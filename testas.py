import sqlite3
import pdfkit

#with sqlite3.connect("dotekas.db") as conn:  # context manager
 #  c = conn.cursor()
#   c.execute("DROP TABLE IF EXISTS Uzsakymai1")


# Prisijungiame prie duomenų bazės
#conn = sqlite3.connect("dotekas.db")
#cursor = conn.cursor()
# Pridedame naują stulpelį, pvz., "Komentaras" (TEXT tipo)
#cursor.execute("ALTER TABLE Uzsakymai ADD COLUMN Invoice INTEGER;")
# Išsaugome pakeitimus
#conn.commit()
# Uždarome jungtį
#conn.close()

with sqlite3.connect("dotekas.db") as conn: # context manager
  c = conn.cursor()
  c.execute("DELETE FROM  Klientai")
  c.execute("DELETE FROM  Bankai")
  c.execute("DELETE FROM  Uzsakymai")
  conn.commit()

# print(type(data_for_bank_database))
# print(data_for_bank_database)

# print(data.keys())






#with sqlite3.connect("dotekas.db") as conn:
#    c = conn.cursor()
#    c.execute("PRAGMA table_info(Bankai)")
#print(c.fetchall())




# input_data_bank = f"""INSERT INTO Bankai (Name, Code, SWIFT, Account_Nr)
#            VALUES ('{row["Name"]}', '{row["Code"]}', '{row["SWIFT"]}', '{row["Account_Nr"]}')"""


# for row in data_for_bank_database:
#   execute_query(database_name=MY_DATABASE, query=input_data_bank)


# input_data_bank = """INSERT INTO Bankai (Name, Code, SWIFT, Account_Nr)
#                VALUES ('{Name}', '{Code}', '{swift}', '{Account_Nr}')"


# for row in data_for_bank_database:
#    print(row)
#    print("Tai ko mums reikia :-) ")
#    execute_query(
#       database_name=MY_DATABASE,
#        query=input_data_bank.format(
#           name=row["Name"],
#            code=row["Code"],
#            swift=row["SWIFT"],
#            account_nr=row["Account_Nr"],
#        ),
#    )


# input_data_clients = f"""
# INSERT INTO Klientai
#   (Klientas, Code, "Vat_code", Adresas, Emailas, "Shipping_adress", PVM,
#   "Apmokejimo_terminas", Atsakingas, Telefonas, Bankas, "Išankstinis_mok")
# VALUES
#  ('{row["Klientas"]}', '{row["Code"]}', '{row["Vat_code"]}', '{row["Adresas"]}',
#   '{row["Emailas"]}', '{row["Shipping_adress"]}', '{row["PVM"]}', '{row["Apmokejimo_terminas"]}',
#   '{row["Atsakingas"]}', '{row["Telefonas"]}', '{row["Bankas"]}', '{row["Išankstinis_mok"]}')
# """

# for row in data_for_clients_database:
#    execute_query(database_name=MY_DATABASE, query=input_data_clients)

# input_data_orders = f"""
# INSERT INTO Uzsakymai (
#   customer, order_Nr, shipping_day, project,
#   code, ver, description, description_LT,
#   qty, measure, discount, price_Eur, shipping_adress
# )
# VALUES (
#   '{row["customer"]}', '{row["order_Nr"]}', '{row["shipping_day"]}', '{row["project"]}',
#   '{row["code"]}', '{row["ver"]}', '{row["description"]}', '{row["description_LT"]}',
#   '{row["qty"]}', '{row["measure"]}', '{row["discount"]}', '{row["price_Eur"]}',
#   '{row["shipping_adress"]}'
# )
# """

# for row in data_for_orders_database:
#    execute_query(database_name=MY_DATABASE, query=input_data_orders)




#eiluciu_sarasas_pagal_klienta = {
#    "dotekas": [
#        {"2021-05-01": ["eilute_1", "eilute_2"]},
#         {"2021-06-01": ["eilute_1", "eilute_2"]} 
#    ],
#    "uab_elnias": [
#        {"2021-05-01": ["eilute_1", "eilute_2"]},
#         {"2021-06-01": ["eilute_1", "eilute_2"]} 
#    ],
#}
#reikia_israsyti_sitom_imonem = list(eiluciu_sarasas_pagal_klienta.keys())
#for klientas in reikia_israsyti_sitom_imonem:
#	print(klientas, eiluciu_sarasas_pagal_klienta[klientas])
#	for eilutes in eiluciu_sarasas_pagal_klienta[klientas]:
#		print(eilutes.keys())
#	break

