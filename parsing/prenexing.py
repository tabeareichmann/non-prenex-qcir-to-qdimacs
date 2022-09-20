from path import crit_paths, longest_common_prefix, print_path, print_set_of_paths, zip_paths, split, merge

prenexing_strategies = {
    'adeu': lambda delta : 1 if delta[0]._connective == 'exists' else 0,
    'aued': lambda delta: len(delta) - 1 if delta[-1]._connective == 'exists' else len(delta),
    'edau': lambda delta: 1 if delta[0]._connective == 'forall' else 0,
    'euad': lambda delta: len(delta) - 1 if delta[-1]._connective == 'forall' else len(delta),
    'd': lambda delta: 0,
    'u': lambda delta: len(delta)
}

def simple_symbol_based_path_merging(formula_tree, strategy='d'):
    paths = formula_tree.get_quant_paths()
    if len(paths) == 0:
        return tuple()
    
    critical_paths = crit_paths(paths)
    gamma = list(critical_paths)[0]

    g = paths.copy()
    g.remove(gamma)

    while len(g) > 0:
        critical_paths_g = crit_paths(g)
        delta = list(critical_paths_g)[0]
        g.remove(delta)

        temp_gamma = split(gamma)
        temp_delta = split(delta)
        zeta = longest_common_prefix(temp_gamma, temp_delta)

        temp_gamma = merge(temp_gamma[len(zeta):])
        temp_delta = merge(temp_delta[len(zeta):])

        n = len(temp_gamma)
        m = len(temp_delta)

        if n == m and temp_gamma[0] != temp_delta[0]:
            gamma = zip_paths(temp_gamma, temp_delta, 0, len(temp_gamma))
        else:
            d = prenexing_strategies[strategy](temp_delta)
            c = m - n + 1
            gamma = zeta + zip_paths(temp_delta, temp_gamma, 0, d+1) + temp_gamma[d+1:d+c] + zip_paths(temp_gamma[d+c:], temp_delta[d+1:], 0, len(temp_gamma[d+c:]))
    return gamma
