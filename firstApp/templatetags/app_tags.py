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

@register.assignment_tag
def econ(balls, runs, extra):
    try :
        return round((runs+extra)/(balls/6),2)
    except :
        return '-'

@register.assignment_tag
def avg(runs, extra, wickets):
    try :
        return round((runs+extra) / wickets,2)
    except :
        return '-'
