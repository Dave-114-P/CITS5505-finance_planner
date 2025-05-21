# Finance Planner

## Overview
# Finance Tracker App

A simple, interactive finance tracker designed to help users manage their everyday expenses, set goals, and gain insight into their spending habits.

## 🚀 Purpose

The Finance Tracker App empowers individuals to take control of their finances by allowing them to **upload**, **visualise**, **share**, and **explore** their personal financial data in an intuitive way.

## 🧩 Key Features

- 🗺️ **Interactive Australia Map**  
  Click on any state to view fee comparisons between regions. Unauthorised users are provided with helpful links to learn more.

- 🔐 **User Account Management**  
  Register a new account, log in securely, and use features like "Remember Me" and "Forgot Password."

- 📊 **Dashboard**  
  Upload financial data, view spending charts, share insights, or reset all data.

- 💰 **Lifestyle Fee Estimator**  
  Choose between Simple, Quality, or Luxury life to view dynamic spending percentages for the month.

- 📆 **Transaction View**  
  Upload income and spending, filter by month, and access older transactions via dropdown.

- 🎯 **Goals Tracker**  
  Set savings goals and calculate how much to save monthly.

- 📈 **Visualised Insights**  
  Automatically generated visual summaries of monthly financial data.

- 🔄 **Sharing Options**  
  Share insights publicly or privately and manage shared content.

## 📌 Core Functions

- **Upload**
- **Visualise**
- **Share**
- **Introduce**

## Technologies used
- HTML
- CSS
- JavaScript
- Bootstrap
- JQuery
- Flask (with plugins described in lectures)
- AJAX/Websockets
- SQLite interfaced to via the SQLAlchemy package

### Group Info
Developed by **Group-18** for **CITS5505**.

---

## Setup and Run Guide

### Clone the Repository
```bash
git clone https://github.com/Dave-114-P/CITS5505-finance_planner
cd CITS5505-finance_planner
```

### Set Up a Virtual Environment
```bash
python -m venv venv
```
- On Linux/Mac:
    ```bash
    source venv/bin/activate
    ```
- On Windows:
    ```bash
    venv\Scripts\activate
    ```
    ```bash
    powershell -ExecutionPolicy Bypass
    /venv/Scripts/activate
    ```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure Environment Variables
Set the following environment variables:
```bash
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URI=sqlite:///finance.db
```

### Run the Application with python to avoid database errors - caused by mismatched database
```bash
python app.py
```

### Access the Application
Open your browser and navigate to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---
## Setup and run test

### Run all Unit Tests
```bash
python -m unittest run_unit_test.py 
```
### Run Selenium
Get your server handy and chromedriver downloaded on your local machine, then open new terminal to run test
```bash
python test_app 
```

#### Download chromedriver
https://developer.chrome.com/docs/chromedriver/downloads

### How to setup chromedriver
https://developer.chrome.com/docs/chromedriver/get-started

---

## Teams

| UWA ID    | Name        | Github User Name   |
|-----------|-------------|--------------------|
| 23320288  | Zeyu Wang   | zeyu-wang-123      |
| 24595816  | Karl Hoang  | Karl-Sue           |
| 24331475  | Bomin Liao  | Maxwell2048        |
| 23495103  | David Pan   | Dave-114-P         |
