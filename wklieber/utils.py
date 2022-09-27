class DeadExc(Exception):
    pass

def flatten(L):
    return (item for sublist in L for item in sublist)

def unique(coll):
    hit = set()
    for x in coll:
        if x in hit:
            continue
        hit.add(x)
        yield x

def negate(fmla):
    if is_lit(fmla):
        return -fmla
    if isinstance(fmla, tuple) and fmla[0] == 'not':
        return fmla[1]
    else:
        assert(isinstance(fmla, tuple))
        return Fmla('not', fmla)

def is_lit(x):
    # Returns true if this a literal (as opposed to a formula with logical operators).
    return type(x) == int

def die(text): 
    sys.stderr.write("Error encountered in function '%s' at line %d:\n" % 
        (sys._getframe(1).f_code.co_name, sys._getframe(1).f_lineno))
    text = str(text)
    if (text[-1] != "\n"):
        text += "\n"
    sys.stderr.write(text + "\n")
    #stop()
    sys.exit(1)