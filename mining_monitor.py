from loguru import logger
import argparse
import os
import psutil
from telegram_service import TelegramService
import json

#command line parameters (temp until better solution)
parser = argparse.ArgumentParser(description='mining monitor settings')
parser.add_argument('--log-level', dest='log_level', type=str, default="INFO",
                    help='DEBUG, INFO, ERROR')

args= parser.parse_args()

#Initialize logger
logger.add(os.path.abspath(os.path.dirname(__file__)) + "\logs\log_{time}.log", format="{time} {level} {message}", level=args.log_level, rotation="500 MB")
logger.info("Mining monitor starting...")

#Initialize telegram service
telegram = TelegramService(logger)

#control flags
nanominer_running = False
green_list_running = False

#load config provided in config.json
config = {}
with open(os.path.abspath(os.path.dirname(__file__)) + '\config.json') as ci_json:
    config = json.load(ci_json)

# Approved programs that could be running instead of nanominer
# Green list - never alert
green_list = config["green-list"]

#do something to see if the nanominer process is running OR something from a list of approved processes?
for p in psutil.process_iter(attrs=['pid', 'name']):
    print(p.info['name'])
    #logger.info(p.info['name'])
    if p.info['name'] == "nanominer.exe":
        logger.info("Nanominer running...", (p.info['name']))
        nanominer_running = True

    if p.info['name'] in green_list:
        logger.info("Green list item: {}...", (p.info['name']))
        green_list_running = True

#If nanominer isn't running & no approved programs are either, then send an alert
if(nanominer_running == False and green_list_running == False):
    telegram.bot_sendtext("Nanominer isn't running!")


