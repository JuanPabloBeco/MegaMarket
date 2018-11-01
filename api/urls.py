from django.urls import path

from api import views

urlpatterns = [
    path('bought/', views.BoughtChart.as_view(), name='bought'),
]
