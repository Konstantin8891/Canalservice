import os
import requests
import time
import xml.etree.ElementTree as ET

import gspread
import httplib2

from datetime import date as dt, datetime

from django.core.management.base import BaseCommand
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from order.models import Order


class Command(BaseCommand):
    def __init__(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'token.json', [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive',
            ]
        )
        httpAuth = credentials.authorize(httplib2.Http(timeout=10))
        self.drive_service = build('drive', 'v3', http=httpAuth)
        response_token = (
            self.drive_service.changes().getStartPageToken().execute()
        )
        self.start_page_token = response_token.get('startPageToken')
        self.spreadsheet_id = os.getenv('SPREADSHEET')

    def check_changes(self):
        flag_changes = False
        self.page_token = self.start_page_token
        try:
            while self.page_token is not None:
                response = self.drive_service.changes().list(
                    pageToken=self.page_token,
                    spaces='drive',
                ).execute()

                for change in response.get('changes'):
                    file_id = change.get("fileId")
                    if file_id == self.spreadsheet_id:
                        flag_changes = True
                if 'newStartPageToken' in response:
                    self.start_page_token = response.get('newStartPageToken')
                self.page_token = response.get('nextPageToken')

        except Exception as e:
            print(f'''
                GSheets error: unable to fetch {self.spreadsheet_id}
                table with Google Sheets API: {e}
            ''')
        finally:
            return self.start_page_token, flag_changes

    def handle(self, *args, **options):
        flag_changes = True
        today = dt.today()
        flag_day = False
        while True:
            temp_today = dt.today()
            temp_today_str = str(temp_today)
            temp_today_str = temp_today_str.split('-')
            temp_today_str = temp_today_str[::-1]
            try:
                exchange = requests.get(f'''
                    https://www.cbr.ru/scripts/XML_daily.asp?date_req=
                    {temp_today_str[0]}/{temp_today_str[1]}/{temp_today_str[2]}
                ''')
                tree = ET.ElementTree(ET.fromstring(exchange.text))
                root = tree.getroot()
                temp_today = root.attrib['Date']
                temp_today = datetime.strptime(temp_today, "%d.%m.%Y").date()
                if temp_today != today:
                    today = temp_today
                    flag_day = True
            except Exception as e:
                print(f'error {e}, problems with cbr site')
            if flag_day and not flag_changes:
                for child in root:
                    if child.attrib['ID'] == 'R01235':
                        for sub_child in child:
                            if sub_child.tag == 'Value':
                                dollar = sub_child.text.replace(',', '.')
                                dollar = float(dollar)
                orders = Order.objects.all()
                for order in orders:
                    rub = order.price * dollar
                    order.rub_price = float('{:.2f}'.format(rub))
                    order.save()
                flag_day = False

            if flag_changes:
                gc = gspread.service_account(filename='token.json')
                sh = gc.open('Canalservice')
                data_list = sh.sheet1.get_all_values()
                today_str = str(today)
                today_str = today_str.split('-')
                today_str = today_str[::-1]
                exchange = requests.get(f'''
                    https://www.cbr.ru/scripts/XML_daily.asp?date_req=
                    {today_str[0]}/{today_str[1]}/{today_str[2]}
                ''')
                tree = ET.ElementTree(ET.fromstring(exchange.text))
                root = tree.getroot()
                for child in root:
                    if child.attrib['ID'] == 'R01235':
                        for sub_child in child:
                            if sub_child.tag == 'Value':
                                dollar = sub_child.text.replace(',', '.')
                                dollar = float(dollar)
                orders = Order.objects.all()
                if orders:
                    orders.delete()
                for i in range(1, len(data_list)):
                    date = data_list[i][3]
                    date = date.split('.')
                    date = reversed(date)
                    date = '-'.join(date)
                    rub_price = int(data_list[i][2]) * dollar
                    rub_price = float('{:.2f}'.format(rub_price))
                    try:
                        order = Order(
                            order_id=int(data_list[i][1]),
                            price=int(data_list[i][2]),
                            rub_price=rub_price,
                            date=date
                        )
                        order.save()
                    except Exception:
                        raise Exception(f'error in line {i + 1}')
                flag_changes = False
            self.start_page_token, flag_changes = self.check_changes()
            time.sleep(30)
