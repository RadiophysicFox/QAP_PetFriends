def write_log(func):
    def wrapper(*args, **kwargs):
        with open("log.txt", "a", encoding="utf-8") as log_file:
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            log_file.write(f"Вызываем функцию {func.__name__} с аргументами {signature}\n")
            value = func(*args, **kwargs)
            log_file.write(f"{func.__name__!r} вернула значение - {value!r}\n")
        log_file.close()
        return value
    return wrapper

