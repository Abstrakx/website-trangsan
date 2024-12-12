from django import template
from datetime import datetime

register = template.Library()

@register.filter
def format_iso_datetime(value):
    try:
        dt_object = datetime.fromisoformat(value)
        return dt_object.strftime("%d %B %Y, %H:%M:%S")
    except ValueError:
        return value  
