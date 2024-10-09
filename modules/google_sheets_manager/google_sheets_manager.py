import gspread
from google.oauth2.service_account import Credentials


class GSheets_Manager:
    def __init__(self, scopes: str, credentials: str, sheet_id: str, table_range: str):
        self.credentials = Credentials.from_service_account_file(credentials, scopes=scopes)
        self.client = gspread.authorize(self.credentials)
        self.sheet = self.client.open_by_key(sheet_id).sheet1
        self.table_range = table_range
        self.row_template = {}
        self.sheet_template = [["Отопление", "Залог", "Комиссия", "Предоплата", "Продолжительность аренды", "Условия проживания", "ID предложения"]]
        self.load_sheet_template()

    def load_sheet_template(self):
        if self.sheet.row_count == 0:
            self.sheet.append_row(self.sheet_template, table_range=self.table_range)

    def upload_offers_info_to_gsheet(self, offers_info: list):
        self.sheet.append_rows(offers_info, table_range=self.table_range)

    def empty_gsheet(self):
        self.sheet.clear()
        self.load_sheet_template()
