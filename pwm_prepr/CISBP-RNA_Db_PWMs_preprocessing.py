from pathlib import Path
import argparse
import numpy as np
import datetime


parser = argparse.ArgumentParser()
parser.add_argument('--ppm_directory', '-ppmd', type=str,
    help='Relative or absolute path to the folder\
         containing one or multiple PPMs', required=True)
parser.add_argument('--outfile', '-out', type=str, default='.',
    help='Specify absolute or relative path to output directory, default = .')
args = parser.parse_args()


p = Path(args.outfile)
ppm_files = Path(args.ppm_directory)

# creating dict of np.arrays with all users PPMs
# extracting protein_name from the name of PPM file
all_ppms = {}
for ppm in ppm_files.glob('*.txt'):
    name = ''
    with open(ppm) as f:
        current_ppm = []

        file_name = Path(ppm).stem
        try: 
            index = file_name.index('.')
        except ValueError: 
            index = len(file_name)
        protein_name = file_name[0:index]

        lines = f.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                continue
            else:
                if line == '':
                    continue
                else:
                    ppm_part = [float(pos) for pos in line.strip().split()[1:]]
                    current_ppm.append(ppm_part)    
        all_ppms[protein_name] = np.asarray(current_ppm)

dt = datetime.datetime.now().strftime("%d:%m:%Y-%H:%M")

# preparing output files and folders
output_folder = Path(f'{p}', 'results', 'preprocessed_pwms', f'{dt}')
output_folder.mkdir(parents=True, exist_ok=True)

# creating output file
for protein_name, matrix in all_ppms.items():
    output_file = f'{protein_name}'
    output_file_path = output_folder / output_file
    np.save(output_file_path, matrix)