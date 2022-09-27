from tatsu import parse
import logging

from parsing.formula_tree import FormulaTree
from prenexing.path_merging import simple_symbol_based_path_merging
from wklieber.wklieber_orig_tabea_style import prenex_qcir_to_qdimacs

logging.basicConfig(format='%(message)s', level=logging.INFO)

grammar = open('./parsing/grammars/qcir-nonprenex-cleansed-closed-nnf.ebnf', 'r').read()

input = open('./test_formulas/test1.qcir').read()
ftree = FormulaTree()
ast = parse(grammar, input, semantics=ftree)

sk_tree = ftree.get_propositional_skeleton()

prenex_path = simple_symbol_based_path_merging(ftree)

prenexed_tree = FormulaTree.from_quant_path(prenex_path, propositional_skeleton=sk_tree)

prenex_qcir_to_qdimacs(prenexed_tree.to_qcir_string())
