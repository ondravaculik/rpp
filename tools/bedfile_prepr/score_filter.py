import argparse
import pybedtools
import time
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('--score_treshold', '-sc', type=float, default=6., 
    help='Define treshold for filtering out by score, default = 6.')
parser.add_argument('--infile', '-in', type=str, required=True, 
    help='Absolute path to the bedfiles with binding sites positions')
parser.add_argument('--outfile', '-out', type=str, default='.', 
    help='Specify absolute or relative path to output directory, default = .')               
args = parser.parse_args()

# preparing files and folders
ts = time.time()

p = Path(args.outfile)
score_treshold = args.score_treshold
bed_files = Path(args.infile)

output_dir = Path(f'{p}', 'results', 'preprocessed_bedfiles', 'filtered_by_score', f'{ts}')
output_dir.mkdir(parents=True, exist_ok=True)

# bedfiles processing
for bed_f in bed_files.glob('*.bed'):
    bedfile = pybedtools.BedTool(bed_f)
    protein = Path(bed_f).stem
    output_file_name = protein + '_score_filtered.bed'
    output_file_path = output_dir / output_file_name
    
    pybedtools.BedTool(position for position in bedfile\
        if float(position.score) >= score_treshold)\
    .saveas(output_file_path)