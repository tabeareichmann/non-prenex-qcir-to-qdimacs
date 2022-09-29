from tatsu import parse
import logging
import argparse

from parsing.formula_tree import FormulaTree
from prenexing.path_merging import simple_symbol_based_path_merging
from wklieber.wklieber_orig_tabea_style import prenex_qcir_to_qdimacs

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("input_file", type=str)
parser.add_argument("--qcir-output-file", type=str, help="output file for the prenexed formula in qcir format")
parser.add_argument("-o", type=str, dest="outfile", required=True, help="klieber output file")
parser.add_argument("--keep-var-names", choices=[0,1], type=int, default=1, dest="keep_var_names",
    help="Use VarName comment lines")
parser.add_argument("--keep-gate-names", choices=[0,1], type=int, default=0, dest="keep_gate_names")
parser.add_argument("--native-ite", choices=[0,1], type=int, default=0, dest="native_ite",
    help="Use special 4-clause encoding for XOR and ITE gates")
parser.add_argument("--reclim", type=int, default=2000, help="recursion limit " +
    "(increase this if Python dies with 'RuntimeError: maximum recursion depth exceeded')")
parser.add_argument("--fmt", type=str, help="output file format ('qcir', 'qdimacs')")
parser.add_argument("--log-level", type=int, default=logging.WARNING, help="enable logging by setting this to 20")
args = parser.parse_args()


logging.basicConfig(format='%(message)s', level=args.log_level)

grammar = open('./parsing/grammars/qcir-nonprenex-cleansed-closed-nnf.ebnf', 'r').read()

input = open(args.input_file).read()
ftree = FormulaTree()
ast = parse(grammar, input, semantics=ftree)

sk_tree = ftree.get_propositional_skeleton()

prenex_path = simple_symbol_based_path_merging(ftree)

prenexed_tree = FormulaTree.from_quant_path(prenex_path, propositional_skeleton=sk_tree)
if args.qcir_output_file:
    prenexed_tree.to_qcir_file(args.qcir_output_file)

prenex_qcir_to_qdimacs(prenexed_tree.to_qcir_string(), args)
