import logging
from prenexing.path import crit_paths, longest_common_prefix, print_path, print_set_of_paths, zip_paths, split, merge

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
    i = 0
    while len(g) > 0:
        i += 1
        logging.info(f'Iteration: {i}')
        critical_paths_g = crit_paths(g)
        delta = list(critical_paths_g)[0]
        print_path(delta, "delta")
        g.remove(delta)

        temp_gamma = split(gamma)
        temp_delta = split(delta)
        zeta = longest_common_prefix(temp_gamma, temp_delta)
        print_path(zeta, "zeta")

        temp_gamma = merge(temp_gamma[len(zeta):])
        temp_delta = merge(temp_delta[len(zeta):])

        
        print_path(temp_gamma, "temp_gamma")
        print_path(temp_delta, "temp_delta")

        n = len(temp_gamma)
        m = len(temp_delta)

        if n == m and temp_gamma[0] != temp_delta[0]:
            gamma = merge(zeta + zip_paths(temp_gamma, temp_delta, 0, len(temp_gamma)))
        else:
            d = prenexing_strategies[strategy](temp_delta)
            c = n - m + 1
            gamma = merge(zeta + zip_paths(temp_delta, temp_gamma, 0, d) + temp_gamma[d:d+c-1] + zip_paths(temp_gamma[d+c-1:], temp_delta[d:], 0, len(temp_gamma[d+c-1:])))
            print_path(gamma, "Gamma in iteration "+str(i))
    return gamma