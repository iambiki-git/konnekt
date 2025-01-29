from django.shortcuts import render

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'mainApp/signin.html')
    
    return render(request, 'mainApp/index.html')

from datetime import datetime
def signup(request):
    return render(request, 'mainApp/signup.html')

def signin(request):
    return render(request, 'mainApp/signin.html')



