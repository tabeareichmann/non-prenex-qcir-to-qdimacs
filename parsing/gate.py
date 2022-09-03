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
            'or': '∨',
            'and': '∧',
            'forall': '∀{inputs}'.format(inputs=','.join(self._params)),
            'exists': '∃{inputs}'.format(inputs=','.join(self._params)),
        }
        return mapping[self._connective] if self._connective != None else self._name