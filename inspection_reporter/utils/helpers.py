def get_if_exists(model, *args, **kwargs):
    """Checks to see if entry exists or returns None."""
    try:
        obj = model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        obj = None
    return obj
