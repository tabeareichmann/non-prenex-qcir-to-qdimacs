import json
from tatsu import parse

from formula_tree import FormulaTree

grammar = open('./parsing/grammars/qcir-nonprenex-cleansed-closed-nnf.ebnf', 'r').read()

test_formula = '''
#QCIR-G14 7

output(g4)

g1 = and(x1, x2, z)
g2 = exists(x1, x2; g1)
g3 = or(z, -g2)
g4 = forall(z; g3)
'''

ftree = FormulaTree()
ast = parse(grammar, test_formula, semantics=ftree)