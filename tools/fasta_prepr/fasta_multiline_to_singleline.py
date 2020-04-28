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


# preparing files and folders
ts = time.time()

p = Path(args.outfile)
ref_files = Path(args.reference)

output_folder = Path(f'{p}', 'results', 'preprocessed_references', f'{ts}')
output_folder.mkdir(parents=True, exist_ok=True)

# processing formated outputs
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