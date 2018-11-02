from django.urls import path

from mega_market_core import views

urlpatterns = [
    path('ticket/', views.ticket, name='ticket'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
