from pathlib import Path
import argparse, sys
import time


parser = argparse.ArgumentParser()
parser.add_argument('--prepr_ref', '-pr', type=str,required=True,
    help='Relative or absolute path to the folder containing\
         one or multiple preprocessed reference fasta files')
parser.add_argument('--outfile', '-out', type=str, default='.',
    help='Specify absolute or relative path to output directory, default = .')
args = parser.parse_args()


ref_files = Path(args.prepr_ref)

# creating dict with all references
all_references = {}
for reference in ref_files.glob('*.fa*'):
    sequence_length = 0
    with open(reference) as f:
        ref_path = Path(reference)
        name = ref_path.stem
        for line in f.readlines():
            if line.startswith('>'):
                continue
            else:
                sequence_length += len(line.strip())
                all_references[name] = sequence_length

total_len = sum(all_references[ref] for ref in all_references)

# creating dict with the information about total length
# and proportions of individual references
ref_proportionality = {}

remainder = 1
for name, length in all_references.items():
    proportionality_of_positions = round(length/total_len, 2)
    if remainder >= proportionality_of_positions:
        remainder -= proportionality_of_positions
    else:
        proportionality_of_positions = round(remainder, 2)
        remainder -= proportionality_of_positions
    ref_proportionality[name] = proportionality_of_positions

p = Path(args.outfile)
ts = time.time()

# preparing output files and folders
output_folder = Path(f'{p}', 'results', 'preprocessed_references', 'proportions',  f'{ts}')
output_folder.mkdir(parents=True, exist_ok=True)
output_file_path = output_folder / f'references_proportions.txt'

with output_file_path.open("w", encoding ="utf-8") as of:
    of.write(f'Reference\tRef_length\tProportion\n')
    for name, proportion in ref_proportionality.items():
        reference_len = all_references[name]
        of.write(f'{name}\t{reference_len}\t{proportion}\n')