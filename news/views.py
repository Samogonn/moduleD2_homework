from django.shortcuts import render, redirect
from django.urls import resolve
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm


class NewsList(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news_list'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.all()
        context['category'] = category
        return context


class CreatePost(PermissionRequiredMixin, CreateView):
    template_name = 'news/create_post.html'
    form_class = PostForm
    permission_required = ('news.add_post', )


class Search(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class CategoryList(ListView):
    model = Post
    template_name = 'news/category.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        c = Category.objects.get(id=self.id)
        queryset = Post.objects.filter(category=c)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        category = Category.objects.get(pk=self.id)
        context['category'] = category
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/news_details.html'
    context_object_name = 'news_details'


class UpdatePost(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'create_post.html'
    form_class = PostForm
    permission_required = ('news.change_post', )

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class DeletePost(DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/protect/')
