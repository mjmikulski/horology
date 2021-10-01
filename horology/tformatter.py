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
    """
    Rescale the time interval using the provided unit

    Parameters
    ----------
    interval: float
        Time interval to be rescaled, in seconds.
    unit: {'auto', 'ns', 'us', 'ms', 's', 'min', 'h', 'd'}
        Time unit to which `interval` should be rescaled. Use 'a' or
        'auto' for automatic time adjustment.

    Returns
    -------
    rescaled_interval: float
        Time interval in new units.
    unit:
        Convenient unit found automatically if input unit was 'auto'.
        Otherwise `unit` is returned unchanged.


    Examples
    --------
        >>> rescale_time(0.421, 'us')
        (421000.0, 'us')
        >>> rescale_time(150, 'min')
        (2.5, 'min')
        >>> rescale_time(0.911, 'auto')
        (911.0, 'ms')

    # Raises
        ValueError: when the unit provided is unknown

    """
    unit = unit.lower().strip()

    if unit in ('auto', 'a'):
        unit = auto_unit(interval)

    for names, scale, _ in UNITS:
        if unit in names:
            return interval / scale, unit

    raise ValueError(f"Unknown unit: {unit}. Use one of the following: {[x[0] for x in UNITS]} or 'auto'")


def auto_unit(interval: float):
    """
    Automatically finds a time unit that is convenient for the time scale of
    the interval

    # Arguments
        interval: time interval

    # Returns
        String representation of the suitable time unit.

    # Example
        >>> auto_unit(0.123)
        'ms'
        >>> auto_unit(1234)
        'min'
    """

    for names, _, limit in UNITS:
        if interval < limit:
            return names[0]
