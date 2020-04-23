import argparse
import pybedtools
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('--same_strands_only', '-sso', type=bool, default=True, 
    help='Intersect only positions on the same strands? default = True')
parser.add_argument('--transcriptome', '-tr', type=str, required=True, 
    help='Absolute path to the transcriptome bedfile')
parser.add_argument('--infile', '-in', type=str, required=True, 
    help='Absolute path to folder with bedfiles containing binding sites positions')
parser.add_argument('--outfile', '-out', type=str, default='.', 
    help='Specify absolute path to output directory')               
args = parser.parse_args()


transcriptome_path = Path(args.transcriptome)
bed_files = Path(args.infile)
output_dir = Path(args.outfile)
output_dir.mkdir(parents=True, exist_ok=True)

for bed_f in bed_files.glob('*.bed'):
    transcriptome = pybedtools.BedTool(transcriptome_path)
    bedfile = pybedtools.BedTool(bed_f)
    protein = Path(bed_f).stem
    output_file_name = protein + '_onlytrue.bed'
    output_file_path = output_dir / output_file_name
    
    if args.same_strands_only == True:
        bedfile.intersect(transcriptome, u=True, wa=True, s=True)\
        .saveas(output_file_path)
    else:
        bedfile.intersect(transcriptome, u=True, wa=True)\
        .saveas(output_file_path)