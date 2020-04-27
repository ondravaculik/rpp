import argparse
import pybedtools
import time
from pybedtools.featurefuncs import midpoint
from pathlib import Path


def by_chr_filtering(feature, chr_list, inverse):
    """ 
    the function takes bedfile and returns new bedfile with specified chrs only 
    """  
    if chr_list == []:
        return feature
    else:
        if args.inverse == False:
            if feature.chrom in chr_list:
                return feature
        else:
            if feature.chrom not in chr_list:
                return feature


def score_filtering(feature, score_treshold):
    """
    the function returns only positions with score equal or higher than specified threshold
    """
    if float(feature.score) >= score_treshold:
        return feature


parser = argparse.ArgumentParser()
parser.add_argument('--chromosomes', '-chr', type=str, default='',
    help='Optional list of chromosomes delimited by comma, which will\
         be filtered out from the bedfile')
parser.add_argument('--inverse', '-i', type=bool, default=False, 
    help='Exclude the specified chromosomes? default = False')
parser.add_argument('--midpoints', '-mid', type=bool, default=False,
    help='Processed intervals into midpoints? default = False')
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


p = Path(args.outfile)
input_bed_files = Path(args.infile)

ts = time.time()

# preparing output files and folders
output_dir = Path(f'{p}', 'results', 'preprocessed_bedfiles', 'filtered_by_score_midpoints', f'{ts}')
output_dir.mkdir(parents=True, exist_ok=True)

intermediate_out = None
inverse = args.inverse 
midpoint_arg = args.midpoints

if midpoint_arg == True:
    is_midpoint = '_midpoints'
else:
    is_midpoint = ''

if args.chromosomes == '':
    chr_list = []
else:
    chr_list = args.chromosomes.split(',')

if chr_list != []:
    if inverse == False:
        if args.intermediate_out != None:
            intermediate_out = 'inversed_false_filtered_only_true'
        final_out = f'_inversed_false_filtered_by_chr{is_midpoint}'
    else:
        if args.intermediate_out != None:
            intermediate_out = 'inversed_true_filtered_only_true'
        final_out = f'_inversed_true_filtered_by_chr{is_midpoint}'
else:
    intermediate_out = None
    final_out = f'{is_midpoint}'

score_treshold = args.score_treshold

for bed_f in input_bed_files.glob('*.bed'):
    protein = Path(bed_f).stem

    if intermediate_out != None:
        intermediate_output_file_path = output_dir / f'{protein}_{intermediate_out}.bed'
    else:
        intermediate_output_file_path = None

    if score_treshold == 0.:
        final_output_file_path = output_dir / f'{protein}{final_out}.bed'
    else:
        final_output_file_path = output_dir / f'{protein}{final_out}_score_filtered.bed'

    bedfile = pybedtools.BedTool(bed_f)

    bedfile.filter(by_chr_filtering, chr_list, inverse)\
        .saveas(intermediate_output_file_path)

    if midpoint_arg == True:
        bedfile.each(midpoint)
    else:
        pass

    bedfile.filter(score_filtering, score_treshold)\
        .saveas(final_output_file_path)