import json
import requests
import os

class TelegramService:
    def __init__(self, logger):

        #load config provided in config.json
        config = {}
        with open(os.path.abspath(os.path.dirname(__file__)) + '\config.json') as ci_json:
            config = json.load(ci_json)
        
        self.logger = logger
        self.token = config["telegram"]["bot_token"]
        self.chat_id = config["telegram"]["bot_chat_id"]

    def bot_sendtext(self, message_text):
        send_text = 'https://api.telegram.org/bot' + self.token + '/sendMessage?chat_id=' + self.chat_id + '&text=' + message_text

        response = requests.get(send_text)
        return response.json()
