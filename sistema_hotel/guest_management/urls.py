#urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_booking/<str:room_number>/', views.create_booking, name='create_booking'),
    path('room/<str:room_number>/details/', views.room_details, name='room_details'),
    path('room/<str:room_number>/checkout/', views.checkout, name='checkout'),
    path('financial_report/', views.financial_report, name='financial_report'),
    path('all-stays/', views.all_stays, name='all_stays'),
    path('stay-details/<int:booking_id>/', views.stay_details, name='stay_details'),

]
