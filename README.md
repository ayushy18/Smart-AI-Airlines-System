# Smart AI Airlines System ✈️🤖

## Overview

Smart AI Airlines System is an AI-powered flight booking application developed using **Python**, **Tkinter**, and **MySQL**. The system allows users to search flights, book tickets, interact with an AI chatbot assistant, make secure payments, and generate digital e-tickets with QR code support.

---

## Features

* ✈️ Flight Search & Booking
* 🤖 AI Chatbot Assistant
* 💳 Secure Card & UPI Payment Gateway
* 📄 PDF Ticket & Receipt Generation
* 🔳 QR Code-Based Ticket Support
* 🗄️ MySQL Database Integration
* 📊 Real-Time Seat Availability Management
* 🖥️ Interactive GUI using Tkinter

---

## Technologies Used

* Python
* Tkinter
* MySQL
* PyMySQL
* FPDF
* QRCode
* Pillow (PIL)

---

## System Modules

### 1. Flight Booking Module

* View available flights
* Select flight and reserve seats
* Real-time seat updates

### 2. AI Assistant Module

* Smart chatbot for flight queries
* Search flights by destination
* Book flights through conversation

### 3. Payment Gateway

* Credit/Debit Card Payment
* UPI Payment Integration
* QR Code Payment Support

### 4. Ticket Generation

* Generate PDF e-ticket
* Download booking receipt
* QR-enabled ticket system

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/smart-ai-airlines-system.git
cd smart-ai-airlines-system
```

### Install Required Libraries

```bash
pip install pymysql fpdf qrcode pillow
```

### Setup MySQL Database

Create a database named:

```sql
rec
```

Create the airline table:

```sql
CREATE TABLE airline (
    flightNo INT PRIMARY KEY,
    amount INT,
    seats INT,
    origin VARCHAR(50),
    destination VARCHAR(50),
    flight_type VARCHAR(50)
);
```

---

## Run the Project

```bash
python AirlinesManagementSytem.py
```

---

## Future Enhancements

* AI Recommendation System
* Voice-Based Booking Assistant
* Online Flight API Integration
* Multi-language Support
* Cloud Deployment

---

## Project Screenshots
<img width="736" height="857" alt="image" src="https://github.com/user-attachments/assets/a659f91a-7518-4421-92d3-a77bc996629e" />


---

## Author

**Ayush Yadav**
B.Tech (DS + AI)
202210101150081

---

## License

This project is developed for educational and research purposes.
