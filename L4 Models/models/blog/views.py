from django.shortcuts import render

from .models import Post


def index(request):
    posts = Post.objects.filter(is_published=True)
    return render(request, 'blog/index.html', {'posts': posts})


def show_post(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'blog/post.html', {'post': post})
