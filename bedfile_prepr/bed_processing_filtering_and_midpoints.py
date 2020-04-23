import argparse
import pybedtools
from pybedtools.featurefuncs import midpoint
from pathlib import Path


def by_chr_filtering(feature, chr_list, inverse):
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
parser.add_argument('--chromosomes', '-chr', type=str, required=True,
    help='List of chromosomes delimited by comma, which will\
         be filtered out from the bedfile')
parser.add_argument('--inverse', '-i', type=bool, default=False, 
    help='Exclude the specified chromosomes? default = False')
parser.add_argument('--score_treshold', '-sc', type=float, default=0., 
    help='Define treshold for filtering out by score, default = 0.')
parser.add_argument('--infile', '-in', type=str, required=True, 
    help='Absolute path to the bedfiles with binding sites positions')
parser.add_argument('--intermediate_out', '-int_out', type=str, default=None,
    help='Specify folder to save intermediate_outputfile\
         (filtered by chromosomes only)')
parser.add_argument('--outfile', '-out', type=str, default='.', 
    help='Specify absolute or relative path to output directory, default = .')                
args = parser.parse_args()


p = Path(args.output_file)
input_bed_files = Path(args.infile)
output_dir = Path(args.outfile)
output_dir.mkdir(parents=True, exist_ok=True)

intermediate_out = None
chr_list = args.chromosomes.split(',')

if args.inverse == False:
    if args.intermediate_out != None:
        intermediate_out = 'inversed_filtered_only_false.bed'
    final_out = 'inversed_midpoints_false.bed'
else:
    if args.intermediate_out != None:
        intermediate_out = 'inversed_filtered_only_true.bed'
    final_out = 'inversed_midpoints_true.bed'

score_treshold = args.score_treshold

if intermediate_out != None:
    intermediate_output_file_path = output_dir / f'{intermediate_out}'
else:
    intermediate_output_file_path = None

if score_treshold == 0.:
    final_output_file_path = output_dir / f'{final_out}'
else:
    final_output_file_path = output_dir / f'{final_out}_score_filtered'

for bed_f in input_bed_files.glob('*.bed'):
    bedfile = pybedtools.BedTool(bed_f)
    protein = Path(bed_f).stem
    output_file_name = protein + '_score_filtered.bed'
    output_file_path = output_dir / output_file_name

    pybedtools.BedTool(args.input_file)\
        .filter(by_chr_filtering, chr_list, args.inverse)\
        .saveas(intermediate_output_file_path)\
        .each(position for position in bedfile if float(position.score) >= score_treshold)\
        .each(midpoint)\
        .saveas(final_output_file_path)