from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from news.models import Category

# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()

        user_categories = []
        for category in Category.objects.all():
            if category.subscribers.filter(id=user.id).exists():
                user_categories.append(category)

        context['user_categories'] = user_categories
        return context
