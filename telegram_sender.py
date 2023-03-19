
from telethon.sync import TelegramClient #using Telethon 1.27.0
from telethon.sessions import StringSession
import config

class TelegramSender:
    def __init__(self, bot_token, api_id, api_hash, phone):
        API_SESSION = config.api_session

        self.client = TelegramClient(StringSession(API_SESSION), api_id, api_hash)
        
        self.client.connect()

        if not self.client.is_user_authorized():
            self.client.send_code_request(phone)
     
            # signing in the client
            self.client.sign_in(phone, input('Enter the code: '))
    
    def send_message(self, message):
        self.client.send_message(config.recipient, message)
        print(f"Message '{message}' was sent to '{config.recipient}' successfully!")

    def disconnect(self):
        self.client.disconnect()