from django.shortcuts import get_object_or_404, render, redirect # Import necessary functions for rendering views and redirecting
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash # Import authentication functions
from django.contrib.auth.forms import AuthenticationForm # Import authentication form for login
from django.contrib.auth.decorators import login_required # Import decorator to require login for certain views
from .forms import CombinedProfileForm, CustomUserCreationForm, OptionalPasswordChangeForm, SpeechCardForm # Import custom forms for user creation, profile editing, and speech card handling
from .models import Profile, SpeechCard # Import models for user profile and speech cards
from django.templatetags.static import static # Import static files handling for serving profile pictures

# Home view for the application
@login_required
def home_view(request):
    default_cards = SpeechCard.objects.filter(user__isnull=True)
    user_cards = SpeechCard.objects.filter(user=request.user)
    cards = list(default_cards) + list(user_cards)
    
    # Add theme to context
    theme = request.session.get('theme', 'blue')
    
    return render(request, 'accounts/home.html', {
        'cards': cards,
        'theme': theme,
    })

# Sign-up view
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            # Render the form with errors if invalid
            return render(request, 'accounts/signup.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

# Login view with 'remember me' functionality
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) 
                response = redirect('home') 

                # Check if 'remember me' checkbox was selected
                remember = request.POST.get('remember', False)
                if remember:
                    response.set_cookie('remembered_username', username, max_age=60*60*24*30)  # 30 days
                else:
                    response.delete_cookie('remembered_username')

                return response
    else:
        form = AuthenticationForm()

        # Pre-fill the username field if 'remembered_username' cookie exists
        remembered_username = request.COOKIES.get('remembered_username')
        if remembered_username:
            form.fields['username'].initial = remembered_username

    return render(request, 'accounts/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Profile view 
@login_required
def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if profile.profile_picture:
        profile_pic_url = profile.profile_picture.url
    else:
        profile_pic_url = static('img/default.jpg')

    return render(request, 'accounts/profile.html', {
        'user': user,
        'profile': profile,
        'banner_color': profile.banner_color,
        'profile_pic_url': profile_pic_url,
    })

# Edit profile view
@login_required
def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = CombinedProfileForm(request.POST, request.FILES, user=user)
        pwd_form = OptionalPasswordChangeForm(user=user, data=request.POST)

        banner_color = request.POST.get('banner_color', profile.banner_color)

        if form.is_valid():
            user, profile = form.save()

            # ✅ Manually save uploaded profile picture
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            
            profile.banner_color = banner_color
            profile.save()

            # Handle password update
            if any(request.POST.get(f) for f in ['old_password', 'new_password1', 'new_password2']):
                if pwd_form.is_valid():
                    pwd_form.save()
                    update_session_auth_hash(request, pwd_form.user)
                    return redirect('profile')
                else:
                    return render(request, 'accounts/edit_profile.html', {
                        'form': form,
                        'pwd_form': pwd_form,
                        'banner_color': profile.banner_color,
                        'profile_pic_url': profile.profile_picture.url if profile.profile_picture else static('img/default.jpg'),
                    })

            return redirect('profile')

    else:
        form = CombinedProfileForm(user=user)
        pwd_form = OptionalPasswordChangeForm(user=user)

    profile_pic_url = profile.profile_picture.url if profile.profile_picture else static('img/default.jpg')

    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'pwd_form': pwd_form,
        'banner_color': profile.banner_color,
        'profile_pic_url': profile_pic_url,
    })

# Add a new speech card - view
@login_required
def add_card(request):
    if request.method == 'POST':
        form = SpeechCardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            return redirect('home')
    else:
        form = SpeechCardForm()
    return render(request, 'accounts/add_card.html', {'form': form})

# Delete a speech card - view
@login_required
def delete_card(request, card_id):
    card = get_object_or_404(SpeechCard, id=card_id, user=request.user)
    if request.method == 'POST':
        card.delete()
    return redirect('home')

# Set theme for the application
def set_theme(request):
    if request.method == 'POST':
        request.session['theme'] = request.POST.get('theme')
    return redirect(request.META.get('HTTP_REFERER', '/'))