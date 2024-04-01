def taskName(func):
    """decorator for printing executed function name"""
    def wrapper(*args, **kwargs):
        print(f"running function : {func.__name__}")
        result = func(*args, **kwargs)
        return result
    return wrapper