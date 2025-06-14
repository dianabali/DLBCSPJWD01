from django.urls import path
from . import views

# URL paths for the accounts app
urlpatterns = [
    path('signup/', views.signup_view, name='signup'), # Sign-up page
    path('login/', views.login_view, name='login'), # Login page
    path('logout/', views.logout_view, name='logout'), # Logout page
    path('', views.home_view, name='home'), # Home page
    path('profile/', views.profile_view, name='profile'), # User profile page
    path('profile/edit/', views.edit_profile, name='edit_profile'), # Edit profile page
    path('add-card/', views.add_card, name='add_card'), # Add card page
    path('delete/<int:card_id>/', views.delete_card, name='delete_card'), # Delete card
    path('set-theme/', views.set_theme, name='set_theme'), # Set theme page
]
