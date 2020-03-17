import argparse
from sys import stdin, stdout
import pybedtools


parser = argparse.ArgumentParser()
parser.add_argument('--evaluation_file', '-evf', type=str, required=True,
 help='Absolute Path to bedfile with\
    experimentaly validated protein binding sites')
parser.add_argument('--model', '-m', type=str, required=True, 
    help='Name of the model')
parser.add_argument('--same_strands_only', '-sso', type=bool, default=True, 
    help='Intersect only positions on the same strands? default = True')
parser.add_argument('--input_file', '-in', type=str, required=True, 
    help='Absolute path to bedfile with protein binding sites positions')
parser.add_argument('--output_file', '-out', type=str, required=True, 
    help='Specify absolute path to output file with bed extension')               
args = parser.parse_args()


model_name = args.model
test = pybedtools.BedTool(args.evaluation_file)
pred = pybedtools.BedTool(args.input_file)

if args.same_strands_only == True:
    pred_and_test = pred.intersect(test, wa=True, s=True)
    test_and_pred = test.intersect(pred, wa=True, s=True)
else:
    pred_and_test = pred.intersect(test, wa=True)
    test_and_pred = test.intersect(pred, wa=True)

precision = pred_and_test.count() / pred.count() # BedTool.count() method
sensitivity = test_and_pred.count() / test.count()

print(f'{model_name}\t{precision}\t{sensitivity}', file=args.output_file) # just temporary solution