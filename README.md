# Finance Planner

## Overview
Finance Planner is a web application built with Flask and Bootstrap to help users manage their finances. It includes features such as:
- User authentication
- Expense, Income tracking
- Savings goals
- Data visualization
- Community forum

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
## Features
- **User Authentication**: Login, register, and logout functionality.
- **Expense Tracking**: Upload spending data and budget estimates.
- **Savings Goals**: Set and track your savings goals.
- **Data Visualization**: View financial data through responsive charts.
- **Community Forum**: Share advice and connect with others.

## Teams

| UWA ID    | Name        | Github User Name   |
|-----------|-------------|--------------------|
| 23320288  | Zeyu Wang   | zeyu-wang-123      |
| 24595816  | Karl Hoang  | Karl-Sue           |
| 24331475  | Bomin Liao  | Maxwell2048        |
| 23495103  | David Pan   | Dave-114-P         |
