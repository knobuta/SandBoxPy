import requests
import datetime as dt
import os
import smtplib

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# -------------------- STEP 1: STOCK PRICE -------------------- #
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = os.environ.get('AVT_API_KEY')

# Get the daily stock price for the last ~5 months
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY # in ENV
}
stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_response.raise_for_status() # Print status if error out
data = stock_response.json()

# Yesterday's data in YYYY-MM-DD format
today = dt.date.today()
yesterday = (today - dt.timedelta(days=1)).strftime("%Y-%m-%d")

# Find the difference between open and close stock price of yesterday.
open_price = float(data["Time Series (Daily)"][yesterday]["1. open"]) # End price of the day before yesterday
close_price = float(data["Time Series (Daily)"][yesterday]["4. close"]) # End price of yesterday
perc_diff = round((close_price - open_price) / open_price * 100, 2) # diff of 2 data points in %
print(perc_diff)

# Calc 5% of the stock price of the day before (yesterday's beginning price) and flag if yesterday's end price is more than 5% different.
msg_head = f"{STOCK}: "
if perc_diff > 0:
    msg_head += f"🔺{perc_diff}%"
    if perc_diff >= 5.0:
        print(f"{msg_head}: Gain is more than 5%. Email.")
    else:
        print(f"{msg_head}: Gain is less than 5%. Not worth to email.")
elif perc_diff < 0:
    msg_head += f"🔻{perc_diff}%"
    if perc_diff <= 5.0:
        print(f"{msg_head}: Loss is more than 5%. Email.")
    else:
        print(f"{msg_head}: Loss is less than 5%. Not worth to email.")
else:
    msg_head += f"🔺🔻 0%"
    print(f"{msg_head}: Rare case. No change at all. Not worth to email.")


# -------------------- STEP 2: NEWS -------------------- #
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

# Get today's news of the company.
today = dt.datetime.today()
news_params = {
    "q": COMPANY_NAME,
    "from": today.strftime("%Y-%m-%d"),
    "sortBy": "popularity",
    "apikey": NEWS_API_KEY
}
news_response = requests.get(NEWS_ENDPOINT, params=news_params)
news_response.raise_for_status()
news_data = news_response.json()
#top3_news = news_data["articles"][:3] # Using slice

# Using for loop to create the body part of the email
msg_str = "" # Body of the email
for i in range(3): # Only the first 3.
    print(news_data["articles"][i]["title"])
    headline = news_data["articles"][i]["title"]
    brief = news_data["articles"][i]["description"]
    msg_str += f"Headline: {headline}\nBrief: {brief}\n"

# # Using slice and list comprehension to create the body part of the email.
# top3_news = news_data["articles"][:3] # Using slice
# formatted_articles = [f"Headline: {top3_news['title']}. \nBrief: {top3_news['description']}" for news_data["article"] in top3_news]

# -------------------- STEP 3: EMAIL not SMS -------------------- #
## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.

# #Optional: Format the SMS message like this:
# """
# TSLA: 🔺2%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
# or
# "TSLA: 🔻5%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
# """

msg_str_utf8 = msg_str.encode("utf-8") # Reformat to UTF-8 otherwise it does not work for email.

# Replace this dummy info. Or set ENV.
MY_EMAIL = "myemail@gmail.com"
MY_PASSWORD = "mypassword"

# Deos work, but it does not print out as the required format above.
with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    smtp.starttls()
    smtp.login(MY_EMAIL, MY_PASSWORD)
    smtp.sendmail(
        from_addr=MY_EMAIL,
        to_addrs=MY_EMAIL,
        msg=f"Subject: {STOCK}\n\n{msg_str_utf8}")