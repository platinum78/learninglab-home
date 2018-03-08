from django import template
import numpy as np
register = template.Library()

@register.filter
def index(data_arr, idx):
    return data_arr[idx]

def add(val, arg):
    return val+arg

def sub(val, arg):
    return val-arg

def mul(val, arg):
    return val*arg

def div(val, arg):
    return val/arg
