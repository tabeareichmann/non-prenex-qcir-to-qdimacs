from gate import Gate

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
        for variable in gate._params:
            new_path += tuple([Gate(f'{gate._name}-{variable}', gate._connective, [], params=[variable])])
    return new_path

def merge(path):
    new_path = tuple()
    for gate in path:
        if len(new_path) == 0:
            new_path += tuple([gate])
        elif new_path[-1]._connective == gate._connective:
            new_path[-1]._params.append(gate._params[0])
            new_path[-1]._name += f'-{gate._params[0]}'
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
    print(f'{name}:')
    print([gate.to_string() for gate in path]) 
    print()

def print_set_of_paths(path_set, name):
    print(f'{name}:')
    for path in path_set:
        print([gate.to_string() for gate in path])
    print()