from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def get_subscribers(category):
    subscribers_emails = []
    for subscriber in category.subscribers.all():
        subscribers_emails.append(subscriber.email)

    return subscribers_emails


def send_subscription_letter(instance):
    template = 'accounts/mail/new_post.html'

    for category in instance.category.all():
        subject = f'Новый пост в категории {category.category_name}'
        subscribers_emails = get_subscribers(category)

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
