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

def die(text): 
    sys.stderr.write("Error encountered in function '%s' at line %d:\n" % 
        (sys._getframe(1).f_code.co_name, sys._getframe(1).f_lineno))
    text = str(text)
    if (text[-1] != "\n"):
        text += "\n"
    sys.stderr.write(text + "\n")
    #stop()
    sys.exit(1)