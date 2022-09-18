import json
from tatsu import parse

from formula_tree import FormulaTree
from path import get_alternations, crit_paths

grammar = open('./parsing/grammars/qcir-nonprenex-cleansed-closed-nnf.ebnf', 'r').read()

test_formula = '''
#QCIR-G14 7

output(g4)

g1 = and(x1, x2, z)
g2 = exists(x1, x2; g1)
g3 = or(-z, g2)
g4 = forall(z; g3)
'''

larger_test_formula = '''
#QCIR-G14 7

output(g_output)

g1 = or(z, -z)
g2 = or(y, -y)
g3 = exists(y; g2)
g4 = and(g3, g1)
g5 = or(x, -x)
g6 = forall(x; g5)
g7 = and(g6, g4)
g_output = forall(z; g7)
'''

input = open('./red_1133/axquery_axquery_1133.nonprenex.qcir').read()
ftree = FormulaTree()
ast = parse(grammar, larger_test_formula, semantics=ftree)

tree = ftree.visualize()
tree.write_svg('test.svg')
for path in (ftree.get_quant_paths()):
    print([gate.to_string() for gate in path])
    print(get_alternations(path))

for path in (crit_paths(ftree.get_quant_paths())):
    print([gate.to_string() for gate in path])