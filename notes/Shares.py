import json
import os
import re
from datetime import datetime

from django.contrib.auth.models import User

import hidden_config
from notes.models import UserProfile, Note


class Shares:
    """
    Searchs and loads notes shared in telegram (bot notes_bot, @sshares_bot)
    path is configured in hidden_config.py:
    TELEGRAM_FILES = '<path_to_bot_src>/data'
    """

    FILE_LAST_CHARGED = 'last.txt'
    path = None
    user: User = None
    user_profile: UserProfile = None

    def __init__(self, user):
        self.user = user
        self.user_profile = UserProfile.objects.get(user=user)

        pattern = re.compile(r'\d{4}-\d{2}-\d{2}_url\.json')  # шаблон имени файла
        files = os.listdir(self.path)
        matching_files = [f for f in files if pattern.match(f)]
        print(matching_files)  # список файлов
        for file in matching_files:
            pass

    def process(self):
        self.path = self.__get_path()
        if self.path is None:
            return
        last_charged, last_day_notes_charged = self.__get_last_charged()
        last_charged_ymd = datetime.fromtimestamp(last_charged).strftime("%Y-%m-%d")

        matching_files = self.__get_matched_files(last_charged_ymd)
        today = datetime.now().strftime('%Y-%m-%d')
        today_notes_charged = 0
        for file in matching_files:
            full_filename = os.path.join(self.path, file)
            with open(full_filename, 'r') as f:
                shared_notes = json.load(f)
            counter_notes = 0
            for shared_note in shared_notes:
                if file[0: 10] == last_charged_ymd and counter_notes <= last_day_notes_charged:
                    continue
                shared_note['user'] = self.user
                shared_note['private'] = True
                Note.objects.create(**shared_note).save()
                today_notes_charged += 1 if file[0: 10] == today else 0

        self.__set_last_charged(today_notes_charged)

    def __get_matched_files(self, last_charged_ymd):
        pattern = re.compile(r'\d{4}-\d{2}-\d{2}_url\.json')
        files = os.listdir(self.path)
        matching_files = list(filter(lambda f: pattern.match(f) and f > last_charged_ymd, files))
        return matching_files

    def __get_path(self):
        """
        get path with shared items in files YYYY-MM-DD_url.json format
        Path includes telegram user name.
        Example: /Users/user/bot/data/<Telegram_User>
        :return: path or None if path is not exist or not configured
        """
        if self.user_profile is None or self.user_profile.telegram is None or self.user_profile.telegram == '':
            return
        if not os.path.exists(os.path.join(hidden_config.TELEGRAM_FILES, self.user_profile.telegram)):
            return
        path = os.path.join(hidden_config.TELEGRAM_FILES, self.user_profile.telegram)
        return path

    def __get_last_charged(self) -> tuple:
        if self.path is None:
            return 0, 0
        full_filename = os.path.join(self.path, self.FILE_LAST_CHARGED)
        if not os.path.exists(full_filename):
            return 0, 0
        unix_date = '0'
        with open(full_filename, 'r') as f:
            data = f.read()
            unix_date, today_notes_charged = data.split(',')
        return int(unix_date), int(today_notes_charged)

    def __set_last_charged(self, today_notes_charged):
        if self.path is None:
            return 0
        full_filename = os.path.join(self.path, self.FILE_LAST_CHARGED)
        now = datetime.now().timestamp()
        with open(full_filename, 'w') as f:
            unix_date = f.write(f'{str(int(now))},{str(today_notes_charged)}')
        return int(unix_date)
