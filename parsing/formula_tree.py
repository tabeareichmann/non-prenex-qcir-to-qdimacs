import pydot
from gate import Gate

class FormulaTree:

    def __init__(self):
        self._output_gate = None
        self._gates = {}
        self._variables = set()

    def outputStmt(self, output_gate):
        self._output_gate = output_gate
        return output_gate

    def propGateStmt(self, ast):
        gate_name,connective,inputs = ast

        new_variables = set(self._gates).difference(set(inputs))
        self._variables = self._variables.union(new_variables)
        self._gates[gate_name] = Gate(gate_name, connective, [ self.resolve_gate(i) for i in inputs ])

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
        paths = set()
        self._output_gate.get_quant_paths(paths, tuple())
        return paths
