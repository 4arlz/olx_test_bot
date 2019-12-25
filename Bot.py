import telebot
import requests
import datetime
from telebot.types import Message

from bs4 import BeautifulSoup, element


links = []

def get_text(url):    
    #.replace(' ', '-')
    link = url.replace(' ', '-')+ '/'
    print(link)
    with open("BotLog.txt", "a") as file:
        file.write(str(datetime.datetime.now()) + ' ' + link + '\n' )
    
    page = requests.get(link)
    page.encoding = 'utf-8'
    soup = BeautifulSoup(page.text, "html.parser")    
    text = soup.find_all('tr', class_='wrap')
    links.clear()
    for p in text:
        links.append(p.find('a', class_='detailsLink').get('href'))
        # replay += p.find('a', class_='detailsLink').get('href') #+ '\n' #+' ' + p.find('p', class_='price').find('strong').text + '\n' + '\n'
    return links
	
def main(sity='list', poisk=None):
    url = 'https://www.olx.ua/'   # iterate pages for parsing 
    url_p = url + sity + '/q-' + poisk
    return url_p                

City = 'list'
TOKEN = ''
#get_text(str(main(poisk=str(message)))
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['сhangeсity', 'start'])
def echo_comand(message: Message):
    city = bot.send_message(message.chat.id, 'Введите город \nnezhin \nkiev \nvinnitsa и тому подобное'  )
    bot.register_next_step_handler(city, process_city_step)
#753143738
@bot.message_handler(commands=['givemelog'])
def send_log_file(message: Message):
    if message.from_user.id == 406110401:
        doc = open('BotLog.txt', 'rb')
        bot.send_document(message.chat.id, doc  )
        doc.close()
    else:
        bot.send_message(message.chat.id, 'unknown user'  )

def process_city_step(message):
    global City 
    City = message.text
    bot.send_message(message.chat.id, 'Теперь можете искать товары'  )


@bot.message_handler(content_types=['text'])
def echo_edit(message: Message):
    try:
        mas = get_text(main(sity=City, poisk=message.text))
    except:
        mas  = 'Не найдено'
    for i in mas:
        bot.send_message(message.chat.id, i  )
    
    #bot.send_message(message.chat.id, message.entities[0].url('https://www.olx.ua/')  )
        
bot.polling(timeout=60)