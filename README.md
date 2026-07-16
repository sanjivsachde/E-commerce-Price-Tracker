# E-commerce-Price-Tracker
A Python automation project that tracks product prices from e-commerce websites, stores historical price data in CSV format, and sends email notifications when the price falls below a target threshold.
Overview

This project automates product price monitoring from e-commerce websites using Python. It periodically scrapes product information, records price history in a CSV file, and sends an email alert whenever the product price drops below a predefined target.

Features
Scrapes product title and current price
Stores price history in CSV format
Sends automatic email alerts on price drops
Runs automatically every 6 hours
Uses HTTP headers to reduce request blocking
Cleans extracted prices using Regular Expressions (Regex)
Error handling for network and parsing failures
Technologies Used
Technology	Purpose
Python	Programming Language
Requests	HTTP Requests
BeautifulSoup4	HTML Parsing
Pandas	CSV Storage
Schedule	Task Scheduling
SMTP	Email Notifications
Regex	Price Cleaning
OS	File Handling
Datetime	Timestamp Generation
Project Structure
Price-Tracker/
│
├── tracker.py          # Main application
├── config.py           # Configuration variables
├── data.csv            # Price history
├── requirements.txt
├── .gitignore
└── README.md
Workflow
Start
   │
   ▼
Fetch Product Page
   │
   ▼
Extract Product Name
   │
   ▼
Extract Price
   │
   ▼
Clean Price using Regex
   │
   ▼
Save into CSV
   │
   ▼
Price < Target?
   │
 ┌─┴──────────┐
 │            │
No           Yes
 │            │
 │      Send Email Alert
 │            │
 └────Wait 6 Hours────┘
