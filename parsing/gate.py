import pydot

class Gate:

    def __init__(self, name, connective, inputs, params=[]):
        self._name = name
        self._connective = connective
        self._inputs = inputs
        self._params = params

    def visualize(self, graph):
        graph.add_node(pydot.Node(self._name, label=self.get_graph_label()))
        
        for i in self._inputs:
            i.visualize(graph)
            
            edge_exists = len(graph.get_edge(self._name, i._name))
            if not edge_exists:
                graph.add_edge(pydot.Edge(self._name, i._name))    

    def get_graph_label(self):
        mapping = {
            'or': '<<FONT POINT-SIZE="15">&#8744;</FONT><BR/><FONT POINT-SIZE="6">{gate_name}</FONT>>'.format(gate_name=self._name),
            'and': '<<FONT POINT-SIZE="15">&#8743;</FONT><BR/><FONT POINT-SIZE="6">{gate_name}</FONT>>'.format(gate_name=self._name),
            'forall': '<<FONT POINT-SIZE="15">&#8704;{inputs}</FONT><BR/><FONT POINT-SIZE="6">{gate_name}</FONT>>'.format(inputs=','.join(self._params), gate_name=self._name),
            'exists': '<<FONT POINT-SIZE="15">&#8707;{inputs}</FONT><BR/><FONT POINT-SIZE="6">{gate_name}</FONT>>'.format(inputs=','.join(self._params), gate_name=self._name),
        }
        return mapping[self._connective] if self._connective != None else self._name

    def to_string(self):
        return f'{self._name}:{self._connective} {", ".join(self._params)}'

    def get_quant_paths(self):
        if len(self._inputs) == 0:
            return set()
        if self._connective == 'forall' or self._connective == 'exists':
            child_paths = self._inputs[0].get_quant_paths()
            if (len(child_paths) == 0):
                result = set()
                result.add(tuple([self]))
                return result
            else:
                return { tuple([self]) + path for path in child_paths }
        elif self._connective == 'or' or self._connective == 'and':
            child_paths = [ i.get_quant_paths() for i in self._inputs ]
            union = set().union(*child_paths)
            return union

    def get_propositional_skeleton(self):
        if self._connective == 'forall' or self._connective == 'exists':
            return self._inputs[0].get_propositional_skeleton()
        else:
            sk_inputs = [i.get_propositional_skeleton() for i in self._inputs]
            return Gate(self._name, self._connective, sk_inputs, params=self._params)

    def collect_nested_vars_and_gates(self, vars, gates):
        vars = vars.union(self._name)
        gates[self._name] = self

        for input in self._inputs:
            input.collect_nested_vars_and_gates(vars, gates)

    def to_qcir_string(self):
        if len(self._inputs) == 0:
            return ''

        own_qcir_def = f"{self._name} = {self._connective}({', '.join([i._name for i in self._inputs])})"
        child_qcir_def = '\n'.join(filter(lambda s: len(s) > 0, [i.to_qcir_string() for i in self._inputs]))
        return child_qcir_def + ('\n' if len(child_qcir_def) > 0 else '') + own_qcir_def

    def __eq__(self, obj):
        self._params.sort()
        obj._params.sort()
        return self._connective == obj._connective and self._params == obj._params

    def __hash__(self):
        self._params.sort()
        return hash(self._connective + ''.join(self._params))
