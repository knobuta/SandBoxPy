# Udemy Day 53: Web Scraping: Capstone project
# Required Knowledge:
#   1. Selenium
#   2. BeautifulSoup
#   3. Google Form

# NOTE:
# Clicking response and creating the sheet part is not in the scope of this Udemy project.
# Can be done by creating the selenium instance of edit page?

import time

from dotenv import load_dotenv
load_dotenv()

import zillow_clone
import google_form

# -------------------- Google_form: To fill in rent infos -------------------- #
form = google_form.GoogleForm()
form.get_form() # form object

# -------------------- Zillow: Scrape necessary infos -------------------- #
zillow = zillow_clone.ZillowClone()
infos = zillow.get_rent_info() # rent information in 2D list format: [[href, address, price], [...], ... ]
for info in infos:
    href = info[0]
    address = info[1]
    price = info[2]
    # print(f"Address: {address}, Price: {price}, href: {href}")

    # Fill in to google form and submit
    form.fill_address(address)
    form.fill_price(price)
    form.fill_href(href)
    time.sleep(1)
    form.submit_form()
    time.sleep(1)

    # This page popups after submitting the form. Click Submit another icon and go back to form
    form.submit_another()
    time.sleep(1)







