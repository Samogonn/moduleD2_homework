import logging

from django.shortcuts import redirect
from django.urls import resolve
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache

from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm


from dotenv import load_dotenv


load_dotenv()


logger = logging.getLogger('django.security')
logger.debug('debug error')
logger.info('info error')
logger.warning('warning error')
logger.error('error error)')
logger.critical('critical error(')


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


class CategoryView(ListView):
    model = Category
    template_name = 'news/category.html'
    context_object_name = 'posts'

    # getting all posts by category
    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        c = Category.objects.get(id=self.id)
        queryset = Post.objects.filter(category=c)
        return queryset

    # getting all categories, current category and is user subscribed info
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        categories = Category.objects.all()
        context['categories'] = categories
        category = Category.objects.get(pk=self.id)
        context['category'] = category
        is_user_subscribed = category.subscribers.filter(email=user.email)

        context['is_user_subscribed'] = is_user_subscribed

        subscribers = category.subscribers.values
        context['subscribers'] = subscribers

        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/news_details.html'
    context_object_name = 'news_details'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'news-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'news-{self.kwargs["pk"]}', obj)

        return obj


class UpdatePost(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'news/create_post.html'
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
def subscribe_to_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)

    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
    else:
        return redirect('/accounts/protect/')


@login_required
def unsubscribe_from_category(request, pk):
    user = request.user
    c = Category.objects.get(id=pk)

    if c.subscribers.filter(id=user.id).exists():
        c.subscribers.remove(user)
    return redirect('/accounts/protect/')


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/accounts/protect/')
