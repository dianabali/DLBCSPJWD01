from django import forms # Import Django forms module
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm # Import forms for user creation and password change
from django.contrib.auth.models import User # Import User model for authentication
from .models import Profile, SpeechCard # Import Profile and SpeechCard models
from django import forms
from django.contrib.auth.models import User
from .models import Profile

# CombinedProfileForm combines user and profile information into a single form.
class CombinedProfileForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    profile_picture = forms.ImageField(required=False)
    banner_color = forms.CharField(
        max_length=7, 
        required=False, 
        widget=forms.TextInput(attrs={'type': 'color'})
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user:
            self.fields['username'].initial = user.username
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

            profile = getattr(user, 'profile', None)
            if profile:
                self.fields['profile_picture'].initial = profile.profile_picture
                self.fields['banner_color'].initial = profile.banner_color

    def clean_username(self):
        username = self.cleaned_data['username']
        if username != self.user.username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("This username is already taken.")
        return username

    def save(self, commit=True):
        user = self.user
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()

        profile, created = Profile.objects.get_or_create(user=user)

        if self.cleaned_data.get('profile_picture'):
            profile.profile_picture = self.cleaned_data['profile_picture']

        profile.banner_color = self.cleaned_data.get('banner_color', profile.banner_color)

        if commit:
            profile.save()

        return user, profile

# OptionalPasswordChangeForm allows users to change their password optionally.
class OptionalPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make password fields optional
        self.fields['old_password'].required = False
        self.fields['new_password1'].required = False
        self.fields['new_password2'].required = False

    # Custom clean method to handle optional password fields
    def clean(self):
        cleaned_data = super().clean()
        old = cleaned_data.get('old_password')
        new1 = cleaned_data.get('new_password1')
        new2 = cleaned_data.get('new_password2')
    
        # If any password field is filled, require all to be valid
        if old or new1 or new2:
            # Run full validation (calls parent's clean())
            return super().clean()
        else:
            # If all empty, skip validation and clear errors
            self._errors = {}
            return cleaned_data

# A form for creating new users with additional fields.
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "The passwords didn't match.")

# User form 
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

# Speech card form
class SpeechCardForm(forms.ModelForm):
    class Meta:
        model = SpeechCard
        fields = ['text', 'image']