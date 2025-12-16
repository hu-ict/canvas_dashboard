# ======================
# Strategy abstractions
# ======================
from abc import abstractmethod, ABC
from typing import Dict, List, Optional, Callable, Tuple

# Number of days near end of semester that are excluded from certain calculations
from scripts.lib.bandwidth.lib_bandwidth_const import IMPROVEMENT_PERIOD
from scripts.lib.bandwidth.lib_bandwidth_util import _find_between, calc_interp, calc_dev, _series_from_sequences_sum


class BandwidthStrategy(ABC):
    """
    Strategy interface: compute lower/upper bands.

    Returns:
        (band_lower, band_upper) as lists aligned with x_time.
    """
    @abstractmethod
    def build(
        self,
        assignment_group,
        days_in_semester: int,
        days: List[int],
        logger: Optional[Callable[[str], None]] = None
    ) -> Tuple[List[float], List[float]]:
        ...


class LinPointsStrategy(BandwidthStrategy):
    def build(self, assignment_group, days_in_semester, days, logger=None):
        lower_b = assignment_group.lower_points / assignment_group.total_points
        upper_b = assignment_group.upper_points / assignment_group.total_points

        if logger:
            logger(f"LB02 - lower_points {assignment_group.lower_points} upper_points {assignment_group.upper_points} total_points {assignment_group.total_points}")
            logger(f"LB03 - lower a {0:5} b {lower_b:5.3} c {0:5}")
            logger(f"LB04 - upper a {0:5} b {upper_b:5.3} c {0:5}")

        series = _series_from_sequences_sum(assignment_group, days_in_semester, exclude_aanvullend=False, logger=logger)
        band_lower: List[float] = []
        band_upper: List[float] = []

        for x in days:
            x1, y1, x2, y2 = _find_between(series, "sum", x)
            # print("LBS08 -", x, x1, y1, x2, y2, x2 - x1)
            if (x2 - x1) != 0:
                y = calc_interp(x1, y1, x2, y2, x)
                band_lower.append(y * lower_b)
                band_upper.append(y * upper_b)
            else:
                band_lower.append(0)
                band_upper.append(0)
        print("LBS11 -", len(days), len(band_lower), len(band_upper))
        return band_lower, band_upper


class ExpPointsStrategy(BandwidthStrategy):
    def build(self, assignment_group, days_in_semester, days, logger=None):
        const = 6.0

        lower_c = float(assignment_group.lower_c)
        lower_b = 1.0 / const
        lower_a = (assignment_group.lower_points - lower_c - assignment_group.total_points / const) / (assignment_group.total_points * assignment_group.total_points)

        upper_c = float(assignment_group.upper_c)
        upper_b = 1.0 / const
        upper_a = (assignment_group.upper_points - upper_c - assignment_group.total_points / const) / (assignment_group.total_points * assignment_group.total_points)

        if logger:
            logger("LB61 - " + str(assignment_group))
            logger(f"LB62 - lower_points {assignment_group.lower_points} upper_points {assignment_group.upper_points} total_points {assignment_group.total_points}")
            logger(f"LB63 - lower a {lower_a:8.5} b {lower_b:5.2} c {lower_c:5.2}")
            logger(f"LB64 - upper a {upper_a:8.5} b {upper_b:5.2} c {upper_c:5.2}")

        # Build a per-day series of lower/upper from cumulative points
        series: Dict[int, Dict[str, float]] = {
            0: {"day": 0, "value_day": 0, "lower": lower_c, "upper": int(assignment_group.total_points / 30)}
        }

        total_points = 0
        lower_y = lower_c
        upper_y = upper_c

        if logger:
            logger(f"LB66 - Day points; 0; 0; 0;{lower_y:5.2f};{upper_y:5.2f}".replace('.', ','))

        series[0] = {"day": 0, "value_day": 0, "lower": lower_y, "upper": upper_y}

        for assignment_sequence in assignment_group.assignment_sequences:
            day = assignment_sequence.get_day()

            # name = getattr(assignment_sequence, "name", "")
            # if "Verbeter" in name:
            #     continue
            # if "Aanvullend" in name:
            #     continue
            if day > (days_in_semester - IMPROVEMENT_PERIOD):
                continue

            total_points += assignment_sequence.points
            lower_y = lower_a * total_points * total_points + lower_b * total_points + lower_c
            upper_y = upper_a * total_points * total_points + upper_b * total_points + upper_c

            if logger:
                out = f"LB68 - Day points; {assignment_sequence.points:2};{day:3};{total_points:>3};{lower_y:5.2f};{upper_y:5.2f}"
                logger(out.replace('.', ','))

            series[day] = {"day": day, "value_day": total_points, "lower": lower_y, "upper": upper_y}

        band_lower: List[float] = []
        band_upper: List[float] = []

        for x in days:
            x1, y1, x2, y2 = _find_between(series, "lower", x)
            y = calc_interp(x1, y1, x2, y2, x) if (x2 - x1) != 0 else y2
            band_lower.append(y)

        for x in days:
            x1, y1, x2, y2 = _find_between(series, "upper", x)
            y = calc_interp(x1, y1, x2, y2, x) if (x2 - x1) != 0 else y2
            band_upper.append(y)
        print("LBS21 -", len(days), len(band_lower), len(band_upper))
        return band_lower, band_upper


class PointsStrategy(BandwidthStrategy):
    def build(self, assignment_group, days_in_semester, days, logger=None):
        series = _series_from_sequences_sum(assignment_group, days_in_semester, exclude_aanvullend=True, logger=logger)

        lower_fraction = assignment_group.lower_points / assignment_group.total_points
        upper_fraction = assignment_group.upper_points / assignment_group.total_points

        band_lower: List[float] = []
        band_upper: List[float] = []

        for x in days:
            x1, y1, x2, y2 = _find_between(series, "sum", x)
            if (x2 - x1) != 0:
                y = calc_interp(x1, y1, x2, y2, x)
                band_lower.append(y * lower_fraction)
                band_upper.append(y * upper_fraction)
            else:
                band_lower.append(0)
                band_upper.append(0)
        print("LBS31 -", len(days), len(band_lower), len(band_upper))
        return band_lower, band_upper


class FixedStrategy(BandwidthStrategy):
    def build(self, assignment_group, days_in_semester, days, logger=None):
        # No filtering here (mirrors original FIXED)
        series: Dict[int, Dict[str, float]] = {0: {"day": 0, "sum": 0}}
        total_points = 0
        for assignment_sequence in assignment_group.assignment_sequences:
            total_points += assignment_sequence.points
            day = assignment_sequence.get_day()
            series[day] = {"day": day, "sum": total_points}

        if logger:
            logger(str(series.items()))

        band_lower: List[float] = []
        band_upper: List[float] = []

        for x in days:
            x1, y1, x2, y2 = _find_between(series, "sum", x)
            band_lower.append(y1)
            band_upper.append(assignment_group.upper_points)

        print("LBS41 -", len(days), len(band_lower), len(band_upper))
        return band_lower, band_upper


class ExponentialStrategy(BandwidthStrategy):
    def build(self, assignment_group, days_in_semester, days, logger=None):
        # Shared precomputed values
        y_start = assignment_group.upper_points / 25

        lower_a = assignment_group.lower_points / (days_in_semester - IMPROVEMENT_PERIOD) / (days_in_semester - IMPROVEMENT_PERIOD)
        band_lower = calc_dev(days_in_semester, IMPROVEMENT_PERIOD, lower_a, 0.00, 0)

        upper_a = (assignment_group.upper_points - y_start * 3) / (days_in_semester - IMPROVEMENT_PERIOD) / (days_in_semester - IMPROVEMENT_PERIOD)
        band_upper = calc_dev(days_in_semester, IMPROVEMENT_PERIOD, upper_a, 0.00, y_start * 3)
        print("LBS51 -", len(days), len(band_lower), len(band_upper))
        return band_lower, band_upper


class LinearStrategy(BandwidthStrategy):
    """
    Default fallback: 'LINEAIR' (Dutch spelling preserved).
    """
    def build(self, assignment_group, days_in_semester, days, logger=None):
        # Shared precomputed values
        y_start = assignment_group.upper_points / 25

        b_lower = (assignment_group.lower_points + y_start) / (days_in_semester - IMPROVEMENT_PERIOD)
        band_lower = calc_dev(days_in_semester, IMPROVEMENT_PERIOD, 0, b_lower, -y_start)

        b_upper = (assignment_group.upper_points - y_start) / (days_in_semester - IMPROVEMENT_PERIOD)
        band_upper = calc_dev(days_in_semester, IMPROVEMENT_PERIOD, 0, b_upper, y_start)

        print("LBS61 -", len(days), len(band_lower), len(band_upper))
        return band_lower, band_upper


class ConstantStrategy(BandwidthStrategy):
    """
    Used for both 'CONSTANT' and 'ATTENDANCE' (they are equivalent in original code).
    """
    def build(self, assignment_group, days_in_semester, days, logger=None):
        band_lower = calc_dev(days_in_semester, IMPROVEMENT_PERIOD, 0, 0, assignment_group.lower_points)
        band_upper = calc_dev(days_in_semester, IMPROVEMENT_PERIOD, 0, 0, assignment_group.upper_points)
        print("LBS71 -", len(days), len(band_lower), len(band_upper))
        return band_lower, band_upper
