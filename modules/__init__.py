from .google_sheets_manager.google_sheets_manager import GSheets_Manager
from .tg_bot.bot import Bot
from .web_scrapper.cian_web_scrapper import WebScrapper


def load_web_scrapper():
    global web_scrapper

    web_scrapper = WebScrapper()

def load_gsheets_manager(scopes: str, credentials: str, sheet_id: str, table_range: str):
    global gsheets_manager

    gsheets_manager = GSheets_Manager(scopes=scopes, credentials=credentials, sheet_id=sheet_id, table_range=table_range)

async def start_bot(bot_token: str, persistence_file_path: str):
    global gsheets_manager
    global web_scrapper

    bot = Bot(bot_token=bot_token, persistence_file_path=persistence_file_path, gheets_manager=gsheets_manager, web_scrapper=web_scrapper)
    await bot.run()
