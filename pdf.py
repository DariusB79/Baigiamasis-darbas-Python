import pdfkit
from datetime import datetime, timedelta
from helpers import (
    get_data_for_invoice,
    get_client_data_for_invoice,
    get_invoice_data_by_client_name,
    get_clients_names,
    execute_sql_query,
)
from debug_helpers import checking_type_and_data
from datetime import datetime
import base64


# Paveiksliuko sutvarkymas:
image_path = "C:/Users/HP/OneDrive/Desktop/phyton_mokymai/Paskaitos/_baigiamasis_darbas/logo_m.jpg"

with open(image_path, "rb") as img_file:
    base64_string = base64.b64encode(img_file.read()).decode("utf-8")

html_image = f'<img src="data:image/jpeg;base64,{base64_string}" alt="Company Logo" style="max-width: 100%;">'


# client_name = input(str("Iveskite klienta kuriam israsinesite saskaita"))
new_data = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

invoice_number = "DOT" + datetime.now().strftime("%Y-%m-%d")

client_data_for_invoice = get_client_data_for_invoice(
    database_name="dotekas.db", name="J. de Jager & Zonen BV"
)

print("kliento duomenys saskaitai")
checking_type_and_data(client_data_for_invoice)
print()
print()

data_for_todays_shipment = get_data_for_invoice(
    database_name="dotekas.db", date="2025/02/07", as_dict=True
)

checking_type_and_data(data=data_for_todays_shipment)

clients_names_for_invoice = get_clients_names(data_for_todays_shipment)

data_for_invoice = get_invoice_data_by_client_name(
    data=data_for_todays_shipment, name="J. de Jager & Zonen BV"
)

html_table_row = ""
for item in data_for_invoice:
    print(type(item), item)  # Debug info
    # Jei 'Price_Eur' tuščias, nustatome į 0 ir pašaliname simbolius
    price = (
        float(item["Price_Eur"].replace("€", "").replace(",", "").strip())
        if item["Price_Eur"]
        else 0
    )
    # Jei 'Discount' tuščias, nustatome į 0 ir pašaliname simbolius
    discount = (
        float(item["Discount"].replace("%", "").strip()) / 100
        if item["Discount"]
        else 0
    )
    # Apskaičiuojame kainą su nuolaida
    discounted_price = price * (1 - discount)
    # Apskaičiuojame bendrą sumą
    total_price = discounted_price * item["Qty"]

    html_table_row += f"""
    <tr>
        <td style="border-top: 1px solid #eee; padding: 5px;">{item['Description']}</td>
        <td align="center" style="border-top: 1px solid #eee; padding: 5px;">{item['Qty']}</td>
        <td align="center" style="border-top: 1px solid #eee; padding: 5px;">{price:.2f}</td>
        <td align="center" style="border-top: 1px solid #eee; padding: 5px;">{discount * 100:.0f}%</td>
        <td align="center" style="border-top: 1px solid #eee; padding: 5px;">{discounted_price:.2f}</td>
        <td align="right" style="border-top: 1px solid #eee; padding: 5px;">{total_price:.2f}</td>
    </tr>
    """


subtotal = sum(
    float(item["Price_Eur"].replace("€", "").replace(",", "").strip() or 0.0)
    * (1 - float(item["Discount"].replace("%", "").strip() or 0) / 100)
    * item["Qty"]
    for item in data_for_invoice
)



# Apskaičiuojame TAX sumą (jei nėra, nustatome 0)
tax_value = client_data_for_invoice[0][6].replace("%", "").replace(",", "").strip()
tax = (float(tax_value) if tax_value else 0.0)/10000 +1 # Jei tuščia, priskiriame 0.0


invoice_html_data = f"""

<!DOCTYPE html>
<html xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" lang="en">
    <body style="font-family:Arial Unicode MS, Helvetica , Sans-Serif;">
        <table style="table-layout: fixed; width: 100%;">
            <tbody>
                <tr>
                    <td class="">
                        <div>
                            <img src="data:image/jpeg;base64,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" alt="Company Logo" style="max-width: 100%;" alt="Company Logo" style="max-width: 75%;">
                        </div>
                    </td>
                    <td width="15%">
                        
                    </td>
                    <td>    
                        <table class="tbl-padded">
                            <caption style="text-transform: uppercase; text-align: left; font-size: 30pt;">
                                <strong>
                                    Invoice
                                </strong>
                            </caption> 
                            <tbody>
                                <tr>
                                    <td style="padding:5px;">
                                        <strong >Invoice No.</strong>
                                    </td>
                                    <td style="padding:5px;">
                                        <div>
                                           {invoice_number}
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding:5px;">
                                        <strong >Date Issued </strong>                            
                                    </td>
                                    <td style="padding:5px;">
                                        {datetime.now().strftime("%Y-%m-%d")}
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding:5px;">
                                        <strong >Due Date</strong>                            
                                    </td>
                                    <td style="padding:5px;">
                                        {new_data}
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding:5px;">
                                        <strong >Currency</strong>                                
                                    </td>
                                    <td style="padding:5px;">
                                        EUR
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
            </tbody>
        </table>
        
        <div style="padding-top: 1cm; padding-bottom: 1cm;">
            <table style="table-layout: fixed; width: 100%;">
                <tbody>
                    <tr>
                        <td>
                            <div style="padding-bottom: 10px;">
                                <strong style="text-transform: uppercase;">From</strong>
                            </div>
                            <div>
                                Dotekas, UAB <br>
                                Jovaru g.3 Kaunas LT-47192, Lietuva<br>
                                Darius Balsevicius  <br>
                                darius@dotekas.eu <br>  
                            </div>
                        </td>
                        <td width="15%">
                            
                        </td>
                        <td>
                            <div style="padding-bottom: 10px;">
                                <strong style="text-transform: uppercase;">Bill To</strong>
                            </div>
                            <div>
                                {client_data_for_invoice[0][0]} <br>
                                {client_data_for_invoice[0][3]} <br>
                                {client_data_for_invoice[0][8]} <br>
                                {client_data_for_invoice[0][4]} <br>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
       
        <div>
            <table style="table-layout: fixed; width: 100%;">
                <thead>
                    <tr>
                        <th  width="40%" align="left" style="border-top: 1px solid #eee; padding: 5px;">
                            Item / Description
                        </th>
                        <th align="center" style="border-top: 1px solid #eee; padding: 5px;">
                            Qty / Hr
                        </th>
                        <th align="center" style="border-top: 1px solid #eee; padding: 5px;">
                           Unit Price, Eur
                        </th>
                        <th align="center" style="border-top: 1px solid #eee; padding: 5px;">
                            Discount
                        </th>
                        <th align="center" style="border-top: 1px solid #eee; padding: 5px;">
                            Unit Price with Discount, EUR
                        </th>
                        <th align="right" style="border-top: 1px solid #eee; padding: 5px;">
                            Amount,Eur
                        </th>
                    </tr>
                </thead>
                <tbody>
                  {html_table_row}
                </tbody>
            </table>
        </div>
        
        <div style="border-top: 1px solid #eee;">
            <table style="table-layout: fixed; width: 100%; border-collapse: collapse;">
                <tbody>
                    <tr>
                        <td align="right" style="padding: 5px;">
                            Subtotal
                        </td>
                        <td align="right" width="20%" style="padding: 5px;">
                           {subtotal:.2f} 
                        </td>
                    </tr>
                    <tr>
                        <td align="right" style="padding: 5px;">
                            + VAT    
                        </td>
                        <td align="right" width="20%" style="padding: 5px;">
                         {client_data_for_invoice[0][6]}
                        </td>
                    </tr>
                    <tr>
                        <td align="right" style="border-top: 2px solid #eee; padding: 8px;">
                            <span style="font-size: 16pt;">
                                Total Amount        
                            </span>
                        </td>
                        <td align="right" width="20%" style="border-top: 2px solid #eee; padding: 8px;">
                            <strong style="font-size: 16pt;">
                               {(subtotal * tax):.2f}
                            </strong>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div>
            <div style="padding-top:1cm; padding-bottom: 1cm;">
                <div>
                    <strong>Note</strong>
                </div>
                <p style="font-size: 10pt; line-height: 14pt;">
                    Please pay attention to the invoice payment deadline and pay on time. 
                </p>
            </div>
        </div>
</body>

</html>
"""

options = {"no-images": ""}

config = pdfkit.configuration(
    wkhtmltopdf=r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe"
)

with open("invoice.html", "w", encoding="utf-8") as file:
    file.write(invoice_html_data)

pdfkit.from_file("invoice.html", "invoice.pdf")

print("PDF sukurtas sėkmingai!")
