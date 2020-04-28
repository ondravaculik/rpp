import argparse
import pybedtools
import time
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('--same_strands_only', '-sso', type=bool, default=False, 
    help='Intersect only positions on the same strands? default = True')
parser.add_argument('--transcriptome', '-tr', type=str, required=True, 
    help='Path to the transcriptome bedfile')
parser.add_argument('--infile', '-in', type=str, required=True, 
    help='Path to folder with bedfiles containing binding sites positions')
parser.add_argument('--outfile', '-out', type=str, default='.', 
    help='Specify absolute or relative path to output directory, default = .')               
args = parser.parse_args()

# preparing files and folders
ts = time.time()

p = Path(args.outfile)
transcriptome_path = Path(args.transcriptome)
bed_files = Path(args.infile)

output_dir = Path(f'{p}', 'results', 'preprocessed_bedfiles', 'real_positions', f'{ts}')
output_dir.mkdir(parents=True, exist_ok=True)

# bedfiles processing
for bed_f in bed_files.glob('*.bed'):
    transcriptome = pybedtools.BedTool(transcriptome_path)
    bedfile = pybedtools.BedTool(bed_f)
    protein = Path(bed_f).stem
    output_file_name = protein + '_onlytrue.bed'
    output_file_path = output_dir / output_file_name
    
    # output processing according to same_strands_only argument
    if args.same_strands_only == True:
        bedfile.intersect(transcriptome, u=True, wa=True, s=True)\
        .saveas(output_file_path)
    else:
        bedfile.intersect(transcriptome, u=True, wa=True)\
        .saveas(output_file_path)