from django.conf.urls import url, include
from auxiliare import urls
from .views import ThirdPartyCreate, PaymentModeCreate, ExpenseListView, ExpenseCreate, ExpenseUpdate, ExpenseDelete, print_it

urlpatterns = [
    url(r'^', include('auxiliare.urls')),
    url(r'^list-expense/$', ExpenseListView.as_view(), name = 'expense-list' ),
    url(r'^create-expense/$', ExpenseCreate.as_view(), name='expense-create'),
    url(r'^update-expense/(?P<pk>\d+)/$', ExpenseUpdate.as_view(), name='expense-update'),
    url(r'^delete-expense/(?P<pk>\d+)/$', ExpenseDelete.as_view(), name='expense-delete'),
    url(r'^create-thirdparty/$', ThirdPartyCreate.as_view(), name='thirdparty-create'),
    url(r'^create-paymentmode/$', PaymentModeCreate.as_view(), name='paymentmode-create'),
    url(r'^print-expense$', print_it, name = 'print-expense-list' ),
]