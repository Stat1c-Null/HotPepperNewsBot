import os
import telebot
import yfinance as yf

API_KEY = os.environ['API']
bot = telebot.TeleBot(API_KEY)

#Start convo
@bot.message_handler(commands=["start"])
def start(message):
  bot.reply_to(message, "Here are my commands")
  bot.send_message(message.chat.id, "/stocks - get latest stock prices (gme, amc, nok, tsla)")

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

#Keep checking for new messages
bot.polling()