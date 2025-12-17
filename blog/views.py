from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Post, Category, Tag, Comment
from .forms import PostForm, CommentForm


class PostList(ListView):
    model = Post
    ordering = '-pk'
    template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm()
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    login_url = '/admin/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    login_url = '/admin/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    login_url = '/admin/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(request, 'blog/post_list.html', {
        'post_list': post_list,
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count(),
        'category': category,
    })


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(request, 'blog/post_list.html', {
        'post_list': post_list,
        'tag': tag,
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count(),
    })


def index(request):
    recent_posts = Post.objects.order_by('-created_at')[:3]
    return render(request, 'blog/index.html', {
        'recent_posts': recent_posts,
    })


def about_me(request):
    return render(request, 'blog/about_me.html')


@login_required(login_url='/admin/login/')
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect('post_detail', pk=pk)


@login_required(login_url='/admin/login/')
def delete_comment(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.author:
        comment.delete()
    return redirect('post_detail', pk=pk)


def search(request):
    query = request.GET.get('q', '')
    if query:
        post_list = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()
    else:
        post_list = Post.objects.none()

    return render(request, 'blog/post_list.html', {
        'post_list': post_list,
        'search_query': query,
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count(),
    })
