# A Python-based Amazon price tracker that monitors a product's price 
# and sends an email alert when the price falls below a specified threshold. 
# This tool is perfect for snagging great deals and staying updated on price changes automatically.

# The program currently works with Amazon's website, 
# but due to frequent changes in Amazon's frontend structure, future compatibility may require adjustments.
# Users can update the target product URL and modify the scraping logic as needed to ensure continued functionality

import requests
from bs4 import BeautifulSoup
from smtplib import SMTP
from dotenv import dotenv_values

# Loading .env variables
secrets = dotenv_values(".env")

URL = "https://www.amazon.in/Ant-Esports-Elite-1100-Mid-Tower/dp/B0CRNQJBWB/ref=sr_1_5?crid=39UARD4G8RZA6&dib=eyJ2IjoiMSJ9.8UgabYWEhmvzC6O63SjaCHW5GGpdsY_XhRWnqmmVHdbltW-0fcIypGirU71kyzEBlHC-hJDZ9rmReD9y5pnZ-Q2dvbd8ZISxNTj2M_l72vdkpYEnoT5CaYrhrebBH-05O3Cx-BcqW2BJZXdrTVLj5jTV-712EzDcok4-ijo4pIYERCZs6DBvc_LH9fspyJWdLhnwlY6DWaOYLONrRjwSfsZVondyvsTTV6qqjSEagc0.ydPv4yRRo6ZGHaQQWJsS_L0_n8oAkqM5NrpYc8fW09Q&dib_tag=se&keywords=pc&qid=1736147033&sprefix=p%2Caps%2C237&sr=8-5"

# See the headers that your own browser is sending by going to this website: http://myhttpheader.com/
# for easy copy go to: https://httpbin.org/headers
# always erase the host and X-Amzn-Trace-Id before sending
header = secrets.get("HEADER")

# A minimal header would look like this:
# header = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) Chrome/84.0.4147.125 Safari/537.36",
#     "Accept-Language": "en-US,en;q=0.9"
# }

response = requests.get(url = URL, headers= header)
soup = BeautifulSoup(response.text, "html.parser")
# print(soup.prettify())

# Fetching Details of Amazon Product
try:
    product = soup.find("span" , id = "productTitle").string.strip()
    print(product)
    price = soup.find(class_="a-offscreen").getText()[1:].split(".")[0].split(",") # ignoring fraction part of the price
    price = int("".join(price))
    print(price)
except AttributeError:
    print("Not able to fetch Product details. Run Again!")
    exit()

BUY_PRICE = 2500
if price < BUY_PRICE:
    with SMTP(secrets.get("SMTP_ADDRESS"), 587) as connection:
        connection.starttls() # to secure smtp connection
        connection.login(user = secrets.get("MY_EMAIL"), password = secrets.get("PASSWORD"))
        from_address = secrets.get("MY_EMAIL")
        to_address = secrets.get("RECEIVER_EMAIL")
        message = f"Subject: Amazon Price Alert!\n\n{product} is on sale at price Rs{price}\n{URL}".encode("utf-8")
        connection.sendmail(from_addr = from_address, to_addrs = to_address, msg = message)
    print("email sent")
else:
    print(f"Price of {product} is High.")