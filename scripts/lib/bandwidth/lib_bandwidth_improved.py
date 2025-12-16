from typing import Optional, Iterable, Callable
from scripts.lib.bandwidth.lib_bandwidth_const import IMPROVEMENT_PERIOD
from scripts.lib.bandwidth.lib_bandwidth_strategy import ExponentialStrategy, LinPointsStrategy, \
    ExpPointsStrategy, ConstantStrategy, PointsStrategy, FixedStrategy, LinearStrategy, BandwidthStrategy
from scripts.lib.bandwidth.lib_bandwidth_util import _append_points, calc_dev, _make_my_days
from scripts.model.Bandwidth import Bandwidth, Point

# ====================
# Strategy factory map
# ====================

STRATEGY_MAP = {
    "EXPONENTIAL": ExponentialStrategy(),
    "LIN_POINTS": LinPointsStrategy(),
    "EXP_POINTS": ExpPointsStrategy(),
    "CONSTANT": ConstantStrategy(),
    "ATTENDANCE": ConstantStrategy(),  # same behavior in original code
    "POINTS": PointsStrategy(),
    "FIXED": FixedStrategy(),
    "LINEAIR": LinearStrategy(),       # default branch
}


def _get_strategy(name: str) -> BandwidthStrategy:
    """
    Return strategy instance by name. Defaults to LinearStrategy if unknown.
    """
    return STRATEGY_MAP.get(name, STRATEGY_MAP["LINEAIR"])


# =======================
# Public builder functions
# =======================

def bandwidth_builder(assignment_group, days_in_semester: int, logger: Optional[Callable[[str], None]] = None) -> Optional[Bandwidth]:
    """
    Build Bandwidth for an assignment_group across the semester days using Strategy Pattern.

    Args:
        assignment_group: Object with properties:
            strategy, total_points, lower_points, upper_points,
            assignment_sequences (iterable with .name, .points, .get_day()).
        days_in_semester: Total number of semester days.
        logger: Optional callable for debug logging.

    Returns:
        Bandwidth or None if strategy is "NONE" or guard checks fail.
    """
    strategy_name = getattr(assignment_group, "strategy", "NONE")
    if strategy_name == "NONE":
        return None

    # Guard checks (preserved behavior)
    if assignment_group.total_points == 0:
        if logger:
            logger(f"GCS81 - ERROR Couldn't calculate bandwidth for assignment_group {assignment_group.name} total_points is zero")
        return None
    if assignment_group.lower_points == 0:
        if logger:
            logger(f"GCS82 - ERROR Couldn't calculate bandwidth for assignment_group {assignment_group.name} lower_points is zero")
        return None
    if assignment_group.upper_points == 0:
        if logger:
            logger(f"GCS83 - ERROR Couldn't calculate bandwidth for assignment_group {assignment_group.name} upper_points is zero")
        return None

    # Delegate to strategy
    print("LBI25 - strategy_name", strategy_name, assignment_group.name)
    strategy = _get_strategy(strategy_name)
    days = _make_my_days(days_in_semester)
    band_lower, band_upper = strategy.build(assignment_group, days_in_semester, days, logger)
    print("LBI27 - bandwidth.points", len(band_lower), len(band_upper), assignment_group.name)

    # Assemble Bandwidth
    points = _append_points(days, band_lower, band_upper)
    bw = Bandwidth()
    bw.days = days
    bw.lowers = band_lower
    bw.uppers = band_upper
    bw.points = points
    print("LBI29 - bandwidth.points", len(bw.points), assignment_group.name)
    return bw


def get_bandwidth_sum(course, assignment_group_ids: Iterable[int]) -> Bandwidth:
    """
    Sum multiple assignment groups' bandwidths day-by-day.
    """
    assignment_groups = [course.get_assignment_group(ag_id) for ag_id in assignment_group_ids]

    for ag in assignment_groups:
        print("LBI31 - bandwidth.points", len(ag.bandwidth.points), ag.name)
    bandwidth = Bandwidth()
    for day in range(course.days_in_semester + 1):
        new_point = Point(day, 0, 0)
        for ag in assignment_groups:
            point = ag.bandwidth.points[day]
            new_point.lower += point.lower
            new_point.upper += point.upper
        bandwidth.points.append(new_point)
    return bandwidth


def bandwidth_builder_attendance(
    a_lower_points: float,
    a_upper_points: float,
    a_total_points: float,   # unused in original, kept for signature parity
    days_in_semester: int
) -> Bandwidth:
    """
    Build a constant attendance bandwidth across the semester.

    Implemented via ConstantStrategy semantics.
    """
    # Reuse common day series
    x_time = calc_dev(days_in_semester, 0, 0, 1, 0)

    # Build lower/upper as constants with improvement tail
    band_lower = calc_dev(days_in_semester, IMPROVEMENT_PERIOD, 0, 0, a_lower_points)
    band_upper = calc_dev(days_in_semester, IMPROVEMENT_PERIOD, 0, 0, a_upper_points)

    points = _append_points(x_time, band_lower, band_upper)

    bw = Bandwidth()
    bw.days = x_time
    bw.lowers = band_lower
    bw.uppers = band_upper
    bw.points = points
    return bw
