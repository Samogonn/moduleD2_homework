from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models import Sum
from allauth.account.forms import SignupForm

# Create your models here.

class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        post_rating = self.post_set.all().aggregate(postrating=Sum('rating'))
        pRating = 0
        pRating += post_rating.get('postrating')

        comment_rating = self.author.comment_set.all().aggregate(commentrating=Sum('rating'))
        cRating = 0
        cRating += comment_rating.get('commentrating')

        self.rating = pRating * 3 + cRating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique = True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    POST_TYPE_CHOICES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    ]

    type = models.CharField(
        max_length=2,
        choices=POST_TYPE_CHOICES,
        default=NEWS
    )
    datetime = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
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
        return self.text[:124] + '…'

    def get_absolute_url(self):
        return f'/news/{self.id}'


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


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
