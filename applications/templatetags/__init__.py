from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    """Multiply the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def divide(value, arg):
    """Divide the value by the argument."""
    try:
        return float(value) / float(arg) if float(arg) != 0 else 0
    except (ValueError, TypeError):
        return 0


@register.filter
def floating_point_format(value, decimal_places=1):
    """Format a number to specified decimal places."""
    try:
        return f"{float(value):.{decimal_places}f}"
    except (ValueError, TypeError):
        return "0"


@register.filter
def percentage(value, total):
    """Calculate percentage."""
    try:
        if total == 0:
            return 0
        return (float(value) / float(total)) * 100
    except (ValueError, TypeError):
        return 0
