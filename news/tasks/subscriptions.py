from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.models import User

from datetime import datetime, timedelta
from pytz import UTC

from news.models import Category

def send_subscription_letter(instance):
    template = 'accounts/mail/new_post.html'

    for category in instance.category.all():
        subject = f'Новый пост в категории {category.category_name}'
        subscribers_emails = [subscriber.email for subscriber in category.subscribers.all()]

        html = render_to_string(
            template,
            {
                'category': category,
                'post': instance,
            },
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=subscribers_emails
        )

        msg.attach_alternative(html, 'text/html')

        msg.send()

def send_weekly_subscription_letter():
    template = 'accounts/mail/weekly_posts.html'

    users = User.objects.all()

    users_mail = {}

    for category in Category.objects.all():
        new_category_posts = [post for post in category.post_set.all() if post.datetime.replace(tzinfo=UTC) > (datetime.now() - timedelta(weeks=1)).replace(tzinfo=UTC)]

        for subscriber in category.subscribers.all():
            users_mail.setdefault(subscriber.email, set()).update(new_category_posts)

    for user in users:
        if users_mail.get(user.email, None):
            subject = 'Новые посты за неделю по вашей подписке.'
            html = render_to_string(
                template,
                {
                    'posts': users_mail[user.email],
                },
            )

            msg = EmailMultiAlternatives(
                subject=subject,
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email, ]
            )

            msg.attach_alternative(html, 'text/html')

            msg.send()
