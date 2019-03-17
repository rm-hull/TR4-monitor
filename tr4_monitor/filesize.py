suffix = "KMGTPEZY"


def naturalsize(value, format='%.1f'):

    base = 1024
    bytes = float(value)

    if bytes == 1: 
        return '1'
    elif bytes < base: 
        return '%d' % bytes

    for i, s in enumerate(suffix):
        unit = base ** (i + 2)
        if bytes < unit:
            return (format + '%s') % ((base * bytes / unit), s)
    
    return (format + '%s') % ((base * bytes / unit), s)