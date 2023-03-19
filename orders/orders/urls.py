from django.contrib import admin
from django.urls import path

from order.views import OrderListView, chart

urlpatterns = [
    path('', OrderListView.as_view()),
    path('chart/', chart, name='chart'),
]
