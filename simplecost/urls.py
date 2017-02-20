from django.conf.urls import url

from .views import ExpenseListView

urlpatterns = [
    url(r'^simplecost/$', ExpenseListView.as_view(), name = 'expense_list_view' ),
]