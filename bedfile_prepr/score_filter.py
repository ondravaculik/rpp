import argparse
import pybedtools
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('--score_treshold', '-sc', type=float, default=5.5, 
    help='Absolute path to the transcriptome bedfile')
parser.add_argument('--infile', '-in', type=str, required=True, 
    help='Absolute path to folder with bedfiles containing binding sites positions')
parser.add_argument('--outfile', '-out', type=str, required=True, 
    help='Specify absolute path to output folder')               
args = parser.parse_args()


score_treshold = args.score_treshold
bed_files = Path(args.infile)
output_dir = Path(args.outfile)
output_dir.mkdir(parents=True, exist_ok=True)

for bed_f in bed_files.glob('*.bed'):
    bedfile = pybedtools.BedTool(bed_f)
    protein = Path(bed_f).stem
    output_file_name = protein + '_score_filtered.bed'
    output_file_path = output_dir / output_file_name
    
    pybedtools.BedTool(position for position in bedfile if float(position.score) >= score_treshold)\
    .saveas(output_file_path)