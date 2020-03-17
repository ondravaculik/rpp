from pathlib import Path
import datetime
import argparse, sys


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

# preparing files and folders
dt = datetime.datetime.now().strftime("%d:%m:%Y-%H:%M")

# preparing output files and folders
output_folder = Path(f'{p}', 'results', 'preprocessed_references', f'{dt}')
output_folder.mkdir(parents=True, exist_ok=True)

# creating dict with all references
for reference in ref_files.glob('*.fa*'):
    name = ''
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

    output_file_path = output_folder / f'{name}.fasta'
    with output_file_path.open("w", encoding="utf-8") as of:
        of.write(f'>{header}\n')
        of.write(f'{sequence}')

# pass path to processed files into the stdin 
sys.stdout.write(str(output_folder))