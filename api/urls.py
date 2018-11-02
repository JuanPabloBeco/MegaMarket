from django.urls import path

from api import views

urlpatterns = [
    path('bought/', views.BoughtChart.as_view(), name='bought'),
    path('sold/', views.SoldChart.as_view(), name='sold'),
    path('boughtsold/', views.BoughtSoldChart.as_view(), name='boughtsold'),
    path('earnedboughtsold/', views.EarnedBoughtSoldChart.as_view(), name='earnedboughtsold'),
]
