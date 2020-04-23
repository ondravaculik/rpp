import argparse
import pybedtools
import numpy as np
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('--infile', '-in', type=str, required=True,
    help='Absolute Path to bedfiles with binding sites positions')
parser.add_argument('--reference', '-r', type=str, required=True,
    help='Absolute Path to the preprocessed fasta file containing all\
    necessary chromosomes')
parser.add_argument('--strandness', '-s', type=bool, default=True,
    help='Apply stradness? Default = True')
parser.add_argument('--format', '-f', type=bool, default=True,
    help='Choose the format of output bed file. By default (True)\
         are header and extracted sequence in tab delimited format')
parser.add_argument('--outfile', '-out', type=str, default='.',
    help='Specify absolute or relative path to output directory, default = .')                
args = parser.parse_args()


bed_files = Path(args.infile)
output_dir = Path(args.outfile)
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