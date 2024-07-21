import json
import logging

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Post, Profile
from .forms import PostForm, RegisterForm, CommentForm, ProfileForm

logger = logging.getLogger(__name__)


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'hello/post_list.html', {'page_obj': page_obj})


@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post added successfully!')
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'hello/add_post.html', {'form': form})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'hello/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


@csrf_exempt
def generate_content(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            main_idea = data.get('text', 'random story be creative')
            prompt = f"Give me a short story (5 sentences max) about the following idea/summary: {main_idea}"
            response = requests.post('http://127.0.0.1:3000/generate/', json={'text': prompt})
            response.raise_for_status()  # Raise an exception for HTTP errors
            generated_content = response.json().get('generated_text')
            return JsonResponse({'generated_text': generated_content})
        except requests.RequestException as e:
            logger.error(f"Failed to generate content: {e}")
            return JsonResponse({'error': 'Failed to generate content'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')  # Redirect to the post list page
    else:
        form = RegisterForm()
    return render(request, 'hello/register.html', {'form': form})


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'hello/edit_profile.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'hello/profile.html', {'profile': profile})


def search(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    else:
        posts = Post.objects.all()
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'hello/post_list.html', {'page_obj': page_obj})
