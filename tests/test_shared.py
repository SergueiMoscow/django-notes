import os
import shutil
from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from hidden_config import TELEGRAM_FILES
from notes.models import Note, UserProfile
from notes.Shares import Shares


class TestShared(TestCase):

    user = None
    shares = None
    username = 'unittest'
    password = 'test123456'
    userprofile = None

    def setUp(self):
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.userprofile = UserProfile.objects.create(user=self.user, telegram=self.username)
        self.client.login(username=self.username, password=self.password)
        self.shares = Shares(self.user)
        user_notes_dir = os.path.join(TELEGRAM_FILES, self.username)
        if not os.path.exists(user_notes_dir):
            os.mkdir(user_notes_dir, mode=777)

    # def test_set_last_charged(self):
    #     num_bytes = self.shares.__set_last_charged()
    #     self.assertGreater(num_bytes, 0)

    # def test_get_last_charged(self):
    #     today, num = self.shares.__get_last_charged()
    #     self.assertEqual(num, 0)  # add assertion here

    @staticmethod
    def notes_records_count():
        return Note.objects.count()

    def test_process_file(self):
        """
        Тестируем 2 новых объекта с телеграма
        :return:
        """
        now = datetime.now()
        filename_test = f'{now.strftime("%Y-%m-%d")}_url.json'
        file_name_full_path = os.path.join(self.shares.path, filename_test)
        source = os.path.join(os.path.dirname(__file__), 'data', 'test_2.json')
        shutil.copy2(source, file_name_full_path)
        self.assertEqual(0, self.notes_records_count())
        records_added = self.shares.__process_file(filename_test, 0)
        self.assertEqual(2, records_added)

        self.shares.__set_last_charged()
        self.assertEqual(2, self.notes_records_count())

        today, num = self.shares.__get_last_charged()
        self.assertEqual(num, 2)
        # Добавляем ещё объект с телеграма
        source = os.path.join(os.path.dirname(__file__), 'data', 'test_3.json')
        shutil.copy2(source, file_name_full_path)
        self.shares.__process_file(filename_test, num)
        self.shares.__set_last_charged()
        self.assertEqual(3, self.notes_records_count())
        today, num = self.shares.__get_last_charged()
        self.assertEqual(num, 3)  # add assertion here

    def tearDown(self):
        pass
        # self.userprofile.delete()
        # self.user.delete()
