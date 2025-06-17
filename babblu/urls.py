from django.conf import settings # For checking if the project is in DEBUG mode
from django.conf.urls.static import static # For serving media files in development
from django.contrib import admin # For admin site
from django.urls import path, include # For URL routing
from accounts import views # Import views from the accounts app

# URL paths for the Django project
urlpatterns = [
    path('admin/', admin.site.urls), # Admin site URL
    path('', include('accounts.urls')), # Include URLs from the accounts app
    
    path('signup/', views.signup_view, name='signup'), # Signup view URL
    path('login/', views.login_view, name='login'), # Login view URL
    path('logout/', views.logout_view, name='logout'), # Logout view URL
    path('', views.home_view, name='home'), # Home view URL
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)