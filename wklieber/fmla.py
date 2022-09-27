class Fmla(tuple):
    id_cache = {}
    idx = {}
    next_idx = 1
    rev_hash = {}
    hash = {}

    def __eq__(self, other): return (self is other)
    def __ne__(self, other): return not(self is other)

    __hash__ = object.__hash__

    def __new__(cls, *args):
        ret = Fmla.id_cache.get(args, None)
        if (ret is None):
            ret = tuple.__new__(Fmla, args)
            if args[0] == 'xor': assert(len(args[1:]) == 2)
            if args[0] == 'ite': assert(len(args[1:]) == 3)
            Fmla.id_cache[args] = ret
            assert(ret not in Fmla.idx)
            Fmla.idx[ret] = Fmla.next_idx
            Fmla.next_idx += 1
        return ret
