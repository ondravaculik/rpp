from pathlib import Path
from datetime import date
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--reference', '-r', type=str,
    help='Relative or absolute path to the folder containing\
    one or multiple reference fasta files', required=True)
parser.add_argument('--output_dir', '-od', type=str, help='Specify\
     working directory, where output should be placed, by either\
     relative or absolute PATH', default='.')
args = parser.parse_args()


p = Path(args.output_dir)
ref_files = Path(args.reference)

references = {}

# creating dict with all references
for reference in ref_files.glob('*.fa*'):
    chr_name = reference.stem
    chr_sequence = ''
    with open(reference, 'r') as rf:
        for line in rf.readlines():
            if line.startswith('>'):
                continue
            elif line == '':
                continue
            else:
                chr_sequence += line.strip()
    references[chr_name] = chr_sequence
    chr_sequence = ''
    
# preparing files and folders
d = date.today().isoformat()
output_folder = Path(f'{p}', 'processed_references', f'{d}', 'all_in_one')
output_folder.mkdir(parents=True, exist_ok=True)
output_file_path = output_folder / f'all_references.fasta'

with output_file_path.open("w", encoding ="utf-8") as of:
    for chr_name, chr_sequence in references.items():
        of.write(f'>{chr_name}\n')
        of.write(f'{chr_sequence}\n')