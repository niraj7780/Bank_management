# 🏦 Bank Management System

A simple **Bank Management System** developed using **Python** and **Microsoft SQL Server**. This project demonstrates Object-Oriented Programming (OOP), SQL Server database connectivity, modular programming, and stored procedures through a Command Line Interface (CLI).

---

# 📌 Project Overview

The Bank Management System allows three types of users:

- 👨‍💼 Manager
- 👨‍💻 Employee
- 👤 Customer

The application provides secure login, customer management, account management, transactions, and reports.

---

# 🚀 Features

## Manager Module

- Manager Login
- Add Employee
- View Employees
- Search Employee
- Update Employee
- Delete Employee

---

## Employee Module

- Add Customer
- View Customer Details
- Open Bank Account
- Deposit Money
- Withdraw Money
- Transfer Money

---

## Customer Module

- Login
- View Account Details
- Check Balance
- Deposit Money
- Withdraw Money
- View Mini Statement

---

# 🛠 Technologies Used

| Technology | Description |
|------------|-------------|
| Python 3 | Programming Language |
| SQL Server | Database |
| PyODBC | Database Connectivity |
| Object-Oriented Programming | Software Design |
| Stored Procedures | Database Operations |
| VS Code / PyCharm | IDE |

---

# 📂 Project Structure

```
Bank_management/
│
├── config.py          # Database Configuration
├── database.py        # Database Functions
├── exceptions.py      # Custom Exceptions
├── main.py            # Application Entry Point
├── menu.py            # CLI Menus
├── models.py          # OOP Models
├── utils.py           # Validation & Helper Functions
├── README.md          # Project Documentation
```

---

# 🗄 Database Tables

- Manager
- Employee
- Customer
- Account
- Transaction

---

# ⚙ Stored Procedures

- DepositMoney
- WithdrawMoney
- CustomerDetails
- MiniStatement
- EmployeeReport
- CustomerReport

---

# 📋 OOP Concepts Used

✅ Classes and Objects

✅ Constructors

✅ Inheritance

✅ Encapsulation

✅ Polymorphism

✅ Modular Programming

✅ Exception Handling

---

# 🔒 Validation

The project validates:

- Phone Number
- Username
- Password
- Minimum Balance
- Account Availability
- Insufficient Balance

---

# 📊 Database Relationships

```
Manager

Employee

Customer
    │
    ▼
Account
    │
    ▼
Transaction
```

Manager, Employee, and Customer are independent.

Only:

- Customer → Account
- Account → Transaction

are related.

---

# ▶ How to Run

### 1. Install Python

Download and install Python 3.

---

### 2. Install SQL Server

Install:

- SQL Server
- SQL Server Management Studio (SSMS)

---

### 3. Install Required Package

```bash
pip install pyodbc
```

---

### 4. Configure Database

Open **config.py** and update:

```python
server = "YOUR_SERVER_NAME"
database = "BankSystem"
driver = "{ODBC Driver 18 for SQL Server}"
```

---

### 5. Create Database

Execute the SQL script in SQL Server Management Studio.

---

### 6. Run Project

```bash
python main.py
```

---

# 📷 Sample Menu

```
==============================
BANK MANAGEMENT SYSTEM
==============================

1. Login
2. Exit
```

---

# 🔑 Default Login

### Manager

```
Username : admin
Password : admin123
```

### Employee

```
Username : rahul
Password : rahul123
```

### Customer

```
Username : amit
Password : amit123
```

*(Use the sample data you inserted into your database.)*

---

# 🎯 Learning Outcomes

This project helped in learning:

- Python Programming
- Object-Oriented Programming
- SQL Server
- Stored Procedures
- CRUD Operations
- Database Connectivity
- Exception Handling
- Modular Programming
- Banking System Workflow

---

# 🔮 Future Enhancements

- GUI using Tkinter
- Email Notifications
- OTP Authentication
- Password Encryption
- Interest Calculation
- Account Statement PDF
- Admin Dashboard
- Role-Based Access Control

---

# 👨‍💻 Developed By

**Niraj Charpe** | **shailvi mishra** | **akansha dubey**

**HCLTech TechBee Scholar**

---

# 📜 License

This project is developed for educational and internship purposes.