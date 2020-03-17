import argparse
import pybedtools
import datetime
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

# přidat ještě argument, že si user bude moct zvolit, zda chce i filtrovat podle score treshold

parser = argparse.ArgumentParser()
parser.add_argument('--chromosomes', '-chr', type=str, required=True,
    help='List of chromosomes delimited by comma, which will be filtered from the positions bedfile')
parser.add_argument('--inverse', '-i', type=bool, default=False, 
    help='Exclude the specified chromosomes? default = False')
parser.add_argument('--input_file', '-in', type=str, required=True, 
    help='Absolute path to bedfile with protein binding sites positions')
parser.add_argument('--intermediate_output', '-int_out', type=str, default=None,
    help='Specify folder to save intermediate_outputfile (filtered by chromosomes only)')
parser.add_argument('--output_file', '-out', type=str, required=True, 
    help='Specify folder to save the output bedfile')                
args = parser.parse_args()

chr_list = args.chromosomes.split(',')

p = Path(args.output_file)
dt = datetime.datetime.now().strftime("%d:%m:%Y-%H:%M")

intermediate_out = None

if args.inverse == False:
    if args.intermediate_output != None:
        intermediate_out = 'inversed_filtered_only_false.bed'
    final_out = 'inversed_midpoints_false.bed'
else:
    if args.intermediate_output != None:
        intermediate_out = 'inversed_filtered_only_true.bed'
    final_out = 'inversed_midpoints_true.bed'

# preparing output files and folders
output_folder = Path(f'{p}', 'results', 'preprocessed_bedfiles', f'{dt}')
output_folder.mkdir(parents=True, exist_ok=True)
if intermediate_out != None:
    intermediate_output_file_path = output_folder / f'{intermediate_out}'
else:
    intermediate_output_file_path = None
final_output_file_path = output_folder / f'{final_out}'

pybedtools.BedTool(args.input_file)\
    .filter(by_chr_filtering, chr_list, args.inverse)\
    .saveas(intermediate_output_file_path)\
    .each(midpoint)\
    .saveas(final_output_file_path)