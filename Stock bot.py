import requests
from datetime import datetime, timedelta
from twilio.rest import Client

# Twilio credentials
def send_message (index : int, icon : str, percentage_change, news_content):
    account_sid = 'your id '
    auth_token = 'your api'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
      from_='.',
      content_sid='.',
      body=f"TSLA: {icon} {percentage_change:.2f}%\n"
           f"Headline:{news_content[index][0]["title"]} ?\n"
           f"Brief:{news_content[index][1]["description"]}",
      to=''
    )



date = datetime
current_date = date.now()
date_before_two_days = str((current_date - timedelta(days=2)).date())
date_before_three_days = str((current_date - timedelta(days=3)).date())

# Company stock API Key
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY = ""

para = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK,
    "apikey": API_KEY
}

response = requests.get(url="https://www.alphavantage.co/query", params=para)
response.raise_for_status()
print(response.text)


# close price for today and yesterday
data = response.json()["Time Series (Daily)"]

close_price_today = data[date_before_two_days]["4. close"]
close_price_yesterday = data[date_before_three_days]["4. close"]


# company news API key
api_key = ""
parameter = {
    "q" : STOCK,
    "qInTitle" : COMPANY_NAME,
    "from" : date_before_three_days,
    "sortBy": "publishedAt",
    "apiKey" : api_key,
}


reply = requests.get(url="https://newsapi.org/v2/everything", params= parameter)
reply.raise_for_status()


# getting the recent articles news from starting from yesterday till today
news = reply.json()["articles"]

# create a list that has the title and description for the last recent 3 news articles
news_content = [({ "title" : news[item]["title"]}, {"description" : news[item]["description"] }) for item in range (0,3)]


# Calculating the differences between the two close prices
difference = float(close_price_today) - float(close_price_yesterday)

percentage_change = (difference / float (close_price_yesterday)) * 100
print(difference, percentage_change)

if percentage_change >  2 :
    send_message(0,"🔺", news_content=news_content, percentage_change=percentage_change)
elif percentage_change < 2 :
    abs(percentage_change)
    send_message(2,"🔻",news_content=news_content, percentage_change=percentage_change)
else :
     send_message(1,"🔻🔺",news_content=news_content, percentage_change=percentage_change)


