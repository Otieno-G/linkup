from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # This must match the name and argument in your template
    path('like/<int:post_pk>/', views.like_post, name='like_post'),
]