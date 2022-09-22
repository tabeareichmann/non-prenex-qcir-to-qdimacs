from tatsu import parse

from formula_tree import FormulaTree
from path import get_alternations, crit_paths
from prenexing import simple_symbol_based_path_merging

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

input = open('./test_formulas/test1.qcir').read()
ftree = FormulaTree()
ast = parse(grammar, input, semantics=ftree)

sk_tree = ftree.get_propositional_skeleton()
vtree = sk_tree.visualize()
vtree.write_svg('test1_sk.svg')

prenex_path = simple_symbol_based_path_merging(ftree)

path_tree = FormulaTree.from_quant_path(prenex_path)
path_vtree = path_tree.visualize()
path_vtree.write_svg('test1_prenex_path.svg')

prenexed_tree = FormulaTree.from_quant_path(prenex_path, propositional_skeleton=sk_tree)
prenexed_vtree = prenexed_tree.visualize()
prenexed_vtree.write_svg('test1_prenexed.svg')
