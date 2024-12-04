def cast_int(input_value, raise_exception=True) -> int:
    try:
        return int(input_value)
    except ValueError as exc:
        if raise_exception:
            raise ValueError("Ошибка ввода: ожидалось число.") from exc

def pretty_list(_list: list) -> None:
    print("\n".join([f"    {str(task)}" for task in _list]))
