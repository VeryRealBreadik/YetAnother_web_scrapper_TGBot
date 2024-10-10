from modules.google_sheets_manager.google_sheets_manager import GSheets_Manager
from modules.tg_bot.bot import Bot
from modules.web_scrapper.cian_web_scrapper import WebScrapper
from modules import load_gsheets_manager, load_web_scrapper, start_bot

import asyncio
from dotenv import load_dotenv
import os


load_dotenv("essentials/.env")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SCOPES = [os.getenv("SCOPES")]
CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE")
GSHEET_ID = os.getenv("GSHEET_ID")
TABLE_RANGE = os.getenv("TABLE_RANGE")
PERSISTENCE_FILE_PATH = os.getenv("PERSISTENCE_FILE_PATH")

load_gsheets_manager(SCOPES, CREDENTIALS_FILE, GSHEET_ID, TABLE_RANGE)
load_web_scrapper()


async def main():
    await start_bot(BOT_TOKEN, PERSISTENCE_FILE_PATH)

    stop_event = asyncio.Event()
    await stop_event.wait()

if __name__ == "__main__":
    asyncio.run(main())
