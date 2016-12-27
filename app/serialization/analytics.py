def serialize_year_data(raw_data: dict) -> list:
    container = {(m + 1): 0 for m in range(11)}
    container.update(raw_data)
    return [{'label': key, 'value': val} for key, val in container.items()]


def serialize_month_date(raw_data: dict):
    pass
