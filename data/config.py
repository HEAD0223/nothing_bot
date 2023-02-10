import os
from dotenv import load_dotenv
from typing import Final

load_dotenv()

# class TgKeys:
#     TOKEN: Final = environ.get('TOKEN', 'define me!')

TOKEN = str(os.getenv("TOKEN"))

# webhook settings
WEBHOOK_HOST = 'https://your.domain'
WEBHOOK_PATH = '/path/to/api'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 3001


admins_id = [
    382586338,
]