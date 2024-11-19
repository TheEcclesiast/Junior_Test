import inspect

def strict(func):
    def wrapper(*args, **kwargs):
        # inspect.signature(func) для извлечения сигнатуры функции. Она возвращает объект signature, который содержит параметры функции (Что нам пригодится в дальнейшем)
        sig = inspect.signature(func)


        for arg_value, (param_name, param) in zip(args, sig.parameters.items()): #В sig.parameters.items() находятся параметры функции с их типами, если они аннотированы
            expected_type = param.annotation
            if expected_type is not inspect.Parameter.empty:
                if not isinstance(arg_value, expected_type):
                    raise TypeError(
                        f"Аргумент '{param_name}' не соответствует типу {expected_type.__name__}.\n"
                        f"Получен {type(arg_value).__name__}, пожалуйста проверьте типы аргументов в функции {func.__name__}"
                    )

        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b



print(sum_two(1, 2))
try:
    print(sum_two(1, 2.4))
except TypeError as e:
    print(e)
