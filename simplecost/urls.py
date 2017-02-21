from django.conf.urls import url

from .views import ExpenseListView, ExpenseCreate, print_it

urlpatterns = [
    url(r'^list-expense/$', ExpenseListView.as_view(), name = 'expense-list' ),
    url(r'^create-expense/$', ExpenseCreate.as_view(), name='expense-create'),
    url(r'^print-expense/$', print_it, name = 'print-expense-list' ),
]