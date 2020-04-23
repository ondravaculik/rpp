import argparse
import pybedtools
from pathlib import Path


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
    help='List of chromosomes delimited by comma, which will\
         be filtered out from the bedfile')
parser.add_argument('--inverse', '-i', type=bool, default=False, 
    help='Exclude the specified chromosomes? default = False')
parser.add_argument('--infile', '-in', type=str, required=True, 
    help='Absolute path to bedfiles with binding sites positions')
parser.add_argument('--outfile', '-out', type=str, default='.', 
    help='Specify absolute or relative path to output directory, default = .')                
args = parser.parse_args()


p = Path(args.output_file)
input_bed_files = Path(args.infile)
output_dir = Path(args.outfile)
output_dir.mkdir(parents=True, exist_ok=True)

chr_list = args.chromosomes.split(',')

if args.inverse == False:
    final_out = 'inversed_midpoints_false.bed'
else:
    final_out = 'inversed_midpoints_true.bed'

for bed_f in input_bed_files.glob('*.bed'):
    bedfile = pybedtools.BedTool(bed_f)
    protein = Path(bed_f).stem
    output_file_name = protein + '_score_filtered.bed'
    output_file_path = output_dir / output_file_name

    pybedtools.BedTool(args.infile)\
        .filter(chr_filter, chr_list, args.inverse)\
        .saveas(args.outfile)