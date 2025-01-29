
from django.contrib import admin
from django.urls import path, include
# from django.conf.urls import handler404
# from mainApp.views import custom_404_view  # Adjust import based on your app name

# handler404 = custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainApp.urls')),
]

