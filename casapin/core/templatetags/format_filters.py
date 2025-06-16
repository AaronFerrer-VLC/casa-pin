from django import template

register = template.Library()

@register.filter
def as_float(value):
    try:
        return format(float(value), ".6f")
    except (ValueError, TypeError):
        return "0.000000"
