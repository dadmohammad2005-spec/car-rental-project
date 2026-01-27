from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.home, name='login'),
    path("home/", views.home, name="home"),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),

    # Cars
    path('cars/', views.car_list, name='car_list'),
    path('rent/<int:car_id>/', views.rent_car, name='rent_car'),

    # My Bookings
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    # Owner Dashboard
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('dashboard/add-car/', views.add_car, name='add_car'),

    path('dashboard/car/edit/<int:car_id>/', views.edit_car, name='edit_car'),
    path('dashboard/car/delete/<int:car_id>/', views.delete_car, name='delete_car'),


]
