from django.db import models
from django.contrib.auth.models import User

# ------------------- CAR MODEL -------------------
class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.model})"


# ------------------- BOOKING MODEL -------------------
class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    renter = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car.name} - {self.renter.username}"


# ------------------- USER PROFILE MODEL -------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_owner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({'Owner' if self.is_owner else 'Renter'})"


# Signals to automatically create user profile when user is created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    profile, created = Profile.objects.get_or_create(user=instance)
    profile.save()

