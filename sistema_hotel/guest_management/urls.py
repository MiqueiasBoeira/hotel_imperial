#urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_booking/<str:room_number>/', views.create_booking, name='create_booking'),
    path('room/<str:room_number>/details/', views.room_details, name='room_details'),
    path('room/<str:room_number>/checkout/', views.checkout, name='checkout'),
    path('financial_report/', views.financial_report, name='financial_report'),
    path('all-stays/', views.all_stays, name='all_stays'),
    path('stay-details/<int:booking_id>/', views.stay_details, name='stay_details'),
    path('add-transaction/', views.add_financial_transaction, name='add_transaction'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login'), name='logout'),


]
