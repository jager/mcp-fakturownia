def to_dict(obj):
    if isinstance(obj, list):
        return [to_dict(i) for i in obj]
    elif hasattr(obj, "__dict__"):
        return {k: to_dict(v) for k, v in obj.__dict__.items()}
    else:
        return obj