from typing import Optional, List
import math


def normalize_angle(angle: float) -> float:
    new_angle = angle

    while new_angle <= -math.pi:
        new_angle += 2 * math.pi

    while new_angle > math.pi:
        new_angle -= 2 * math.pi

    return new_angle


def degrees_to_radians(degrees: Optional[float]) -> Optional[float]:
    if degrees is None:
        return None

    return math.radians(degrees)


def radians_to_degrees(radians: Optional[float]) -> Optional[float]:
    if radians is None:
        return None

    return math.degrees(radians)


def degrees_to_counts(degrees: Optional[float], counts_per_revolution: float) -> Optional[float]:
    if degrees is None:
        return None

    return (degrees / 360) * counts_per_revolution


def counts_to_degrees(counts: Optional[float], counts_per_revolution: float, sign: int=1) -> Optional[float]:
    if counts is None:
        return None

    return (counts / counts_per_revolution) * 360.0 * sign


def counts_to_radians(counts: Optional[float], counts_per_revolution: float, sign: int=1) -> Optional[float]:
    if counts is None:
        return None

    return (counts / counts_per_revolution) * 2 * math.pi * sign


def radians_to_counts(radians: Optional[float], counts_per_revolution: float) -> Optional[float]:
    if radians is None:
        return None

    return (float(radians) / (2 * math.pi)) * counts_per_revolution


def cps_to_rpm(counts_per_second: Optional[float], counts_per_revolution: float) -> Optional[float]:
    if counts_per_second is None:
        return None

    return (float(counts_per_second) * 60) / counts_per_revolution


def rpm_to_cps(rpm: Optional[float], counts_per_revolution: float) -> Optional[float]:
    if rpm is None:
        return None

    return (float(rpm) / 60) * counts_per_revolution


def mm_to_counts(mm: Optional[float], counts_per_mm: float) -> Optional[float]:
    if mm is None:
        return None

    return mm * counts_per_mm


def counts_to_mm(counts: Optional[float], counts_per_mm: float) -> Optional[float]:
    if counts is None:
        return None

    return counts / counts_per_mm


def ml_to_counts(ml: Optional[float], counts_per_ml: float) -> Optional[float]:
    if ml is None:
        return None

    return ml * counts_per_ml


def counts_to_ml(counts: Optional[float], counts_per_ml: float) -> Optional[float]:
    if counts is None:
        return None

    return counts / counts_per_ml


def within_range(value, range_list: List):
    a, b = range_list
    return a <= value <= b


def sign(value: float) -> float:
    if value < 0:
        return -1.0

    return 1.0


def velocity_sign(start_velocity: float, end_velocity: float) -> int:
    if start_velocity > end_velocity:
        return -1

    if start_velocity < end_velocity:
        return 1

    return 0


def acceleration(start_velocity: float, end_velocity: float, distance: float) -> float:
    return math.fabs(float(end_velocity ** 2 - start_velocity ** 2) / (2 * distance))


def distance(start_velocity: float, end_velocity: float, acceleration: float) -> float:
    return math.fabs(float(end_velocity ** 2 - start_velocity ** 2) / (2 * acceleration))


def end_velocity(start_velocity: float, acceleration: float, distance: float) -> float:
    velocity_squared = start_velocity**2 + 2 * acceleration * distance
    return math.sqrt(math.fabs(velocity_squared)) * sign(velocity_squared)


def start_velocity(end_velocity: float, acceleration: float, distance: float) -> float:
    velocity_squared = end_velocity ** 2 + 2 * acceleration * distance
    return math.sqrt(math.fabs(velocity_squared)) * sign(velocity_squared)


def acceleration_time(start_velocity: float, end_velocity: float, acceleration: float) -> float:
    return float(end_velocity - start_velocity) / acceleration

