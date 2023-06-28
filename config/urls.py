from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from news.views import *


router = routers.DefaultRouter()
router.register(r"posts", PostViewset)
router.register(r"categories", CategoryViewset)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("pages/", include("django.contrib.flatpages.urls")),
    path("news/", include("news.urls")),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("accounts.urls")),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
