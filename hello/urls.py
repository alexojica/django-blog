from django.urls import path
from .views import post_list, add_post, register, generate_content, post_detail, edit_profile, profile, search

urlpatterns = [
    path('', post_list, name='post_list'),
    path('add/', add_post, name='add_post'),
    path('register/', register, name='register'),
    path('generate/', generate_content, name='generate_content'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/<str:username>/', profile, name='profile'),
    path('search/', search, name='search'),
]