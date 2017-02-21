from django.conf.urls import url

from .views import ExpenseListView, print_it

urlpatterns = [
    url(r'^simplecost/$', ExpenseListView.as_view(), name = 'expense_list_view' ),
    url(r'^printit/$', print_it, name = 'print_it' ),
]