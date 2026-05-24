from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, Car, Profile
from datetime import date



# ------------------- ADD CAR FORM -------------------
class AddCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'model', 'year', 'price_per_day', 'available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Car Name'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Model'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year'}),
            'price_per_day': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price per day'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ------------------- RENT CAR FORM -------------------
class RentCarForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {'start_date': '', 'end_date': ''}

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_date')
        end = cleaned.get('end_date')

        if start and start < date.today():
            raise forms.ValidationError("Start date cannot be in the past")

        if start and end and end <= start:
            raise forms.ValidationError("End date must be after start date")


# ------------------- LOGIN FORM -------------------
class UserLoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'
    }))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'
    }))


# ------------------- REGISTRATION FORM -------------------
class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'
    }))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Email'
    }))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'
    }))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm Password'
    }))
    
    ROLE_CHOICES = [
        ('renter', 'Renter (I want to rent cars)'),
        ('owner', 'Car Owner (I want to list my cars)'),
    ]
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='renter',
        label='Register As'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        role = self.cleaned_data.get('role')
        profile, created = Profile.objects.get_or_create(user=user)
        profile.is_owner = (role == 'owner')
        profile.save()
        return user

