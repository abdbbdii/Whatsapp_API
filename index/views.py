from django.http import HttpResponse
from django.urls.resolvers import URLResolver
from django.urls import get_resolver, reverse, NoReverseMatch
from django.utils.html import format_html


def index(request):
    def get_all_urls(urlpatterns, prefix=""):
        urls = []
        for url_pattern in urlpatterns:
            if hasattr(url_pattern, "name") and url_pattern.name:
                try:
                    path = reverse(url_pattern.name)
                    urls.append((url_pattern.name, path))
                except NoReverseMatch:
                    continue
            elif isinstance(url_pattern, URLResolver):
                new_prefix = prefix + url_pattern.pattern.regex.pattern
                urls.extend(get_all_urls(url_pattern.url_patterns, new_prefix))
        return urls

    resolver = get_resolver()
    all_urls = get_all_urls(resolver.url_patterns)
    url_list = "<h1>Index</h1><ul>"

    for name, path in all_urls:
        url_list += format_html('<li><a href="{}">{}</a></li>', path, name)

    url_list += "</ul>"

    return HttpResponse(url_list)
