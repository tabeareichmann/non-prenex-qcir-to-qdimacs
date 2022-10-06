import logging
from parsing.gate import Gate

def crit_paths(paths):
    mapped_paths = [(get_alternations(path),path) for path in paths]
    malt = max([t[0] for t in mapped_paths])

    crit_paths = [p[1] for p in filter(lambda path: path[0] == malt, mapped_paths)]
    return crit_paths

def get_alternations(path):
    alternations = 0
    for index in range(len(path)):
        quant_diff = index < (len(path) - 1) and (path[index]._connective != path[index + 1]._connective)
        alternations += 1 if quant_diff else 0
    return alternations

def split(path):
    new_path = tuple()
    for gate in path:
        gate._params.sort()
        for variable in gate._params:
            new_path += tuple([Gate(f'{gate._name.split("-", 1)[0]}-{variable}', gate._connective, [], params=[variable])])
    return new_path

def merge(path):
    new_path = tuple()
    for gate in path:
        if len(new_path) == 0:
            new_path += tuple([gate])
        elif new_path[-1]._connective == gate._connective:
            new_path[-1]._params += gate._params
            new_path[-1]._name = new_path[-1]._name.split("-", 1)[0] + "-" + f'{"-".join(new_path[-1]._params)}'
        else:
            new_path += tuple([gate])
    return new_path

def longest_common_prefix(path1, path2):
    prefix = tuple()
    for index in range(min(len(path1), len(path2))):
        if (path1[index] == path2[index]):
            prefix += tuple([path1[index]])
        else:
            break
    return prefix

def zip_paths(path1, path2, begin, end):
    temp = list(zip(path2, path1))[begin:end]
    new_gamma = tuple()
    for gate1, gate2 in temp:
        new_gamma += (tuple([gate1]) + tuple([gate2]))
    return new_gamma

def print_path(path, name):
    logging.info(f'{name}:\n\t{[gate.to_string() for gate in path]}')

def print_set_of_paths(path_set, name):
    "for debugging purposes only"
    logging.info(f"{name}:")
    for path in path_set:
        path_string = f"\t{', '.join([gate.to_string() for gate in path])}"
        logging.info(path_string)