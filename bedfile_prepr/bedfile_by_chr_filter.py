import argparse
import pybedtools


def chr_filter(feature, chr_list, inverse):
    """ 
    the function takes bedfile and returns new bedfile with specified chrs only 
    """  
    if args.inverse == False:
        if feature.chrom in chr_list:
            return feature
    else:
        if feature.chrom not in chr_list:
            return feature


parser = argparse.ArgumentParser()
parser.add_argument('--chromosomes', '-chr', type=str, 
    help='Delimited list of chromosomes to separate from the positions bedfile')
parser.add_argument('--inverse', '-i', type=bool, default=False, 
    help='Exclude the specified chromosomes? default = False')
parser.add_argument('--infile', '-in', type=str, required=True, 
    help='Absolute path to bedfile with protein binding sites positions or stdin by default')
parser.add_argument('--outfile', '-out', type=str, required=True, 
    help='Specify absolute path to output file with bed extension or use stdout by default')                
args = parser.parse_args()


chr_list = args.chromosomes.split(',')

pybedtools.BedTool(args.infile)\
    .filter(chr_filter, chr_list, args.inverse)\
    .saveas(args.outfile)