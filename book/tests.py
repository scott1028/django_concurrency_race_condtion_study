# coding:utf-8
# 如果要在 TestCase 使用 threading
# 參考：https://groups.google.com/forum/#!topic/django-users/3Yz-h1QXNqo

import threading

from django.test import TestCase, TransactionTestCase

from book.models import book


# Create your tests here.
class AnimalTestCase(TransactionTestCase):
    def setUp(self):
        row = book.objects.create(label='first_row')
        self.transaction_uri = '/book/transaction_test/'
        self.non_transaction_uri = '/book/non_transaction_test/'

    def get_uri(self, url):
        resp = self.client.get(url)

    # 似乎另一個 request 會跳出 Http 500 錯誤, 所以在 View 裡面坐了 try-catch
    def test_multi_thread_ger_book_by_transaction(self):
        th = []
        for i in range(0, 50):
            th.append(
                threading.Thread(
                    target=self.get_uri,
                    args=(self.transaction_uri,))
            )
        for i in th:i.start()
        for i in th:i.join()
        self.assertEqual(book.objects.first().version, 50)

    def test_multi_thread_ger_book_by_non_transaction(self):
        th = []
        for i in range(0, 50):
            th.append(
                threading.Thread(
                    target=self.get_uri,
                    args=(self.non_transaction_uri,))
            )
        for i in th:i.start()
        for i in th:i.join()

        print 'In Concurrency Transaction Condition:'
        print 'Expect Value: ',50
        print 'Current Value: ',book.objects.first().version

        self.assertNotEqual(book.objects.first().version, 50)
