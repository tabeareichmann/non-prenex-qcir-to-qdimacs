import pydot
from parsing.gate import Gate

class FormulaTree:

    def __init__(self):
        self._output_gate = None
        self._gates = {}
        self._variables = set()

    @staticmethod
    def from_gate(gate):
        tree = FormulaTree()
        tree.outputStmt(gate)

        gate.collect_nested_vars_and_gates(tree._variables, tree._gates)
        return tree

    @staticmethod
    def from_quant_path(path, propositional_skeleton=None):
        '''
        We assume no free variables, so if there is no quantifier path, then the formula contains Verum and Falsum constants as gate inputs only.
        '''
        if not len(path):
            return propositional_skeleton

        output_gate = Gate(path[0]._name, path[0]._connective, [], params=path[0]._params)

        curr_gate = output_gate
        for g in path[1:]:
            next = Gate(g._name, g._connective, [], params=g._params)
            curr_gate._inputs = [next]
            curr_gate = next

        if propositional_skeleton != None:
            curr_gate._inputs += [propositional_skeleton._output_gate]
        
        return FormulaTree.from_gate(output_gate)

    def outputStmt(self, output_gate):
        self._output_gate = output_gate
        return output_gate

    def propGateStmt(self, ast):
        gate_name,connective,inputs = ast

        new_variables = set(self._gates).difference(set(inputs) if inputs else set())
        self._variables = self._variables.union(new_variables)
        self._gates[gate_name] = Gate(gate_name, connective, [ self.resolve_gate(i) for i in inputs ] if inputs else [])

        return ast

    def quantGateStmt(self, ast):
        gate_name,connective,bound_vars,input = ast

        self._variables = (self._variables).union(set(bound_vars))
        self._gates[gate_name] = Gate(gate_name, connective, [self.resolve_gate(input)], bound_vars)

        return ast

    def qcirFile(self, ast):
        self._output_gate = self.resolve_gate(self._output_gate)
        return ast

    def get_circuit(self):
        return self._gates[self._output_gate]
            
    def resolve_gate(self, gate_name):
        if gate_name in self._gates:
            return self._gates[gate_name]
        else:
            return Gate(gate_name, None, [])

    def visualize(self):
        graph = pydot.Dot('visualization_of_formula_tree')
        self._output_gate.visualize(graph)
        return graph

    def get_quant_paths(self):
        return self._output_gate.get_quant_paths()

    def get_propositional_skeleton(self):
        output_gate_sk = self._output_gate.get_propositional_skeleton({})
        return FormulaTree.from_gate(output_gate_sk)

    def to_qcir_string(self):
        quant_prefix_string = '#QCIR-G14'
        
        top_gate = self._output_gate
        while top_gate._connective == 'forall' or top_gate._connective == 'exists':
            top_gate_str = f"{top_gate._connective}({','.join(top_gate._params)})"
            quant_prefix_string += '\n' + top_gate_str
            top_gate = top_gate._inputs[0]
        
        output_line = f'output({top_gate._name})'

        prop_gate_lines = top_gate.to_qcir_string(set())

        return "\n".join([quant_prefix_string, output_line, prop_gate_lines])
