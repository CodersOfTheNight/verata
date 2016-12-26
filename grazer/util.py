def time_convert(span):
    time_char = span[-1]
    val = span[:-1]
    if time_char == "s":
        return int(val)
    elif time_char == "m":
        return int(val) * 60
    elif time_char == "h":
        return int(val) * 3600
    else:
        raise RuntimeError("Unknown time format char: '{0}'".format(time_char))
