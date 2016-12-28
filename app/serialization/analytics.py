from calendar import monthrange


def serialize_year_data(raw_data: dict) -> list:
    container = {(m + 1): 0 for m in range(11)}
    container.update(raw_data)
    return [{'label': key, 'value': val} for key, val in container.items()]


def serialize_month_data(raw_data: dict, year: int, month: int):
    max_day = monthrange(year, month)
    container = {(d + 1): 0 for d in range(max_day)}
    container.update(raw_data)
    return [{'label': key, 'value': val} for key, val in container.items()]


def serialize_day_data(raw_data: dict):
    container = {h: 0 for h in range(23)}
    container.update(raw_data)
    return [{'label': key, 'value': val} for key, val in container.items()]
