def to_float(x):
    try:
        return float(x)
    except:
        return x


def num_cleaning(x):
    try:
        return re.match(r'[\d]*[\.\d]*', x)[0]
    except:
        return x