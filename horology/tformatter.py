from math import inf
from typing import Tuple, NamedTuple, Literal, cast

UnitType = Literal['a', 'auto', 'ns', 'us', 'ms', 's', 'min', 'h', 'd']


class Unit(NamedTuple):
    name: UnitType
    scale: float
    limit: float


UNITS = [
    Unit('ns', 10 ** -9, 10 ** -6),
    Unit('us', 10 ** -6, 10 ** -3),
    Unit('ms', 10 ** -3, 1),
    Unit('s', 1, 10 ** 3),
    Unit('min', 60, 6 * 10 ** 4),
    Unit('h', 3600, 36 * 10 ** 5),
    Unit('d', 3600 * 24, inf),
]


def rescale_time(
        interval: float,
        unit: UnitType,
) -> Tuple[float, UnitType]:
    """Rescale the time interval using the provided unit

    Parameters
    ----------
    interval
        Time interval to be rescaled, in seconds.
    unit
        Time unit to which `interval` should be rescaled. Use 'a' or
        'auto' for automatic time adjustment.

    Returns
    -------
    float
        Time interval in new units.
    str
        Convenient unit found automatically if input unit was 'auto'.
        Otherwise, provided `unit` is returned unchanged.

    Examples
    --------
    >>> rescale_time(0.421, 'us')
    (421000.0, 'us')
    >>> rescale_time(150, 'min')
    (2.5, 'min')
    >>> rescale_time(0.911, 'auto')
    (911.0, 'ms')

    Raises
    ------
    ValueError
        If the unit provided is unknown.

    """
    unit = cast(UnitType, unit.lower().strip())

    for u in UNITS:
        if unit == u.name or (unit in ('a', 'auto') and interval < u.limit):
            return interval / u.scale, u.name

    raise ValueError(f"Unknown unit: {unit}. Use one of the following: "
                     f"{[x.name for x in UNITS]} or 'auto'")
