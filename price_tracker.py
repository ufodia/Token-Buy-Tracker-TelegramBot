########### IMPORTING MODULES ###########
from os import environ, name
from pathlib import Path
from dotenv import load_dotenv
import logging
from telethon.sync import TelegramClient,Button
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time

######### INFORMATION OF PROJECT ##########
__author__ = "Emrecan Ayas"
__version__ = "0.1Alpha"
###########################################


###### SET LOGGERR ######
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
LOGGER = logging.getLogger(__name__)
########################

###### CONFIGS #####
a = '\\' if name == "nt" else '/'
PARENT_DIR = str(Path(__file__).parent)
load_dotenv(f'config.env')
BOT_TOKEN = environ.get('BOT_TOKEN')
API_KEY = environ.get('API_KEY')
API_HASH = environ.get('API_HASH')
CHROME_DRIVER_PATH = environ.get('CHROME_DRIVER')
########################

bot = TelegramClient('NasadogeBot',API_KEY,API_HASH).start(bot_token=BOT_TOKEN)


def start():
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36")
    options.add_argument('--start-maximized')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH,options=options)
    wait = WebDriverWait(driver, 10)
    driver.set_window_size(1920, 1080)
    driver.get('https://poocoin.app/tokens/0x079dd74cc214ac5f892f6a7271ef0722f6d0c2e6')
    time.sleep(4)
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)
    old_sold = ""
    while True:
        first_line = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div[2]/div/div[3]/div[1]/div/div[2]/div/div[1]')
        a = first_line.find_elements_by_tag_name('div')
        types = a[0].text.replace('\n','')
        amount = a[1].text.split('\n')[0]
        price = a[2].text.split('\n')[0]
        token_price = a[3].text.split('\n')[0]
        times = a[4].text.replace('\n','')
        tx = a[5].text.split('\n')[0]
        tx_url = a[5].find_element_by_tag_name('a').get_attribute('href')
        if types == 'Buy':
            emoji = "🟢"
        else:
            emoji = "🔴"
        if old_sold == tx:
            continue
        old_sold = tx
        text = (
            f"**New {types} Transaction!** {emoji}\n"
            f"**Time**: `{times}`\n"
            f"**Amount:** `{amount}`\n"
            f"**Price:** `{price}`\n"
            f"**Sold By** `{token_price}`\n"
        )
        keyboard = [
        [  
            Button.url(text='Txn Hash',url=tx_url)
        ]
        ]

        chat = bot.get_entity("https://t.me/nasadoge_buy_sell")
        bot.send_message(chat, message=text,buttons=keyboard)
        
if __name__ == "__main__":
    start()
    
