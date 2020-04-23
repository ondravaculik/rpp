import argparse
import pybedtools


parser = argparse.ArgumentParser()
parser.add_argument('--infile', '-in', type=str, 
    help='Absolute path to textfile containing positions')
parser.add_argument('--outfile', '-out', type=str, required=True, 
    help='Specify absolute path to output file with bed extension')                
args = parser.parse_args()


pybedtools.BedTool(args.infile)\
    .saveas(args.outfile)