import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "VIE2GOBNICJI9LIC"
NEWS_API_KEY = "7e58e64a472a416da431127b93f56eed"
TWILIO_SID = "ACefb6d7b3f5fb3fbd3dd3b82f4537deb8"
TWILIO_AUTH_TOKEN = "41e9bcb799fdb33388d2a1955523858b"

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
data = stock_response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

#Getting yesterday's closing stock price.
yesterday_price = float(data_list[0]["4. close"])

#Getting day before yesterday's closing stock price.
day_before_yesterday_price = float(data_list[1]["4. close"])

#Finding the positive difference between the tow-days prices
difference = yesterday_price-day_before_yesterday_price
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

#Finding the percentage difference in price between closing price yesterday and closing price the day before yesterday
percentage = round((difference / yesterday_price) * 100)

#If percentage is greater than 5 then get the first 3 news pieces for the COMPANY_NAME.
if abs(percentage) > 5:
    # Use: https://newsapi.org/
    # Using the News API to get articles related to the COMPANY_NAME.
    news_parameter = {
        "qInTitle": STOCK_NAME,
        "apiKey": NEWS_API_KEY
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameter)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    # Using Python slice operator to create a list that contains the first 3 articles.
    first_three = news_data[:3]
    # Formatting the message with symbols and stock name.
    formatted_articles = [f"{STOCK_NAME}: {up_down}{abs(percentage)}%\nHeadline : {article['title']}."
                          f" \nBrief: {article['description']}"for article in first_three]
    print(formatted_articles)
    #Using twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for articles in formatted_articles:
        message = client.messages.create(
                     body=articles,
                     from_='+19096554341',
                     to='+917033543642'
                 )


# Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file
by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file
by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
coronavirus market crash.
"""
