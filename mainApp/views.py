from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'mainApp/index.html')

def signup(request):
    return render(request, 'mainApp/signup.html')