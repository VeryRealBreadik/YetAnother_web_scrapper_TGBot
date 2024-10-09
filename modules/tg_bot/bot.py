from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ConversationHandler, CommandHandler, MessageHandler, ContextTypes, filters, PicklePersistence, BaseHandler
from ..google_sheets_manager.google_sheets_manager import GSheets_Manager
from ..web_scrapper.cian_web_scrapper import WebScrapper
import re



class Bot:
    def __init__(self, bot_token: str, persistence_file_path: str, gheets_manager: GSheets_Manager, web_scrapper: WebScrapper):
        self.bot_token = bot_token
        self.persistence_file_path = persistence_file_path
        self.gsheets_manager = gheets_manager
        self.web_scrapper = web_scrapper
        self.gsheets_manager.load_sheet_template()

    async def run(self):
        persistence = PicklePersistence(filepath=self.persistence_file_path)
        application = ApplicationBuilder().token(self.bot_token).persistence(persistence).build()
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("parse_offers", self.parse_cian))
        application.add_handler(CommandHandler("load_offers", self.load_offers_to_gsheet))

        application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hello! I'm a bot that can help you find an apartment. Type /help to see availible commands.")

    async def parse_cian(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_data = context.user_data
        url = update.message.text
        self.web_scrapper.scrape_cian(url)
        user_data["offers_info_lst"] = self.web_scrapper.scrape_offers()
        offers_count = len(user_data["offers_info_lst"])
        await update.message.reply_text(f"Web-scrapper scraped {offers_count} offers. Type /load_offers to load to google sheet.")

    async def load_offers_to_gsheet(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_data = context.user_data
        offers_info_lst = user_data["offers_info_lst"]
        offers_to_upload = []
        for offer_info in offers_info_lst:
            offers_to_upload.append(list(offer_info.values()))

        self.gsheets_manager.upload_offers_info_to_gsheet(offers_to_upload)
