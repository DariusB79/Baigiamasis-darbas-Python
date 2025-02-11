def print_data_for_database(data_for_database):
    print("Suvedimui skirtu duomenu spausdinimas")
    for data in data_for_database:
        print(data)
        print()


def print_extracted_data(extracted_data):
    if extracted_data:
        print("Pradedu spausdinti rezultatus :-) ")
        for row in extracted_data:
            print(row)
        else:
            print("Nera duomenu - tuscia lentele")
