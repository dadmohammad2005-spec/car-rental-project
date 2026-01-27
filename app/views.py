from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import date
from .models import Car, Booking
from .forms import UserLoginForm, UserRegistrationForm, RentCarForm, AddCarForm


# ------------------- HOME / LOGIN -------------------
def home(request):
    if request.user.is_authenticated:
        return redirect('car_list')

    form = UserLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('car_list')
        messages.error(request, "Invalid credentials")

    return render(request, 'app/login.html', {'form': form})


# ------------------- REGISTER -------------------
def register(request):
    form = UserRegistrationForm(request.POST or None)
    print("Testing Running")
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Account created successfully")
        return redirect('car_list')
    return render(request, 'app/register.html', {'form': form})


# ------------------- LOGOUT -------------------
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out")
    return redirect('login')


# ------------------- ADD CAR -------------------
@login_required
def add_car(request):
    if request.method == 'POST':
        form = AddCarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            messages.success(request, "Car added successfully")
            return redirect('owner_dashboard')
    else:
        form = AddCarForm()
    return render(request, 'app/add_car.html', {'form': form})


# ------------------- CAR LIST -------------------


from datetime import date

def car_list(request):
    cars = Car.objects.all()
    cars_info = []

    for car in cars:
        # Check if car is booked today
        current_booking = Booking.objects.filter(
            car=car,
            status='confirmed',
            start_date__lte=date.today(),
            end_date__gte=date.today()
        ).first()

        # Future bookings
        future_bookings = Booking.objects.filter(
            car=car,
            status='confirmed',
            start_date__gt=date.today()
        ).order_by('start_date')

        cars_info.append({
            'car': car,
            'current_booking': current_booking,
            'future_bookings': future_bookings
        })

    return render(request, 'app/car_list.html', {'cars_info': cars_info})


# ------------------- RENT CAR -------------------
@login_required
def rent_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    form = RentCarForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        start = form.cleaned_data['start_date']
        end = form.cleaned_data['end_date']

        # Check overlapping with any confirmed booking
        overlap = Booking.objects.filter(
            car=car,
            status='confirmed'
        ).filter(
            Q(start_date__lt=end) & Q(end_date__gt=start)
        )

        if overlap.exists():
            messages.error(request, "Selected dates overlap with existing booking")
            return redirect('rent_car', car_id=car.id)

        booking = form.save(commit=False)
        booking.car = car
        booking.renter = request.user
        booking.total_price = (end - start).days * car.price_per_day
        booking.save()

        messages.success(request, "Car booked successfully")
        return redirect('my_bookings')

    # Pass future bookings for info
    future_bookings = Booking.objects.filter(
        car=car,
        status='confirmed',
        end_date__gte=date.today()
    ).order_by('start_date')

    return render(request, 'app/rent_car.html', {
        'form': form,
        'car': car,
        'future_bookings': future_bookings
    })


# ------------------- MY BOOKINGS -------------------
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(renter=request.user).order_by('-start_date')
    return render(request, 'app/my_bookings.html', {'bookings': bookings, 'today': date.today()})


# ------------------- CANCEL BOOKING -------------------
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        renter=request.user,
        status='confirmed'
    )

    if booking.start_date <= date.today():
        messages.error(request, "Cannot cancel started booking")
    else:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, "Booking cancelled")

    return redirect('my_bookings')


# ------------------- OWNER DASHBOARD -------------------
@login_required
def owner_dashboard(request):
    cars = Car.objects.filter(owner=request.user)
    bookings = Booking.objects.filter(car__owner=request.user).order_by('-start_date')
    available_cars = cars.filter(available=True).count()

    return render(request, 'app/owner_dashboard.html', {
        'cars': cars,
        'bookings': bookings,
        'available_cars': available_cars
    })


@login_required
def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, owner=request.user)
    if request.method == 'POST':
        form = AddCarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, "Car updated successfully!")
            return redirect('owner_dashboard')
    else:
        form = AddCarForm(instance=car)
    return render(request, 'app/edit_car.html', {'form': form, 'car': car})


@login_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, owner=request.user)
    if request.method == 'POST':
        car.delete()
        messages.success(request, "Car deleted successfully!")
        return redirect('owner_dashboard')
    return render(request, 'app/delete_car.html', {'car': car})
