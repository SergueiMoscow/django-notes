from django.test import TestCase


class TestMyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
        # print('setUpTestData вызывается один раз')

    def setUpTest(self):
        pass
        # print('setUpTestData вызывается перед каждым тестом')

    def tearDown(self) -> None:
        pass
        # print('setUpTestData вызывается после каждого теста')
