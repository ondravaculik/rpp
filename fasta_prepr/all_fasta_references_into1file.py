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

# creating dict with all references
all_references = {}
for reference in ref_files.glob('*.fa*'):
    header = ''
    sequence = ''
    with open(reference) as f:
        ref_path = Path(reference)
        name = ref_path.stem
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i < len(lines)-1:
                if line.startswith('>'):
                    header += line.strip()
                else:
                    sequence += line.strip()
            else:
                sequence += line.strip()
                all_references[header] = sequence
    
# preparing files and folders
d = date.today().isoformat()
output_folder = Path(f'{p}', 'processed_references', f'{d}', 'all_in_one')
output_folder.mkdir(parents=True, exist_ok=True)
output_file_path = output_folder / f'all_references.fasta'

with output_file_path.open("w", encoding ="utf-8") as of:
    for header, seq in all_references.items():
        of.write(f'{header}\n')
        of.write(f'{seq}\n')