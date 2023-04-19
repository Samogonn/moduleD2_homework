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


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
