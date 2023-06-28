from django.db import models
from django.contrib.auth.models import User
from accounts.models import Author
from django.core.cache import cache


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)

    def __str__(self) -> str:
        return f"{self.category_name}"


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = "NW"
    ARTICLE = "AR"
    POST_TYPE_CHOICES = [(NEWS, "Новость"), (ARTICLE, "Статья")]

    type = models.CharField(max_length=2, choices=POST_TYPE_CHOICES, default=NEWS)
    datetime = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + "…"

    def get_absolute_url(self):
        return f"/news/{self.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f"news-{self.pk}")


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=512)
    datetime = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
