class Gate:

    def __init__(self, name, connective, inputs, params=[]):
        self._name = name
        self._connective = connective
        self._inputs = inputs
        self._params = params
