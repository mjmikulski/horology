
UNITS = (
    (('ns'), (10 ** -9)),
    (('us'), (10 ** -6)),
    (('ms'), (10 ** -3)),
    (('s'), (1)),
    (('min'), (60)),
    (('h', 'hs', 'hours'), (3600)),
    (('d'), (3600 * 24))
  )


def rescale_time(interval, unit):
    """
        Calculate and return a readable tuple from the arguments passed.
        
        Arguments:
            interval {float} -- Interval
            unit {str} -- String of Unit type.
        
        Raises:
            ValueError: Unknown unit: {unit}. Use one of the following: {[x[0] for x in UNITS]} or 'auto' 
        
        Returns:
            tuple -- interval / calculation, unit
    """
    unit = unit.lower()

    if unit in ('auto', 'a'):
        unit = auto_unit(interval)

    for units, calculation  in UNITS:
        if unit in units:
            return interval / calculation, unit
            
    raise ValueError(f"Unknown unit: {unit}. Use one of the following: {[x[0] for x in UNITS]} or 'auto'")
    

def auto_unit(interval):
    if interval < 10 ** -6:
        return 'ns'
    elif interval < 10 ** -3:
        return 'us'
    elif interval < 1:
        return 'ms'
    elif interval < 10 ** 3:
        return 's'
    elif interval < 6 * 10 ** 4:
        return 'min'
    elif interval < 36 * 10 ** 5:
        return 'h'
    else:
        return 'd'
