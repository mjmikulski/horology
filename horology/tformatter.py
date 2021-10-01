from collections import namedtuple
from math import inf

Unit = namedtuple('Unit', 'names scale limit')

UNITS = [
    Unit(('ns',), 10 ** -9, 10 ** -6),
    Unit(('us',), 10 ** -6, 10 ** -3),
    Unit(('ms',), 10 ** -3, 1),
    Unit(('s',), 1, 10 ** 3),
    Unit(('min',), 60, 6 * 10 ** 4),
    Unit(('h', 'hs', 'hours'), 3600, 36 * 10 ** 5),
    Unit(('d', 'day', 'days'), 3600 * 24, inf)]


def rescale_time(interval: float, unit: str):
    """Rescale the time interval using the provided unit

    Parameters
    ----------
    interval: float
        Time interval to be rescaled, in seconds.
    unit: {'auto', 'ns', 'us', 'ms', 's', 'min', 'h', 'd'}
        Time unit to which `interval` should be rescaled. Use 'a' or
        'auto' for automatic time adjustment.

    Returns
    -------
    float
        Time interval in new units.
    str
        Convenient unit found automatically if input unit was 'auto'.
        Otherwise provided `unit` is returned unchanged.

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
    unit = unit.lower().strip()

    for u in UNITS:
        if unit in u.names or (unit in ('auto', 'a') and interval < u.limit):
            return interval / u.scale, u.names[0]

    raise ValueError(f"Unknown unit: {unit}. Use one of the following: "
                     f"{[x.names[0] for x in UNITS]} or 'auto'")
