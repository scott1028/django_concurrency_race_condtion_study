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
                row.version += 1
                row.save()
                break
        except Exception:
            pass

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