from django.urls import path
from .views import (
    NewsList,
    NewsDetail,
    Search,
    CreatePost,
    DeletePost,
    UpdatePost,
    CategoryView,
    upgrade_me,
    subscribe_to_category,
    unsubscribe_from_category,
)
from django.views.decorators.cache import cache_page


urlpatterns = [
    path("", cache_page(60)(NewsList.as_view()), name="news"),
    path("<int:pk>/", NewsDetail.as_view(), name="post_details"),
    path("search/", Search.as_view()),
    path("add/", CreatePost.as_view(), name="create_post"),
    path("<int:pk>/delete/", DeletePost.as_view(), name="delete_post"),
    path("<int:pk>/edit/", UpdatePost.as_view(), name="update_post"),
    path("upgrade/", upgrade_me, name="upgrade"),
    path("categories/<int:pk>/", CategoryView.as_view(), name="category"),
    path("categories/<int:pk>/subscribe/", subscribe_to_category, name="subscribe"),
    path("unsubscribe/<int:pk>", unsubscribe_from_category, name="unsubscribe"),
]
