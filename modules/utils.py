
def lazyInt(input, default=-1):
    try:
        return int(input)
    except:
        return default
