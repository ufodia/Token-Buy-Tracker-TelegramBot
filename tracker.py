########### IMPORTING MODULES ##########
from web3 import Web3
from unmarshal_api import UnmarshalApi
from os import environ, name
from pathlib import Path
from dotenv import load_dotenv
import logging
from datetime import datetime
from telethon.sync import TelegramClient, Button
import time


######### INFORMATION OF PROJECT ##########
__author__ = "Squirrel"
__version__ = "0.1Alpha"
###########################################


###### SET LOGGERR ######
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
LOGGER = logging.getLogger(__name__)
########################

###### CONFIGS #####
load_dotenv(f'config.env')
BOT_TOKEN = environ.get('BOT_TOKEN')
CHANNEL = environ.get("CHANNEL")
CONTRACT = environ.get("CONTRACT")
PANCAKESWAP_ADDRESS = environ.get("PANCAKESWAP_ADDRESS")
CHAIN = environ.get("CHAIN")
UNMARSHAL_API_KEY = environ.get("UNMARSHAL_API_KEY")
API_KEY = environ.get('API_KEY')
API_HASH = environ.get('API_HASH')
########################

BOT = TelegramClient(CONTRACT,API_KEY,API_HASH).start(bot_token=BOT_TOKEN)
API = UnmarshalApi(PANCAKESWAP_ADDRESS, CONTRACT, CHAIN, UNMARSHAL_API_KEY)

def timestampToHumanReadble(timestamp):
    date_time = datetime.fromtimestamp(timestamp)
    return date_time.strftime("%H:%M:%S %d/%m/%Y")


def sum_multi_sent(sent):
    token_amount = 0
    prices = 0.0
    if len(sent) > 1:
        for i in sent:
            token_amount += int(i["value"])
            prices = prices + i['quote']
        return token_amount, prices
    else:
        return None


def getAmounts(transaction, type):
    if type == "Sell":
        token_name = transaction.received[0]['name']
        token_amount = format(round(Web3.fromWei(int(transaction.received[0]['value']), "gwei"), 2), ",")
        wbnb_amount = round(Web3.fromWei(int(transaction.sent[-1]['value']), "ether"), 5)
        usd_amount = format(round(transaction.received[0]['quote'], 2),",")
        token_price = transaction.received[0]['quoteRate']
        return token_amount, token_name, wbnb_amount, usd_amount, token_price
    else:
        summed_sent = sum_multi_sent(transaction.sent)
        if summed_sent:
            token_amount = format(round(Web3.fromWei(int(summed_sent[0]), "gwei"), 2), ",")
            usd_amount = format(round(summed_sent[1], 2), ",")
        else:
            token_amount = format(round(Web3.fromWei(int(transaction.sent[0]['value']), "gwei"), 2), ",")
            usd_amount = format(round(transaction.sent[0]['quote'], 2), ",")
        
        wbnb_amount = round(Web3.fromWei(int(transaction.received[0]['value']), "ether"), 5)
        token_name = transaction.sent[0]['name']
        token_price = round(float(transaction.sent[0]['quoteRate']), 5)
        return token_amount, token_name, wbnb_amount, usd_amount, token_price

def getTransactionType(transaction):
    if transaction.sent[0]['name'] == "Wrapped BNB":
        return "🔴", "Sell"
    else:
        return "🟢", "Buy" 


def tracker():
    last_trans_id = ""
    while True:
        transaction = API.getTransactions()
        if transaction:
            if transaction.id != last_trans_id:
                _, types = getTransactionType(transaction)
                a,b,c,d,f = getAmounts(transaction, getTransactionType(transaction)[1])
                if types == "Sell":
                    continue
                if round(c, 2) < 0.25:
                    continue
                last_trans_id = transaction.id
                text = "\n**New {} 🎉🎉🚀🚀**".format(types)
                text += f"\n**Date Time:** `{timestampToHumanReadble(transaction.date)}`"
                text += "\n**Amount:** `{} {}` \n**Price:** `{} BNB (${})`\n**Price/Token:** `${}`".format(*getAmounts(transaction, getTransactionType(transaction)[1]))
                keyboard = [[Button.url(text='Bscscan', url=F"https://bscscan.com/tx/{transaction.id}"),Button.url(text=f"Buy On Poocoin", url=f"https://poocoin.app/tokens/{CONTRACT}")]]
                chat = BOT.get_entity(CHANNEL)
                BOT.send_message(chat, message=text,buttons=keyboard)
                time.sleep(5)
                
            else:
                time.sleep(5)
                continue


if __name__ == "__main__":
    tracker()
