from django import template

register = template.Library()


# простой фильтр нецензурных слов на скорую руку


@register.filter(name='censor')
def censor(text):
    censor_words = ('мат', 'ещёмат', 'трехэтажныймат') #кортеж нецензурных слов

    censored_text = []

    for word in text.split():
        if word.lower().strip('''!()-[]{};?@#$%:'"\,./^&amp;*_''') in censor_words:
            word = '*' * len(word)
            censored_text.append(word)
        else:
            censored_text.append(word)

    return ' '.join(censored_text)


forbiden_words = []


@register.filter()
def another_cencor(text):
    return ' '.join([f'*{word[1:-1]}*' for word in text.split() if word in forbiden_words])
