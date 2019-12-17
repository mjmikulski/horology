
def return_units():
    """
    Create a namedtuple of data.  Can be unpacked or accessed using dot notation.
    
    Returns:
        namedtuple -- names scale unit
    """
    from collections import namedtuple

    Unit = namedtuple('Unit', 'names scale limit')

    return (
        Unit(('ns',), 10 ** -9, 10 ** -6),
        Unit(('us',), 10 ** -6, 10 ** -3),
        Unit(('ms',), 10 ** -3, 1),
        Unit(('s',), 1,  10 ** 3),
        Unit(('min',), 60, 6 * 10 ** 4),
        Unit(('h', 'hs', 'hours'), 3600, 36 * 10 ** 5),
        Unit(('d',), 3600 * 24, None)
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

    for units, calculation, _  in return_units():
        if unit in units:
            return interval / calculation, unit
            
    raise ValueError(f"Unknown unit: {unit}. Use one of the following: {[x[0] for x in return_units()]} or 'auto'")
    

def auto_unit(interval):
    """
    Automatically find a unit from the interval passed. 
    
    Arguments:
        interval {float} -- Interval
    
    Returns:
        str -- String representation of the unit found.  
                Will return the 1st item in the tuple or 'd'.
    """

    for units, _, find_unit_sum in return_units():
        if interval < find_unit_sum:
            return units[0]
    return 'd'
