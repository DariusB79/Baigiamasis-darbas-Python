import sqlite3

with sqlite3.connect("dotekas.db") as conn:  # context manager
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS Uzsakymai1")


# with sqlite3.connect("dotekas.db") as conn: # context manager
#  c = conn.cursor()
#  c.execute("DELETE FROM  Klientai")
# conn.commit()

# print(type(data_for_bank_database))
# print(data_for_bank_database)

# print(data.keys())
