import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
from email.message import EmailMessage

URL = "https://www.amazon.in/New-Apple-iPhone-Pro-256GB/dp/B08L5T2XSF/ref=sr_1_1_sspa?qid=1640711521"
EMAIL = "sender-email"
PASSWORD = "sender-password"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/96.0.4664.110 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
}

# retrieving website and turning it into content
response = requests.get(url=URL, headers=headers)
data = response.content

# scraping website for the price
soup = BeautifulSoup(data, "lxml")
price = soup.find(class_="a-offscreen").get_text()
price_without_currency = price.split("₹")[1].replace(",", "")
price_as_float = float(price_without_currency)
# print(price_as_float)

title = soup.find(id="productTitle").get_text().strip()
print(title)

BUY_PRICE = 90000.0

# sending mail
if price_as_float < BUY_PRICE:
    msg = EmailMessage()
    msg['From'] = EMAIL
    msg['To'] = EMAIL
    msg['Subject'] = "Amazon Price Alert!!"
    msg.set_content(f"Hi! {title} is now at a price of just: {price}! \n{URL}")

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(EMAIL, PASSWORD)
        connection.send_message(msg)




