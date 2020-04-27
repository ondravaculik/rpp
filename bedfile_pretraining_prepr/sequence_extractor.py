import argparse
import pybedtools
import numpy as np
import time
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('--infile', '-in', type=str, required=True,
    help='Absolute Path to bedfiles with binding sites positions')
parser.add_argument('--reference', '-r', type=str, required=True,
    help='Absolute Path to the preprocessed fasta file containing all\
    necessary chromosomes')
parser.add_argument('--strandness', '-s', type=bool, default=False,
    help='Apply stradness? Default = False')
parser.add_argument('--format', '-f', type=bool, default=False,
    help='Choose the format of output bed file. By default (False)\
         are header and extracted sequence on separate lines\
         True is tab delimited format')
parser.add_argument('--outfile', '-out', type=str, default='.',
    help='Specify absolute or relative path to output directory, default = .')                
args = parser.parse_args()

p = Path(args.outfile)
bed_files = Path(args.infile)

ts = time.time()

# preparing output files and folders
output_dir = Path(f'{p}', 'results', 'preprocessed_bedfiles', 'extracted_sequences', f'{ts}')
output_dir.mkdir(parents=True, exist_ok=True)

fasta = args.reference
strandness = args.strandness
output_format = args.format

for bedfile in bed_files.glob('*.bed'):
    bed_path = Path(bedfile)
    output_file_name = bed_path.stem + f'_with_sequences.bed'
    output_file_path = output_dir / output_file_name

    pybedtools.BedTool(bedfile)\
        .sequence(fi=fasta, s=strandness, tab=output_format)\
        .save_seqs(output_file_path)