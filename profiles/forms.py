from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, UserProfile, Comment, Endorsement

# -------------------------------
# Signup Form
# -------------------------------
class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

# -------------------------------
# Post Form
# -------------------------------
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share something...'}),
        }

# -------------------------------
# Profile Edit Form
# -------------------------------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'image', 'location', 'skills', 'job_title', 'website', 'contact', 'education']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself'}),
            'skills': forms.TextInput(attrs={'placeholder': 'e.g. Python, Django, HTML'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://yourportfolio.com'}),
            'contact': forms.TextInput(attrs={'placeholder': 'Email or phone'}),
            'education': forms.Textarea(attrs={'rows': 2}),
        }

# -------------------------------
# Comment Form
# -------------------------------
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write a comment...'}),
        }

# -------------------------------
# Endorsement Form
# -------------------------------
class EndorsementForm(forms.ModelForm):
    class Meta:
        model = Endorsement
        fields = ['skill']
        help_texts = {
            'skill': 'Enter a skill listed on the user’s profile.',
        }
        widgets = {
            'skill': forms.TextInput(attrs={'placeholder': 'e.g. JavaScript'}),
        }

# -------------------------------
# Search Form
# -------------------------------
class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search users by name, bio, or skill...',
        })
    )
