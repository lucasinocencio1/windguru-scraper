import json

from constants import INCLUDED_LABELS, PARAM_LABELS


def format_forecast(raw_forecast: dict) -> list[dict]:
    """
    Transforms the raw scrape dictionary into a list of forecasts by time slot.
    Each item represents a time interval with day, hour and metrics.
    """
    if not raw_forecast:
        return []

    # Extract parameter name from row id (e.g. tabid_0_0_WINDSPD -> WINDSPD)
    def get_param(row_id: str) -> str:
        parts = row_id.split("_")
        return parts[-1] if parts else row_id

    # Find the time row (hour/day)
    time_values = None
    for row_id, values in raw_forecast.items():
        param = get_param(row_id)
        if param in ("time", "init") and values:
            time_values = values
            break

    if not time_values:
        time_values = list(range(len(next(iter(raw_forecast.values())))))

    num_slots = len(time_values)
    result = []

    for i in range(num_slots):
        slot = {}

        for row_id, values in raw_forecast.items():
            param = get_param(row_id)
            label = PARAM_LABELS.get(param, param.lower())
            if label not in INCLUDED_LABELS:
                continue

            if i < len(values) and values[i]:
                value = values[i].strip()
                if value and value != "-":
                    slot[label] = value

        result.append(slot)

    return result


def print_forecast(forecast: list[dict], indent: int = 2) -> None:
    """Prints the forecast formatted as readable JSON."""
    print(json.dumps(forecast, ensure_ascii=False, indent=indent))
