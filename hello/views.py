import json

from django.contrib.auth import login
from django.http import JsonResponse
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Post
from .forms import PostForm, RegisterForm


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'hello/post_list.html', {'posts': posts})


@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            if 'generate_content' in request.POST:
                main_idea = form.cleaned_data['content']
                main_idea = "random story be creative" if len(main_idea) == 0 else main_idea
                prompt = "Give me a short story(5 sentences max) about the following idea/summary: " + main_idea
                response = requests.post('http://127.0.0.1:8000/generate/', json={'text': prompt})
                if response.status_code == 200:
                    generated_content = response.json().get('generated_text')
                    form = PostForm(initial={'title': form.cleaned_data['title'], 'content': generated_content})
                else:
                    form.add_error('content', 'Failed to generate content.')
            else:
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'hello/add_post.html', {'form': form})


@csrf_exempt
def generate_content(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        main_idea = data.get('content')
        response = requests.post('http://127.0.0.1:3000/generate/', json={'text': main_idea})
        if response.status_code == 200:
            generated_content = response.json().get('generated_text')
            return JsonResponse({'generated_text': generated_content})
        else:
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
