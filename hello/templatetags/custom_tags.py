from django import template

register = template.Library()


@register.inclusion_tag('hello/generate_content_button.html')
def generate_content_button():
    return {}
