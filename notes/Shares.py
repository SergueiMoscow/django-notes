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
    last_charged_ymd = None
    last_day_notes_charged = None
    today = None
    today_notes_charged = 0

    def __init__(self, user):
        self.user = user
        self.user_profile = UserProfile.objects.get(user=user)
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.path = self.__get_path()

    def process(self):
        if self.path is None:
            return
        last_charged, self.last_day_notes_charged = self.__get_last_charged()
        self.last_charged_ymd = datetime.fromtimestamp(last_charged).strftime("%Y-%m-%d")

        matching_files = self.__get_matched_files()
        for file in matching_files:
            last_day_notes_charged = self.last_day_notes_charged if self.last_charged_ymd == file[0: 10] else 0
            last_day_notes_charged = self.__process_file(str(file), last_day_notes_charged)
            if file[0: 10] == self.today:
                self.today_notes_charged = last_day_notes_charged

        self.__set_last_charged()

    def __process_file(self, filename: str, notes_charged: int) -> int:
        """
        :param filename: only filename without path. Path is taken from self.path
        :param notes_charged: how many notes to pass.
        :return: notes_charged including previous (received with parameter)
        """
        full_filename = os.path.join(self.path, filename)
        with open(full_filename, 'r') as f:
            shared_notes = json.load(f)
        counter_notes = 0
        local_notes_charged: int = notes_charged
        for shared_note in shared_notes:
            counter_notes += 1
            if counter_notes <= local_notes_charged:
                continue
            shared_note['user'] = self.user
            shared_note['private'] = True
            Note.objects.create(**shared_note).save()
            local_notes_charged += 1
        if filename[0: 10] == self.today:
            self.today_notes_charged = local_notes_charged

        return local_notes_charged

    def __get_matched_files(self):
        pattern = re.compile(r'\d{4}-\d{2}-\d{2}_url\.json')
        files = os.listdir(self.path)
        matching_files = list(filter(lambda f: pattern.match(f) and f > self.last_charged_ymd, files))
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
        """
        Reads last.txt with info (<timestamp>, <notes_count>)
        :return: tuple(<timestamp>, <notes_count>)
        """
        if self.path is None:
            return 0, 0
        full_filename = os.path.join(self.path, self.FILE_LAST_CHARGED)
        if not os.path.exists(full_filename):
            return 0, 0
        unix_date = '0'
        with open(full_filename, 'r') as f:
            data = f.read()
            unix_date, notes_charged = data.split(',')
        return int(unix_date), int(notes_charged)

    def __set_last_charged(self):
        """
        Saves number of notes shared and saved today
        :return: number of bytes written
        """
        if self.path is None:
            return 0
        full_filename = os.path.join(self.path, self.FILE_LAST_CHARGED)
        now = datetime.now().timestamp()
        with open(full_filename, 'w') as f:
            bytes_written = f.write(f'{str(int(now))},{str(self.today_notes_charged)}')
        return int(bytes_written)

    # names of theese classes is requirements of unit tests
    def _TestShared__set_last_charged(self):
        return self.__set_last_charged()

    def _TestShared__get_last_charged(self):
        return self.__get_last_charged()

    def _TestShared__process_file(self, filename, notes_charged):
        return self.__process_file(filename, notes_charged)
