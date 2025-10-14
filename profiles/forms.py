# profiles/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm


# Import models from the same app
from .models import Post, UserProfile, Comment, Endorsement # Added Endorsement

# ===============================================
# 1. Signup Form
# ===============================================

class SignupForm(UserCreationForm):
    """
    Extends the built-in UserCreationForm to make the email field required.
    """
    email = forms.EmailField(required=True, label="Email")
    
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)


# ===============================================
# 2. Post Form
# ===============================================

class PostForm(forms.ModelForm):
    """
    Form for creating or editing a Post.
    """
    class Meta:
        model = Post
        fields = ['content', 'image'] # Assumes 'image' field exists on Post
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write something...'}),
        }

# ===============================================
# 3. Profile Form / EditProfileForm (Updated with all model fields)
# ===============================================

class ProfileForm(forms.ModelForm):
    """
    Form for editing the full UserProfile details.
    
    NOTE: This form now includes all the new fields required to fix the FieldError.
    """
    class Meta:
        model = UserProfile
        fields = [
            'profile_picture', # Renamed from 'image' to match your model
            'bio', 
            'location', 
            'job_title', 
            'website', 
            'contact', 
            'skills', 
            'education'
        ]

# ===============================================
# 4. Comment Form
# ===============================================

class CommentForm(forms.ModelForm):
    """
    Form for creating a Comment.
    """
    class Meta:
        model = Comment
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write a comment...'})
        }

# ===============================================
# 5. Search Form (Moved to top level to fix ImportError)
# ===============================================

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Search users...',
        'class': 'form-control'
    }))

# ===============================================
# 6. Endorsement Form (New Form for the new Model)
# ===============================================

class EndorsementForm(forms.ModelForm):
    """
    Form for adding an Endorsement.
    """
    class Meta:
        model = Endorsement
        fields = ['skill']
        widgets = {
            'skill': forms.TextInput(attrs={'placeholder': 'E.g., Python, UI/UX Design'})
        }