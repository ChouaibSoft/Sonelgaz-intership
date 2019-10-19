from django import template

register = template.Library()


@register.filter('multiply')
def multiply(value, args):
    value *= args
    return value


@register.filter('tva')
def tva(value, args):
    value *= (1 + args / 100)
    return value


@register.filter('divide')
def divide(value, args):
    value /= args
    return value


@register.filter('concat')
def concat(value, string):
    return value + string


