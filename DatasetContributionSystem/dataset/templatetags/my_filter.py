from django import template

register = template.Library()

@register.filter
def unitConvert(num):
    unit = ['', 'K', 'M', 'G', 'T', 'E']
    num = float(num)
    for i in range(0, 5):
        if num < 1024:
            return str(round(num, 2)) + unit[i]
        num /= 1024
    return str(round(num, 2)) + 'E'