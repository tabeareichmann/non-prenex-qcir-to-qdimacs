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
            graph.add_edge(pydot.Edge(self._name, i._name))    

    def get_graph_label(self):
        mapping = {
            'or': '<<FONT POINT-SIZE="15">&#8744;</FONT><BR/><FONT POINT-SIZE="6">{gate_name}</FONT>>'.format(gate_name=self._name),
            'and': '<<FONT POINT-SIZE="15">&#8743;</FONT><BR/><FONT POINT-SIZE="6">{gate_name}</FONT>>'.format(gate_name=self._name),
            'forall': '<<FONT POINT-SIZE="15">&#8704;{inputs}</FONT><BR/><FONT POINT-SIZE="6">{gate_name}</FONT>>'.format(inputs=','.join(self._params), gate_name=self._name),
            'exists': '<<FONT POINT-SIZE="15">&#8707;{inputs}</FONT><BR/><FONT POINT-SIZE="6">{gate_name}</FONT>>'.format(inputs=','.join(self._params), gate_name=self._name),
        }
        return mapping[self._connective] if self._connective != None else self._name