from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('sign-up/', views.signup, name='signup'),
    path('sign-in/', views.signin, name='signin'),
    path('sign-out/', views.logout_view, name='logout_view'),

    path('profile/', views.profile, name='profile'),
    path('upload-profile-picture/', views.upload_profile_picture, name='upload-profile-picture'),

]
# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)