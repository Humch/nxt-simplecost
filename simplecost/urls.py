from django.conf.urls import url

from .views import ExpenseListView, ExpenseCreate, print_it

urlpatterns = [
    url(r'^simplecost/$', ExpenseListView.as_view(), name = 'expense_list_view' ),
    url(r'^create-expense/$', ExpenseCreate.as_view(), name='expense-create'),
    url(r'^printit/$', print_it, name = 'print_it' ),
]