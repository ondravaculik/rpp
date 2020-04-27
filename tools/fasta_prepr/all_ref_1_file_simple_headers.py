from pathlib import Path
import time
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--reference', '-r', type=str, required=True,
    help='Relative or absolute path to the folder containing\
         one or multiple reference fasta files')
parser.add_argument('--outfile', '-out', type=str, default='.',
    help='Specify absolute or relative path to output directory, default = .')
args = parser.parse_args()


p = Path(args.outfile)
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
ts = time.time()
output_folder = Path(f'{p}', 'results', 'preprocessed_references', 'all_in_one', f'{ts}')
output_folder.mkdir(parents=True, exist_ok=True)
output_file_path = output_folder / f'all_references.fasta'

with output_file_path.open("w", encoding ="utf-8") as of:
    for chr_name, chr_sequence in references.items():
        of.write(f'>{chr_name}\n')
        of.write(f'{chr_sequence}\n')