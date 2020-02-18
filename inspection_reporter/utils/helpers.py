def get_if_exists(model, *args, **kwargs):
    """Checks to see if entry exists or returns None."""
    try:
        obj = model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        obj = None
    return obj


def calculate_new_average(previous_avg, count, value):
    """ Update average for new entry

    total = previous_avg * (count - 1) + value

    return total / count
    """
    total = previous_avg * (count - 1) + value
    return total / count
