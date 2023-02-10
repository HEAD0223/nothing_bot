import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
URL_APP   = str(os.getenv("URL_APP"))

admins_id = [
    382586338,
]