from django import template
from ..models import UserProfile # Import the UserProfile model

# The necessary line to register this module as a template tag library
register = template.Library()

# ====================================================
# UTILITY FILTERS (Existing code)
# ====================================================

@register.filter(name='split')
def split(value, key=None):
    """
    Splits a string by a given key (defaulting to comma) and returns a list.
    Usage: {{ profile.skills|split:"," }}
    """
    if value:
        # If no key is provided, split by comma and clean up resulting spaces
        if key is None:
            return [s.strip() for s in value.split(',')]
        
        # If a key is provided, split by that key
        return value.split(key)
    return []

@register.filter(name='trim')
def trim(value):
    """
    Removes leading and trailing whitespace from a string.
    Usage: {{ some_string|trim }}
    """
    if value is not None and isinstance(value, str):
        return value.strip()
    return value

# ====================================================
# PROFILE STRENGTH METER FILTER (New code)
# ====================================================

@register.filter
def profile_strength(profile):
    """
    Calculates the completeness percentage of a UserProfile.
    
    Checks for: 
    1. Profile Image
    2. Job Title
    3. Location
    4. Bio
    5. Skills (Checks if the text field is not empty)
    """
    
    total_points = 5
    completed_points = 0

    if not isinstance(profile, UserProfile):
        return 0

    # 1. Profile Image 
    # Check if the ImageField has a file associated with it
    if profile.image:
        completed_points += 1
        
    # 2. Job Title
    if profile.job_title:
        completed_points += 1
        
    # 3. Location
    if profile.location:
        completed_points += 1
        
    # 4. Bio
    if profile.bio:
        completed_points += 1
        
    # 5. Skills
    if profile.skills:
        completed_points += 1
        
    if total_points == 0:
        return 0
        
    # Calculate percentage
    percentage = int((completed_points / total_points) * 100)
    
    return percentage