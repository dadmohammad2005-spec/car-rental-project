from django.contrib import admin
from .models import Car, Booking, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_owner')
    list_filter = ('is_owner',)
    search_fields = ('user__username',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'model', 'owner', 'price_per_day', 'created_at')
    search_fields = ('name', 'model', 'owner__username')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'car', 'renter', 'start_date',
        'end_date', 'total_price', 'status'
    )
    list_filter = ('status', 'start_date')
    search_fields = ('car__name', 'renter__username')

