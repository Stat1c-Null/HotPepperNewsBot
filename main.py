from telebot import types
import os, time, telebot
from datetime import date
from newsapi import NewsApiClient
import yfinance as yf

#Set up API
API_KEY = os.environ['API']  #GET TELEGRAM BOT API KEY
NEWS_KEY = os.environ['NEWS_API']  #GET NEWSAPI.ORG KEY

bot = telebot.TeleBot(API_KEY)
#Settings
newsapi = NewsApiClient(api_key=NEWS_KEY)
news_rate = 5
news_count = 0
news_popularity = 0
send_more = False  #Send more news
today_date = date.today()
#Daily sender
daily_news = True
hours_delay = 1
delay = hours_delay * 60 * 60


#Start convo
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Here are my commands:\n\n/about - About this bot\n\n/daily_sender - Get daily news reminders on topics that interest you TODO\n\n/stonks - get latest stock prices (gme, amc, nok, tsla)\n/news - get latest hottest news\n\n/usa_news - get latest news from greatest country in the world (USA)\n\n/russia_news - get latest news from most communistic country (Russia)\n\n/business_news - get latest business news from around the world\n\n/tech_news - get latest tech news\n\n/media_news - get latest media news\n\n/sport_news - get latest sports news\n\n/science_news - get latest science news\n\n/health_news - get latest health and medicare news")

#Set daily news sender
@bot.message_handler(commands=["daily_sender"])
def daily_news(message):
    bot.send_message(message.chat.id,
                     "Would you like to turn on daily news sender ?")
    bot.send_message(message.chat.id,
                     "How many news would you like to get at time ?")
    bot.send_message(
        message.chat.id,
        "How often would you like to receive automated messages ? Enter number of hours"
    )
    #await daily_news_send()


#Ask user a question
def answer(message):
    #Add selection keyboard
    markup = types.ReplyKeyboardMarkup(row_width=2)
    yesbtn = types.KeyboardButton('/yes')
    nobtn = types.KeyboardButton('/no')
    markup.add(yesbtn, nobtn)
    bot.send_message(message.chat.id,
                     "Choose one option:",
                     reply_markup=markup)

@bot.message_handler(commands=["yes"])
def yes(message):
    global news_count, send_more
    news_count = 0
    send_more = True
    #Remove selection keyboard
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id,
                     "Nice, give me a second to see",
                     reply_markup=markup)


@bot.message_handler(commands=["no"])
def no(message):
    global send_more
    send_more = False
    #Remove selection keyboard
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, "Unfortunate", reply_markup=markup)


#function to send news to the user
def get_news(articles: dict, type: str, message):
    global news_rate, news_popularity, news_count, send_more
    news_popularity += 1
    print("Someone is getting news today again for " + str(news_popularity) +
          " time today")
    bot.send_message(message.chat.id, "We got some HOT " + type + " news")
    news_count = 0
    for news in articles['articles']:
        news_count += 1
        bot.send_message(message.chat.id, 80 * "-")
        bot.send_message(message.chat.id, str(news['title']))
        bot.send_message(message.chat.id, str(news['description']))
        bot.send_message(message.chat.id, str(news['url']))
        #Rework date
        date = str(news['publishedAt'])
        date = date.replace('T', ' ')
        date = date.replace('Z', ' ')
        bot.send_message(message.chat.id, "Published at " + date)
        bot.send_message(message.chat.id, "By " + str(news['author']))
        #Stop loop
        if news_count >= news_rate:
            bot.send_message(message.chat.id,
                             "Would you like to see more news ?")
            answer(message)
            time.sleep(10)
            if send_more == False:
                break


#Get latest news
@bot.message_handler(commands=["news"])
def news(message):
    global newsapi, today_date
    try:
        #all_articles = newsapi.get_everything(sources='bbc-news,the-verge,the-washington-post, abc-news, usa-today, the-wall-street-journal, ign, wired-de, wired, the-washington-times, medical-news-today', from_param=today_date, language='en',sort_by='relevancy')
        all_articles = newsapi.get_top_headlines(category='general',
                                                 country='us',
                                                 language='en')
        data = newsapi.get_sources()
        #print(data)
        get_news(all_articles, "general", message)
    except:
        print("Error occured")
        bot.send_message(message.chat.id,
                         "Sorry error occured, try again later")


#Get business news
@bot.message_handler(commands=["business_news"])
def business_news(message):
    global newsapi, news_rate
    try:
        all_articles = newsapi.get_top_headlines(category='business',
                                                 country='us',
                                                 language='en')
        get_news(all_articles, "business", message)
    except:
        print("Error occured")
        bot.send_message(message.chat.id,
                         "Sorry error occured, try again later")


#Get russian news
@bot.message_handler(commands=["russia_news"])
def russian_news(message):
    global newsapi, news_rate
    try:
        all_articles = newsapi.get_top_headlines(category='general',
                                                 country='ru',
                                                 language='ru')
        get_news(all_articles, "russian", message)
    except:
        print("Error occured")
        bot.send_message(message.chat.id,
                         "Sorry error occured, try again later")


#Get american news
@bot.message_handler(commands=["usa_news"])
def usa_news(message):
    global newsapi, news_rate
    try:
        all_articles = newsapi.get_top_headlines(category='general',
                                                 country='us',
                                                 language='en')
        get_news(all_articles, "american", message)
    except:
        print("Error occured")
        bot.send_message(message.chat.id,
                         "Sorry error occured, try again later")


#Get tech news
@bot.message_handler(commands=["tech_news"])
def tech_news(message):
    global newsapi, news_rate
    try:
        all_articles = newsapi.get_top_headlines(category='technology',
                                                 language='en')
        get_news(all_articles, "tech", message)
    except:
        print("Error occured")
        bot.send_message(message.chat.id,
                         "Sorry error occured, try again later")


#Get sports news
@bot.message_handler(commands=["sport_news"])
def sport_news(message):
    global newsapi, news_rate
    try:
        all_articles = newsapi.get_top_headlines(category='sports',
                                                 language='en')
        get_news(all_articles, "sports", message)
    except:
        print("Error occured")
        bot.send_message(message.chat.id,
                         "Sorry error occured, try again later")


#Get entertainment news
@bot.message_handler(commands=["media_news"])
def media_news(message):
    global newsapi, news_rate
    try:
        all_articles = newsapi.get_top_headlines(category='entertainment',
                                                 language='en')
        get_news(all_articles, "media", message)
    except:
        print("Error occured")
        bot.send_message(message.chat.id,
                         "Sorry error occured, try again later")


#Get science news
@bot.message_handler(commands=["science_news"])
def science_news(message):
    global newsapi, news_rate
    try:
        all_articles = newsapi.get_top_headlines(category='science',
                                                 language='en')
        get_news(all_articles, "science", message)
    except:
        print("Error occured")
        bot.send_message(message.chat.id,
                         "Sorry error occured, try again later")


#Get health news
@bot.message_handler(commands=["health_news"])
def health_news(message):
    global newsapi, news_rate
    try:
        all_articles = newsapi.get_top_headlines(category='health',
                                                 language='en')
        get_news(all_articles, "health", message)
    except:
        print("Error occured")
        bot.send_message(message.chat.id,
                         "Sorry error occured, try again later")


#Get latest stocks
@bot.message_handler(commands=['stonks'])
def get_stocks(message):
    bot.send_message(message.chat.id, "Alright let me take a look")
    answer = ""
    #Choose stocks
    stocks = ['AAPL', 'MSFT', 'GOOG', 'AMZN' ,'NVDA', 'META', 'TSLA', 'XOM', 'JPM', 'WMT', 'KO', 'BAC', 'PFE', 'MCD', 'AMD', 'CSCO', 'NFLX', 'DIS', 'BA', 'INTC', 'GE', 'T', 'F', 'GME', 'AMC', 'NOK', 'AXP', 'CAT', 'CVX', 'DOW', 'GS', 'HD']
    stock_names = ["Apple", "Microsoft", "Google", "Amazon", "NVIDIA", "META", "Tesla", "Exxon Mobil Corporation", "JPMorgan Chase & Co.", "Walmart", "The Coca Cola Company", "Bank of America", "Pfizer Inc.", "McDonald's Corporation", "Advanced Micro Devices, Inc.", "Cisco", "Netflix", "The Walt Disney Company", "The Boeing Company", "Intel Corporation", "General Electric Company", "AT&T Inc.", "Ford Motor Company","GameStop", "AMC", "Nokia", "American Express Company", "Caterpillar", "Chevron", "Dow Inc.", "Goldman Sachs Group, Inc.", "Home Depot Inc."]
    stock_name = 0
    stock_data = []
    for stock in stocks:
        data = yf.download(
            tickers=stock, period='2d',
            interval='1d')  #Download data for the period of 2 days
        data = data.reset_index()  #Reset index so it will drop down to zero
        answer += f"---{stock}---\n"
        stock_data.append([stock])
        columns = ['Stocks']
        for index, row in data.iterrows():
            stock_position = len(stock_data) - 1
            price = round(row['Close'], 2)  #Round up the price
            format_date = row['Date'].strftime(
                '%m/%d')  #Format date in month/day
            answer += f"{format_date}: {price}\n"
            stock_data[stock_position].append(price)
            columns.append(format_date)
        print()

    #Adding column headers and making sure they have 10 spaces between them
    answer = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
    for row in stock_data:
        answer += stock_names[stock_name]
        answer += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
        stock_name += 1
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
        data = data.reset_index()  #Reset index so it will drop down to zero
        data["format_date"] = data["Datetime"].dt.strftime('%m/%d %I:%M %p')
        data.set_index('format_date', inplace=True)
        print(data.to_string())
        bot.send_message(message.chat.id,
                         data['Close'].to_string(header=False))
    else:
        bot.send_message(message.chat.id, 'No data?!')


#about
@bot.message_handler(commands=["about"])
def about(message):
    bot.send_message(
        message.chat.id,
        "My name is Henry and I was developed by Mikita Slabysh aka Stat1c-Null . Version v1.0.0 Last Update: 26/05/2023"
    )


#if fucker wants to edit the message
@bot.edited_message_handler()
def edited(message):
    bot.reply_to(
        message,
        'I saw it! You edited message!Dont try to mix up the court evidence!')


#Keep checking for new messages
print("Bot Is Online!")
bot.polling()
