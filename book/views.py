# coding: utf-8

from django.shortcuts import render
from django.db import transaction

# Create your views here.
from django.http import HttpResponse

from book.models import book, person

# 不會出現 Race Condition
def test_transaction(request):
    # build a response for cookie operation.    
    res=HttpResponse('Thanks for your comment!')

    while True:
        try:
            # 當發生 Dead Lock 的時候再存一次
            # MySQLdb 套件遇到 Transaction Concurrency 將拋 Dead Lock Error！
            with transaction.atomic():
                row = book.objects.first()
                row.version += 1
                row.save()
                row = person.objects.first()
                if row.version%20 == 0:
                    row.version +=10
                else:
                    row.version += 1
                row.save()
                break
        except Exception:
            pass

    # Person 加法展開分析：
    # 1      10
    # 2      11
    # 3      12
    # 4      13
    # 5      14
    # 6      15
    # 7      16
    # 8      17
    # 9      18
    # 10     19
    # 11     20
    # 12     30  (+10)
    # 13     31
    # 14     32
    # 15     33
    # 16     34
    # 17     35
    # 18     36
    # 19     37
    # 20     38
    # 21     39
    # 22     40
    # 23     50  (+10)
    # 24     51
    # 25     52
    # 26     53
    # 27     54
    # 28     55
    # 29     56
    # 30     57
    # 31     58
    # 32     59
    # 33     60
    # 34     70  (+10)
    # 35     71
    # 36     72
    # 37     73
    # 38     74
    # 39     75
    # 40     76
    # 41     77
    # 42     78
    # 43     79
    # 44     80
    # 45     90  (+10)
    # 46     91
    # 47     92
    # 48     93
    # 49     94
    # 50     95

    return res


# 將出現 Race Condition 連續兩次會造成資料結果錯誤
def test_non_transaction(request):
    # build a response for cookie operation.    
    res=HttpResponse('Thanks for your comment!')

    # non transaction
    row = book.objects.first()
    row.version += 1
    row.save()
    row = person.objects.first()
    row.version += 1
    row.save()

    return res

# Transaction 另一個 Model
def test_transaction_only_person(request):
    # build a response for cookie operation.    
    res=HttpResponse('Thanks for your comment with person!')

    while True:
        try:
            # 當發生 Dead Lock 的時候再存一次
            # MySQLdb 套件遇到 Transaction Concurrency 將拋 Dead Lock Error！
            with transaction.atomic():
                row = person.objects.first()
                row.version -= 1
                row.save()
                break
        except Exception:
            pass

    return res

def test_transaction_only_book(request):
    # build a response for cookie operation.    
    res=HttpResponse('Thanks for your comment with book!')

    while True:
        try:
            # 當發生 Dead Lock 的時候再存一次
            # MySQLdb 套件遇到 Transaction Concurrency 將拋 Dead Lock Error！
            with transaction.atomic():
                row = book.objects.first()
                row.version += 1
                row.save()
                break
        except Exception:
            pass

    return res