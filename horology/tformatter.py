
UNITS = {
    'ns': 10 ** -9,
    'us': 10 ** -6,
    'ms': 10 ** -3,
    's': 1,
    'min': 60,
    'h': 3600,
    'd': 3600 * 24
}  # todo: allow alternatives, eg. h == hs == hours


def rescale_time(t, unit):
    unit = unit.lower()
    if unit in ('auto', 'a'):
        unit = auto_unit(t)
    if unit not in UNITS.keys():
        raise ValueError(f"Unknown unit: {unit}. Use one od those: {UNITS.keys()} or 'auto'")

    return t / UNITS[unit], unit


def auto_unit(t):
    if t < 10 ** -6:
        return 'ns'
    if t < 10 ** -3:
        return 'us'
    if t < 1:
        return 'ms'
    if t < 10 ** 3:
        return 's'
    if t < 6 * 10 ** 4:
        return 'min'
    if t < 36 * 10 ** 5:
        return 'h'

    return 'd'
