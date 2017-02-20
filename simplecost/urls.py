from django.conf.urls import url

from .views import BasicView

urlpatterns = [
    url(r'^$', BasicView.as_view(), name = 'basic_view' ),
]