import argparse
import pybedtools
from pybedtools.featurefuncs import midpoint


parser = argparse.ArgumentParser()
parser.add_argument('--infile', type=str, required=True,
    help='Absolute Path to bedfile with protein binding sites positions')
parser.add_argument('--outfile', type=str, required=True,
    help='Specify Path to output folder or use stdout by default')                
args = parser.parse_args()


pybedtools.BedTool(args.infile)\
    .each(midpoint)\
    .saveas(args.outfile)