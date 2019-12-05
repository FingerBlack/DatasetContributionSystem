from django import template

register = template.Library()

@register.filter
def unitConvert(num):
    unit = ['K', 'M', 'G', 'T', 'E']
    if num < 1024:
        return str(num)
    num = float(num)
    for i in range(0, 5):
        num /= 1024
        if num < 1024:
            return str(round(num, 2)) + unit[i]
    return str(round(num, 2)) + unit[i]