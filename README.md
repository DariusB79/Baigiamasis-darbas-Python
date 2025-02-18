## 📄 Invoice Generation Program
### An automated invoice generation and sending program
### that filters orders based on the delivery date,
### generates invoices, and sends them to clients via email.

### 📌 Features
✅ Filters orders by delivery date.
✅ Generates invoices for each client.
✅ Automatically sends invoices to clients via email.
✅ Saves data in a database.

### 📂 Data Sources
📌 Google Sheets API – data is retrieved from two Google Sheets:
📌Clients – stores client information (name, address, email, etc.).
📌Orders – stores order details (product list, quantities, prices, etc.).
📌Banks – stores payment details.
📌 Database – the program creates and uses an SQLite database to store data.

### 🛠️ Technologies Used
🔹 Python – the main programming language.
🔹 Google Sheets API – retrieves data from Google Sheets.
🔹 SQLite – stores data in a local database.
🔹 HTML – used to generate invoice templates.
🔹 pdfkit + wkhtmltopdf – converts HTML invoices into PDF format.




## 📄 Sąskaitų išrašymo programa
### Automatizuota sąskaitų faktūrų generavimo ir išsiuntimo programa,
### kuri pagal išvežimo datą filtruoja užsakymus,
### formuoja sąskaitas ir siunčia jas klientams el. paštu.

### 📌 Funkcionalumas
✅ Filtruoja užsakymus pagal pristatymo datą.
✅ Generuoja sąskaitas faktūras pagal klientus.
✅ Automatiškai siunčia sąskaitas klientams el. paštu.
✅ Išsaugo duomenis duomenų bazėje.

### 📂 Duomenų šaltiniai
📌 Google Sheets API – duomenys paimami iš dviejų „Google Sheets“ lentelių:
📌Klientai – informacija apie klientus (pavadinimas, adresas, el. paštas ir kt.).
📌Užsakymai – informacija apie užsakymus (prekių sąrašas, kiekiai, kainos ir kt.).
📌Bankai – informacija apie pavedimus.
📌 Duomenų bazė – programa sukuria ir naudoja SQLite duomenų bazę duomenims saugoti.

## 🛠️ Panaudotos technologijos
🔹 Python – pagrindinė programos kalba.
🔹 Google Sheets API – duomenų gavimas iš „Google Sheets“.
🔹 SQLite – duomenų saugojimas.
🔹 HTML – sąskaitų šablonų generavimas.
🔹 pdfkit + wkhtmltopdf – HTML konvertavimas į PDF.





