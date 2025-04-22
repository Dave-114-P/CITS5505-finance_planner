Provide an overview of the app.

Finance Planner
Overview
Finance Planner is a web application built with Flask and Bootstrap to help users manage their finances. It includes features for user authentication, expense tracking, savings goals, data visualization, and a community forum.

Group Info
Developed by Group-18 for CITS5505.

Setup and Run Guide

Clone the repository:
git clone https://github.com/Dave-114-P/CITS5505-finance_planner


cd finance_planner
Set up a virtual environment:

python -m venv venv
On Linux / Mac: > source venv/bin/activate  
On Windows:     > venv\Scripts\activate


Install dependencies:
    >pip install -r requirements.txt


FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=123
DATABASE_URI=sqlite:///finance.db

Run the application:
    > python app.py


Open your browser and navigate to http://127.0.0.1:5000.
Features
User authentication (login/register/logout)
Upload spending data and budget estimates
Set and track savings goals
Visualize financial data with charts
Community forum for sharing and advice