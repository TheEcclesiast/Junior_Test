from functools import wraps

def strict(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Получаю аннотации типов, что было разрешено в условии
        annotations = func.__annotations__
        arguments = list(args)
        # Параметры функции (здесь ключи - имена аргументов, а значения - их типы (В теории))
        param_names = func.__code__.co_varnames[:len(arguments)]

        for param, value in zip(param_names, arguments):
            if param in annotations:
                expected_type = annotations[param]
                # Проверка соответствия типа параметра типу аргумента
                if not isinstance(value, expected_type):
                    raise TypeError(f"Аргумент '{param}' не соответствует типу {expected_type.__name__}, "
                                    f"получен {type(value).__name__}")

        return func(*args, **kwargs)
    return wrapper

@strict
def sum_two(a: int, b: int) -> int:
    return a + b

print(sum_two(1, 2))
print(sum_two(1, 2.4))