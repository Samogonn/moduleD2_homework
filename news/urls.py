
from django.urls import path
from .views import NewsList, NewsDetail, Search, CreatePost, DeletePost, UpdatePost, CategoryList, upgrade_me

urlpatterns = [
    path('', NewsList.as_view(), name='news'),
    path('<int:pk>/', NewsDetail.as_view(), name='post_details'),
    path('search/', Search.as_view()),
    path('add/', CreatePost.as_view(), name='create_post'),
    path('<int:pk>/delete/', DeletePost.as_view(), name='delete_post'),
    path('<int:pk>/edit/', UpdatePost.as_view(), name='update_post'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>/', CategoryList.as_view(), name='category_list'),
]
