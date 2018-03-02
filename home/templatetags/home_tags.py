from django import template
register = template.Library()

@register.filter
def index(data_arr, idx):
    return data_arr[idx]
