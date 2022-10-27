import os, time, random
from datetime import date
import telebot
from newsapi import NewsApiClient
import yfinance as yf

#Set up API
API_KEY = os.environ['API']#GET TELEGRAM BOT API KEY
NEWS_KEY = os.environ['NEWS_API']#GET NEWSAPI.ORG KEY

bot = telebot.TeleBot(API_KEY)

#Settings
newsapi = NewsApiClient(api_key = NEWS_KEY)
news_rate = 5
news_popularity = 0 
today_date = date.today()

#Start convo
@bot.message_handler(commands=["start"])
def start(message):
  bot.reply_to(message, "Here are my commands")
  bot.send_message(message.chat.id, "/about - About this bot")
  bot.send_message(message.chat.id, "/settings - Set number of news that you want to get per request TODO")
  bot.send_message(message.chat.id, "/stocks - get latest stock prices (gme, amc, nok, tsla)")
  bot.send_message(message.chat.id, "/news - get latest hottest news")
  bot.send_message(message.chat.id, "/usa_news - get latest news from greatest country in the world (USA)")
  bot.send_message(message.chat.id, "/russia_news - get latest news from most communistic country (Russia)")
  bot.send_message(message.chat.id, "/business_news - get latest business news from around the world")
  bot.send_message(message.chat.id, "/tech_news - get latest news from USA")

#function to send news to the user
def get_news(articles: dict, type: str, message):
  global news_rate, news_popularity
  news_popularity += 1
  print("Someone is getting news today again for " + str(news_popularity) + " time today")
  bot.send_message(message.chat.id, "We got some HOT " + type + " news")
  news_count = 0
  for news in articles['articles']:
    news_count += 1
    bot.send_message(message.chat.id, 80*"-")
    bot.send_message(message.chat.id, str(news['title']))
    bot.send_message(message.chat.id, str(news['description']))
    bot.send_message(message.chat.id, str(news['url']))
    #Rework date
    date = str(news['publishedAt'])
    date = date.replace('T',' ')
    date = date.replace('Z',' ')
    bot.send_message(message.chat.id, "Published at " + date)
    bot.send_message(message.chat.id, "By " + str(news['author']))
    #Stop loop
    if news_count >= news_rate:
      break

#Get latest news
@bot.message_handler(commands=["news"])
def news(message):
  global newsapi, today_date
  try:
    all_articles = newsapi.get_everything(sources='bbc-news,the-verge,the-washington-post, abc-news, usa-today, the-wall-street-journal, ign, wired-de, wired, the-washington-times, medical-news-today', from_param=today_date, language='en',sort_by='relevancy')
    #data = newsapi.get_sources()
    #print(data)
    get_news(all_articles, "general", message)
  except:
    print("Error occured")
    bot.send_message(message.chat.id, "Sorry error occured, try again later")
    

#Get business news
@bot.message_handler(commands=["business_news"])
def business_news(message):
  global newsapi, news_rate
  try:
    all_articles = newsapi.get_top_headlines(category='business', country='us', language='en')
    get_news(all_articles, "business", message)
  except:
    print("Error occured")
    bot.send_message(message.chat.id, "Sorry error occured, try again later")
    
#Get russian news
@bot.message_handler(commands=["russia_news"])
def russian_news(message):
  global newsapi, news_rate
  try:
    all_articles = newsapi.get_top_headlines(category='general', country='ru', language='ru')
    get_news(all_articles, "russian", message)
  except:
    print("Error occured")
    bot.send_message(message.chat.id, "Sorry error occured, try again later")

#Get american news
@bot.message_handler(commands=["usa_news"])
def usa_news(message):
  global newsapi, news_rate
  try:
    all_articles = newsapi.get_top_headlines(category='general', country='us', language='en')
    get_news(all_articles, "american", message)
  except:
    print("Error occured")
    bot.send_message(message.chat.id, "Sorry error occured, try again later")

#Get tech news
@bot.message_handler(commands=["tech_news"])
def tech_news(message):
  global newsapi, news_rate
  try:
    all_articles = newsapi.get_top_headlines(category='technology', language='en')
    get_news(all_articles, "tech", message)
  except:
    print("Error occured")
    bot.send_message(message.chat.id, "Sorry error occured, try again later")
  
#Get latest stocks
@bot.message_handler(commands=['stocks'])
def get_stocks(message):
  answer = ""
  #Choose stocks
  stocks = ["gme", "amc", "nok", "tsla"]
  stock_data = []
  for stock in stocks:
    data = yf.download(tickers=stock, period='2d', interval='1d')#Download data for the period of 2 days
    data = data.reset_index()#Reset index so it will drop down to zero
    answer += f"---{stock}---\n"
    stock_data.append([stock])
    columns = ['stock']
    for index, row in data.iterrows():
      stock_position = len(stock_data) - 1
      price = round(row['Close'], 2)#Round up the price
      format_date = row['Date'].strftime('%m/%d')#Format date in month/day
      answer += f"{format_date}: {price}\n"
      stock_data[stock_position].append(price)
      columns.append(format_date)
    print()

  #Adding column headers and making sure they have 10 spaces between them
  answer = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
  for row in stock_data:
    answer += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
  answer += "\nStock Data"
  print(answer)
  bot.send_message(message.chat.id, answer)

#Request specific stock price
def stock_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "price":
    return False
  else:
    return True

@bot.message_handler(func=stock_request)
def send_price(message):
  request = message.text.split()[1]
  #Get last minute stock price
  data = yf.download(tickers=request, period='5m', interval='1m')
  if data.size > 0:
    data = data.reset_index()#Reset index so it will drop down to zero
    data["format_date"] = data["Datetime"].dt.strftime('%m/%d %I:%M %p')
    data.set_index('format_date', inplace=True)
    print(data.to_string())
    bot.send_message(message.chat.id, data['Close'].to_string(header=False))
  else:
    bot.send_message(message.chat.id, 'No data?!')

#about
@bot.message_handler(commands=["about"])
def about(message):
  bot.send_message(message.chat.id, "My name is Henry and I was developed by Mikita Slabysh aka Stat1c-Null . Version v0.0.5 Last Update: 26/10/2022")

#Keep checking for new messages
print("Bot Is Online!")
bot.polling()