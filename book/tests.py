# coding:utf-8
# 如果要在 TestCase 使用 threading
# 參考：https://groups.google.com/forum/#!topic/django-users/3Yz-h1QXNqo

import threading

from django.test import TestCase, TransactionTestCase

from book.models import book, person


# Create your tests here.
class ConcurrencyRequestTestCase(TransactionTestCase):
    def setUp(self):
        row = book.objects.create(label='first_row')
        row2 = person.objects.create(name='first_row')
        self.transaction_uri = '/book/transaction_test/'
        self.non_transaction_uri = '/book/non_transaction_test/'
        self.non_transaction_person_uri = '/book/transaction_only_person_test/'

    def get_uri(self, url):
        resp = self.client.get(url)

    # 似乎另一個 request 會跳出 Http 500 錯誤, 所以在 View 裡面坐了 try-catch
    def test_multi_thread_get_book_by_transaction(self):
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
        self.assertEqual(person.objects.first().version, 50)

        print
        print 'In Transaction Condition:'
        print 'Expect Value: ',50, 50
        print 'Current Value: ',book.objects.first().version, person.objects.first().version
        print

    def test_multi_thread_get_book_by_non_transaction(self):
        th = []
        for i in range(0, 50):
            th.append(
                threading.Thread(
                    target=self.get_uri,
                    args=(self.non_transaction_uri,))
            )
        for i in th:i.start()
        for i in th:i.join()

        self.assertNotEqual(book.objects.first().version, 50)
        self.assertNotEqual(person.objects.first().version, 50)

        print
        print 'In Concurrency with Race Condition:'
        print 'Expect Value: ',50, 50
        print 'Current Value: ',book.objects.first().version, person.objects.first().version
        print

    def test_mix_uri_multi_thread_get_test(self):
        th = []
        for i in range(0, 50):
            if i % 7 == 0:
                # 8 Times, book+8, person+8
                th.append(
                    threading.Thread(
                        target=self.get_uri,
                        args=(self.transaction_uri,))
                )
            else:
                # 42 Times, person-42
                th.append(
                    threading.Thread(
                        target=self.get_uri,
                        args=(self.non_transaction_person_uri,))
                )
        for i in th:i.start()
        for i in th:i.join()

        self.assertEqual(book.objects.first().version, 8)
        self.assertEqual(person.objects.first().version, -34)

        print
        print 'Book Current Value: ', book.objects.first().version
        print 'Person Current Value: ', person.objects.first().version
        print
