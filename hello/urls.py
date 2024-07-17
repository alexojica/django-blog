from django.urls import path
from .views import post_list, add_post, register, generate_content

urlpatterns = [
    path('', post_list, name='post_list'),
    path('add/', add_post, name='add_post'),
    path('generate_content/', generate_content, name='generate_content'),  # Add this line
    path('register/', register, name='register'),
]
