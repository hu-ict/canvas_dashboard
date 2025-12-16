# ==========
# Utilities
# ==========
from typing import List, Iterable, Callable, Dict, Optional, Tuple

from scripts.lib.bandwidth.lib_bandwidth_const import IMPROVEMENT_PERIOD
from scripts.model.Bandwidth import Point


def _make_my_days(day_count):
    days = []
    for day in range(day_count+1):
        days.append(day)
    return days


def calc_dev(iterations: int, r: int, a: float, b: float, c: float) -> List[float]:
    """
    Build a development series y(x) = a*x^2 + b*x + c for x in [0, iterations - r],
    clamp negatives to 0, and then append the last y value 'r' times.

    Returns a list of length (iterations + 1) to match day indexing [0..iterations].
    """
    iteration_list: List[float] = []
    last_y = 0.0
    for x in range(iterations - r + 1):
        y = a * x * x + b * x + c
        if y < 0:
            y = 0.0
        iteration_list.append(y)
        last_y = y

    for _ in range(r):
        iteration_list.append(last_y)

    return iteration_list


def calc_interp(x1: float, y1: float, x2: float, y2: float, x: float) -> float:
    """
    Linear interpolation:
        y = y1 + ((y2 - y1)/(x2 - x1)) * (x - x1)
    """
    if x2 == x1:
        return y1
    slope = (y2 - y1) / (x2 - x1)
    return y1 + slope * (x - x1)


def _sorted_keys(series: Dict[int, Dict[str, float]]) -> List[int]:
    """Return series keys sorted ascending."""
    return sorted(series.keys())


def _find_between(
    series: Dict[int, Dict[str, float]],
    level_key: str,
    x: float
) -> Tuple[float, float, float, float]:
    """
    Find bounding points (x1, y1, x2, y2) for x in a day->record series.

    Each record must contain at least {"day": int, level_key: float}.
    """
    keys = _sorted_keys(series)
    last_key = keys[-1]
    last_day = series[last_key]["day"]

    # Later than the last known day -> flat extension
    if x > last_day:
        return last_day, series[last_key][level_key], x, series[last_key][level_key]

    prev_key: Optional[int] = None
    for key in keys:
        day = series[key]["day"]
        if prev_key is None:
            prev_key = key
        prev_day = series[prev_key]["day"]
        if prev_day <= x <= day:
            return prev_day, series[prev_key][level_key], day, series[key][level_key]
        prev_key = key

    # Fallback (shouldn't occur in practice)
    return last_day, series[last_key][level_key], x, series[last_key][level_key]


def _append_points(days: Iterable[float], lowers: List[float], uppers: List[float]) -> List[Point]:
    """Create Point objects from aligned arrays."""
    points: List[Point] = []
    for i, day in enumerate(days):
        if i < len(lowers) and i < len(uppers):
            points.append(Point(day, lowers[i], uppers[i]))
    return points


def _series_from_sequences_sum(
    assignment_group,
    days_in_semester: int,
    exclude_aanvullend: bool = False,
    logger: Optional[Callable[[str], None]] = None
) -> Dict[int, Dict[str, float]]:
    """
    Build a series dict keyed by day with cumulative sum of points.

    Filters:
      - Skips sequences containing "Verbeter".
      - Skips days later than (days_in_semester - IMPROVEMENT_PERIOD).
      - Optionally skips names containing "Aanvullend".
    """
    series: Dict[int, Dict[str, float]] = {0: {"day": 0, "sum": 0}}
    total_points = 0

    for assignment_sequence in assignment_group.assignment_sequences:
        name = getattr(assignment_sequence, "name", "")
        day = assignment_sequence.get_day()
        # if "Verbeter" in name:
        #     continue
        # if exclude_aanvullend and "Aanvullend" in name:
        #     continue
        if day > (days_in_semester - IMPROVEMENT_PERIOD):
            continue

        total_points += assignment_sequence.points
        series[day] = {"day": day, "sum": total_points}

        if logger:
            out = f"LB08 - Day points; {assignment_sequence.points:3};{day:4};{total_points:>4}"
            logger(out.replace('.', ','))
    return series
