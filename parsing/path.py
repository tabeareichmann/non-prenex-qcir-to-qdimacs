def crit_paths(paths):
    mapped_paths = [(get_alternations(path),path) for path in paths]
    malt = max([t[0] for t in mapped_paths])
    print(malt)

    crit_paths = [p[1] for p in filter(lambda path: path[0] == malt, mapped_paths)]
    return crit_paths

def get_alternations(path):
    alternations = 0
    for index in range(len(path)):
        quant_diff = index < (len(path) - 1) and (path[index]._connective != path[index + 1]._connective)
        alternations += 1 if quant_diff else 0
    return alternations