from wklieber.fmla import Fmla
from wklieber.utils import flatten, unique, negate, is_lit, die, DeadExc

@memoized
def simplify(fmla):
    Fmla_True = Fmla(True)
    Fmla_False = Fmla(False)

    if is_lit(fmla):
        return fmla
    (op, args) = (fmla[0], fmla[1:])
    if fmla in [Fmla_True, Fmla_False]:
        return fmla
    args = [simplify(arg) for arg in args]

    if op in ('and', 'or'):
        if op == 'and':  (base, negbase) = (Fmla_True, Fmla_False)
        elif op == 'or': (base, negbase) = (Fmla_False, Fmla_True)
        def expand_arg(arg):
            if arg == base:
                return ()
            if arg == negbase:
                raise DeadExc
            else:
                return (arg,)
        ret = None
        try:
            args = tuple(flatten([expand_arg(a) for a in args]))
        except DeadExc:
            ret = negbase
        if ret == None:
            if   len(args) == 0:  ret = base
            elif len(args) == 1:  ret = args[0]
            else:
                ret = Fmla(op, *unique(args))
                if len(args) > 6:
                    arg_coll = set(args)
                else:
                    arg_coll = args
                for arg in args:
                    if negate(arg) in arg_coll:
                        ret = negbase
    elif op == 'not':
        if   args[0] == Fmla_True:  ret = Fmla_False
        elif args[0] == Fmla_False: ret = Fmla_True
        else: ret = Fmla(op, *args)
    elif op == 'xor':
        assert(len(args) == 2)
        if args[1] in (Fmla_True, Fmla_False):
            args = [args[1], args[0]]
        #
        if args[0] == Fmla_False:
            ret = args[1]
        elif args[0] == Fmla_True:
            ret = negate(args[1])
        else:
            ret = Fmla(op, *args)
    elif op == 'ite':
        (test, tbra, fbra) = args
        if   test == Fmla_True:    ret = tbra
        elif test == Fmla_False:   ret = fbra
        elif tbra == Fmla_True:    ret = simplify(Fmla('or',  test,         fbra))
        elif fbra == Fmla_True:    ret = simplify(Fmla('or',  negate(test), tbra))
        elif tbra == Fmla_False:   ret = simplify(Fmla('and', negate(test), fbra))
        elif fbra == Fmla_False:   ret = simplify(Fmla('and', test,         tbra))
        else: ret = Fmla(op, *args)
    else:
        die("Unknown operator: '%s'\n" % op)
    return ret

@memoized
def to_andor(fmla):
    if is_lit(fmla):
        return fmla
    (op, args) = (fmla[0], fmla[1:])
    if len(args) == 0:
        return fmla
    args = [to_andor(arg) for arg in args]
    if op in ('and', 'or', 'not'):
        ret = Fmla(op, *args)
    elif op == 'xor':
        ret = to_andor(Fmla('ite', args[0], negate(args[1]), args[1]))
    elif op == 'ite':
        (sel, y, z) = args
        ret = Fmla('and', Fmla('or', negate(sel), y), Fmla('or', sel, z))
    else:
        die("Unknown operator: '%s'\n" % op)
    return ret

def qcir_to_qdimacs(fmla):
    return simplify(to_andor(fmla))