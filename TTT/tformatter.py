UNITS = {
    'ns': 10 ** 9,
    'us': 10 ** 6,
    'ms': 10 ** 3,
    's': 1,
    'min': 1 / 60,
    'h': 1 / 3600,
    'd': 1 / (3600 * 24)
}


def format(t, unit: str = 's'):
    unit = unit.lower()
    if unit not in UNITS.keys():
        raise ValueError(f"Unknown unit: {unit}. Use one od those: {UNITS.keys()}")

    return t * UNITS[unit], unit
