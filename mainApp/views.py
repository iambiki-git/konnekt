from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse



# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    
    return render(request, 'mainApp/home.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        surname = request.POST.get('surname', '').strip()
        day = request.POST.get('day', '').strip()
        month = request.POST.get('month', '').strip()
        year = request.POST.get('year', '').strip()
        gender = request.POST.get('gender', '').strip()
        email_or_phone = request.POST.get('email_or_phone', '').strip()
        password = request.POST.get('password', '').strip()

        print(email_or_phone)

        # Check for empty fields
        if not all([first_name, surname, day, month, year, gender, email_or_phone, password]):
            messages.error(request, 'All fields are required.')
            return redirect('signup')
        
        # Validate date of birth
        try:
            dob = datetime(int(year), int(month), int(day)).date()
        except (ValueError, TypeError):
            messages.error(request, 'Invalid date of birth.')
            return redirect('signup')

        # Validate email or phone
        try:
            validate_email(email_or_phone)
            is_email = True
        except ValidationError:
            is_email = False

        # Check if user already exists
        if User.objects.filter(Q(username=email_or_phone) | Q(email=email_or_phone)).exists():
            messages.error(request, 'A user with this email/phone already exists.')
            return redirect('signup')

        try:
            # Create User
            user = User.objects.create_user(
            first_name = first_name,
            last_name = surname, 
            username = email_or_phone,
            email=email_or_phone if is_email else "",
            password = password # django hashes this automatically
        )
            # Create UserProfile
            UserProfile.objects.create(
            user = user,
            dob = dob,
            gender = gender,    
            phone = None if is_email else email_or_phone,
        )
            messages.success(request, 'Account created successfully. Please sign in.')
            return redirect('signin')
    
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('signup')
        
    return render(request, 'mainApp/signup.html')


def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        email_or_phone = request.POST.get('email_or_phone')
        password = request.POST.get('password')

        try:
            # Try to find user by email or phone
            user = authenticate(request, username=email_or_phone, password=password)

            if user is not None:
                # If user is found and password matches
                login(request, user)
                return redirect('home')
            else:
                # If user is not authenticated, check if the email/phone exists
                # Assuming email_or_phone can be email or phone number
                if '@' in email_or_phone:
                    # Case where email is entered 
                    messages.error(request, 'Invalid email or password.')
                else:
                    # Case where phone number is entered
                    messages.error(request, 'Invalid phone number or password.')

        except ObjectDoesNotExist:
            # This handles case if the user doesn't exist at all
            messages.error(request, 'User with the provided email/phone does not exist.')

        return redirect('signin')

    return render(request, 'mainApp/signin.html')


def logout_view(request):
    logout(request)
    return redirect('signin')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'mainApp/profile.html')

@login_required
def upload_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile = UserProfile.objects.get(user=request.user)
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        return JsonResponse({'image_url': profile.profile_picture.url})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def navbar_context(request):
    profile_pic = None
    if request.user.is_authenticated:
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile_pic = user_profile.profile_picture.url if user_profile.profile_picture else None

    return {'profile_pic': profile_pic}


# def custom_404_view(request, exception):
#     return render(request, '404.html', status=404)