import re
from django import template

register = template.Library()

@register.filter
def regex_replace(value, args):
    """Replace the last URL segment with the language short name."""
    
    # args'leri virgülle ayırmaya çalışıyoruz
    try:
        url, lang = args.split(',')
    except ValueError:
        raise ValueError("args parametresi iki parçaya ayrılmalı: 'url' ve 'lang': ", args)

    # URL'yi '/' ile ayırıyoruz
    url_parts = url.split('/')

    # Son elemanı çıkarıyoruz
    url_parts.pop()

    # Dil kodunu son eleman olarak ekliyoruz
    url_parts.append(lang)

    # URL'yi tekrar birleştiriyoruz
    new_url = '/'.join(url_parts)

    # Sonuç olarak yeni URL'yi döndürüyoruz
    return new_url

@register.filter
def get_language_name(language_setting, selected_language):
    """Return the language name for the selected language."""
    for lang in language_setting:
        if lang.short_language_name.lower() == selected_language.lower():
            return lang.language_name
    return "Language"