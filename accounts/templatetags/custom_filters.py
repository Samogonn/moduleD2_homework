from django import template

register = template.Library()

#простой фильтр нецензурных слов на скорую руку
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
