
# A tuple of tuples containing:
# ( <unit_names>, <rescale_calc>, <auto_cal> )

UNITS = (
    (('ns',), 10 ** -9, 10 ** -6),
    (('us',), 10 ** -6, 10 ** -3),
    (('ms',), 10 ** -3, 1),
    (('s',), 1,  10 ** 3),
    (('min',), 60, 6 * 10 ** 4),
    (('h', 'hs', 'hours'), 3600, 36 * 10 ** 5),
    (('d',), 3600 * 24, None)
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

    for units, calculation, _  in UNITS:
        if unit in units:
            return interval / calculation, unit
            
    raise ValueError(f"Unknown unit: {unit}. Use one of the following: {[x[0] for x in UNITS]} or 'auto'")
    

def auto_unit(interval):
    """Automatically find a unit from the interval passed. 
    
    Arguments:
        interval {float} -- Interval
    
    Returns:
        str -- String representation of the unit found.  
                Will return the 1st item in the tuple or 'd'.
    """

    for units, _, find_unit_sum in UNITS:
        if interval < find_unit_sum:
            return units[0]
    return 'd'
