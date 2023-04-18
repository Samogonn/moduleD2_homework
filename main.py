#this is a file with shell commands for NewsPaper project

from accounts.models import *
from datetime import datetime

user1 = User.objects.create_user(username='John')
Author.objects.create(author=user1)

user2 = User.objects.create_user(username='Mike')
Author.objects.create(author=user2)

Category.objects.create(category_name='Technology')
Category.objects.create(category_name='Medicine')
Category.objects.create(category_name='Science')
Category.objects.create(category_name='IT')

Post.objects.create(author=Author.objects.get(author=User.objects.get(username='Mike')), type='NW', title='title1', text='text1')
Post.objects.create(author=Author.objects.get(author=User.objects.get(username='Mike')), type='AR', title='title2', text='text2')
Post.objects.create(author=Author.objects.get(author=User.objects.get(username='John')), type='AR', title='title3', text='text3')

p1 = Post.objects.get(title='title1')
p2 = Post.objects.get(pk=2)
p3 = Post.objects.get(author=Author.objects.get(author=User.objects.get(username='John')))

tech = Category.objects.get(category_name='Technology')
med = Category.objects.get(category_name='Medicine')
sci = Category.objects.get(category_name='Science')

p1.category.add(tech, med)
p2.category.add(sci, med)
p3.category.add(tech)
p3.category.add(Category.objects.get(category_name='IT'))

Comment.objects.create(post=Post.objects.get(title='title1'), user=User.objects.get(username='Mike'), text='comment1 text1')
Comment.objects.create(post=Post.objects.get(title='title2'), user=User.objects.get(username='Mike'), text='comment1 text2')
Comment.objects.create(post=Post.objects.get(title='title3'), user=User.objects.get(username='John'), text='comment1 text3')
Comment.objects.create(post=Post.objects.get(title='title1'), user=User.objects.get(username='John'), text='comment2 text1')

Post.objects.get(pk=1).like()
Post.objects.get(pk=1).like()
Post.objects.get(pk=2).like()
Post.objects.get(pk=3).like()
Post.objects.get(pk=3).like()
Post.objects.get(pk=3).dislike()

Comment.objects.get(pk=1).dislike()
Comment.objects.get(pk=1).like()
Comment.objects.get(pk=2).like()
Comment.objects.get(pk=4).like()
Comment.objects.get(pk=4).like()

for a in Author.objects.all():
    a.update_rating()

best_user = Author.objects.all().order_by('-rating').values('author__username', 'rating').first()
print(*best_user.values())

best_post = Post.objects.order_by('-rating').first()
best_post.datetime.strftime('%d.%m.%Y %H:%M')
best_post.author.author.username
best_post.rating
best_post.title
best_post.preview()

comments = best_post.comment_set.all()
for comment in comments:
    comment.datetime.strftime('%d.%m.%Y %H:%M')
    comment.user.username
    comment.rating
    comment.text
