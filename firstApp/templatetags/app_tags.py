from django import template

register = template.Library()

@register.assignment_tag
def sub(arg1, arg2):
    return arg1 - arg2

@register.assignment_tag
def div(arg1, arg2):
    try :
        return round(arg1 / arg2,2)
    except :
        return '-'    
