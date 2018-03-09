from django import template
register = template.Library()

@register.filter
def index(data_arr, idx):
    return data_arr[idx]

def isodd(val):
    if int(val/2) == val/2:
        return False
    else:
        return True

def iseven(val):
    if int(val/2) == val/2:
        return True
    else:
        return False
