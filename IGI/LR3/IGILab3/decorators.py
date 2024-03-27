def taskName(func):
    def wrapper(*args, **kwargs):
        print(f"running function : {func.__name__}")
        result = func(*args, **kwargs)
        return result
    return wrapper