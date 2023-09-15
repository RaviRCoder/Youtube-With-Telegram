from decouple import config
from bot import Bot

Bot(config("APP_ID"),config("APP_HASH"),config("BOT_TOKEN"),config("ADMIN_CHANNAL_USERNAME")).start()
