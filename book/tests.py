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
        self.transaction_book_uri = '/book/transaction_only_book_test/'
        self.transaction_person_uri = '/book/transaction_only_person_test/'

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
        self.assertEqual(person.objects.first().version, 95)

        print
        print 'In Transaction Condition:'
        print 'Expect Value: ',50, 95
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
                # 8 Times, book+8, person+17 (0:10, 1~7:7, total:17)
                th.append(
                    threading.Thread(
                        target=self.get_uri,
                        args=(self.transaction_uri,))
                )
            else:
                # 42 Times, book+42
                th.append(
                    threading.Thread(
                        target=self.get_uri,
                        args=(self.transaction_book_uri,))
                )
        for i in th:i.start()
        for i in th:i.join()

        self.assertEqual(book.objects.first().version, 50) # 50
        self.assertEqual(person.objects.first().version, 17) # 17

        print
        print 'Book Current Value: ', book.objects.first().version
        print 'Person Current Value: ', person.objects.first().version
        print

    def test_mix_uri_mutli_thread_get_test2(self):
        th = []
        for i in range(0, 50):
            if i % 7 == 0:
                # 8 Times, book+8, person+17 (0:10, 1~7:7, total:17)
                th.append(
                    threading.Thread(
                        target=self.get_uri,
                        args=(self.transaction_uri,))
                )
            else:
                # 42 Times, book+42
                th.append(
                    threading.Thread(
                        target=self.get_uri,
                        args=(self.transaction_person_uri,))
                )
        for i in th:i.start()
        for i in th:i.join()

        self.assertEqual(book.objects.first().version, 8) # 8

        # 這情況下 persion value of the person 是無法預測的, 因為他是 -1 邏輯可能會讓 book 的 +10 邏輯重復觸發
        # self.assertEqual(person.objects.first().version, 17)

        print
        print 'Book Current Value: ', book.objects.first().version
        print 'Person Current Value: ', person.objects.first().version
        print
