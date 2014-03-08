from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'concurency_transaction_study.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^book/transaction_test', 'book.views.test_transaction'),
    url(r'^book/non_transaction_test', 'book.views.test_non_transaction'),
    url(r'^book/transaction_only_person_test', 'book.views.test_transaction_only_person'),
    url(r'^book/transaction_only_book_test', 'book.views.test_transaction_only_book'),
)
