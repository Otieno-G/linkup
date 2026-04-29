from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# --- SIGNUP FORM ---
class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

# --- POST FORM ---
class PostForm(forms.ModelForm):
    class Meta:
        # Import inside Meta to prevent circular dependency
        from posts.models import Post 
        model = Post
        fields = ['content', 'image'] 
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': "What's on your mind?"}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

# --- PROFILE EDIT FORM ---
class ProfileForm(forms.ModelForm):
    class Meta:
        # Import inside Meta to prevent circular dependency
        from profiles.models import UserProfile
        model = UserProfile
        fields = ['image', 'bio', 'location', 'skills', 'job_title', 'website', 'contact', 'education']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself'}),
            'skills': forms.TextInput(attrs={'placeholder': 'e.g. Python, Django, HTML'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://yourportfolio.com'}),
            'contact': forms.TextInput(attrs={'placeholder': 'Email or phone'}),
            'education': forms.Textarea(attrs={'rows': 2}),
        }

# --- COMMENT FORM ---
class CommentForm(forms.ModelForm):
    class Meta:
        # Import inside Meta to prevent circular dependency
        from posts.models import Comment
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write a comment...'}),
        }