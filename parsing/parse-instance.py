import json
from tatsu import parse

from formula_tree import FormulaTree

grammar = open('./parsing/grammars/qcir-nonprenex-cleansed-closed-nnf.ebnf', 'r').read()

test_formula = '''
#QCIR-G14 7

output(g4)

g1 = and(x1, x2, z)
g2 = exists(x1, x2; g1)
g3 = or(-z, g2)
g4 = forall(z; g3)
'''

input = open('./red_1133/axquery_axquery_1133.nonprenex.qcir').read()
ftree = FormulaTree()
ast = parse(grammar, input, semantics=ftree)

tree = ftree.visualize()
tree.write_svg('test.svg')
for path in (ftree.get_quant_paths()):
    print([gate.to_string() for gate in path])