import requests #For web acc.
from bs4 import BeautifulSoup # Structure data 
import pandas as pd # CSV 
import datetime 
import smtplib #Email
import schedule # Runs automatically
import time # for delay
import config # sensitive data
import os # checks file existence
import re # search extract

# Scrape product data

def get_price():
    #used mimics headers to prevent blocking by website
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9" #used mimics headers to prevent blocking by website
    }

    try:
        # sends HTTP get request to product URL
        response = requests.get(config.URL, headers=headers)
        response.raise_for_status() # throws error if fails

        #Convert raw html into structure data
        soup = BeautifulSoup(response.text, "html.parser")

        # Product title
        # The condition checks whether the HTML element exists. 
        #  If BeautifulSoup successfully finds the element, it evaluates to true; 
        # otherwise, it falls back to a default value.
        title_tag = soup.find("span", {"id": "productTitle"})
        if title_tag:
            title = title_tag.get_text().strip()
        else:
            title = "Unknown Product"

        # Price extraction (robust)
        price_tag = soup.find("span", {"class": "a-price-whole"})
        # "span" is an element to style part of text
        if not price_tag:
            print("Price not found on page")
            return title, None

        # Simply extract raw string from price
        price_text = price_tag.get_text()

        # CLEAN PRICE USING REGEX
        price = re.sub(r"[^\d]", "", price_text)

        # after removing everything except number
        if not price: #if price is empty 
            print("Price parsing failed")
            0
            return title, None

        price = int(price)

        return title, price
    #catches runtime error
    except Exception as e:
        print("Error fetching product:", e)
        return None, None

        
# Save data to CSV
def save_data(title, price):
    file_exists = os.path.isfile("data.csv")

#checks if CSV file already exists & Create structured record
    data = {
        "Product": title,
        "Price": price,
        "Date": datetime.datetime.now()
    }
# converts dictionary into table 
    d = pd.DataFrame([data])

# Appends new row if file exists
    if file_exists:
        d.to_csv("data.csv", mode="a", header=False, index=False)
    else:
        d.to_csv("data.csv", index=False)


# Send email alert(smtplib)
def send_email(title, price):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(config.EMAIL, config.PASSWORD)

        subject = "Price Drop Alert!"
        body = f"{title}\nCurrent Price: ₹{price}\nLink: {config.URL}"

        message = f"Subject:{subject}\n\n{body}"

        server.sendmail(config.EMAIL, config.TO_EMAIL, message)
        server.quit()

        print("Email sent!")

    except Exception as e:
        print("Email error:", e)



# Main logic
def check_price():
    title, price = get_price()

    if title and price:# Ensures valid data
        print(f"{datetime.datetime.now()} | {title} → ₹{price}")
        # Stores data
        save_data(title, price)
        #  Checks price drop condition
        if price < config.TARGET_PRICE:
            print("Price dropped! Sending email...")
            send_email(title, price)

    # small delay (avoid blocking)
    time.sleep(2)


# Scheduler
schedule.every(6).hours.do(check_price)

# Run immediately once
check_price()

# Loop
while True:
    schedule.run_pending()
    time.sleep(60)

# in conclution:
'''In conclusion, this project automates the process of tracking product prices,
 which helps users save time and make better purchasing decisions.'''