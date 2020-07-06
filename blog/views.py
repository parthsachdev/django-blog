from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from .models import Post

# class based views
from django.views.generic import (
        ListView, DetailView, CreateView, UpdateView, DeleteView)

def home(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'AI'
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'   # the variable to be used in html file
    ordering = ['-date_posted']
    paginate_by = 5  # links are working now. site.com/?page=2

class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = 'posts'
    # ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))   # username is fetched from url
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'  # the default name is object
    # the default template name used by django is <app>/<model>_<viewtype>.html
    # thus it will look into blog/post_detail.html.

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    # for a createview type view, the default template is <appname>/<modelname>_form.html
    # here it is blog/post_form.html
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


def about(request):
    context = {
        'title': 'About page'
    }
    return render(request, 'blog/about.html', context)
