from pathlib import Path
import argparse
import numpy as np
import time


parser = argparse.ArgumentParser()
parser.add_argument('--pwm_directory', '-pwmd', type=str, required=True,
    help='Relative or absolute path to the folder\
         containing one or multiple PWMs')
parser.add_argument('--outfile', '-out', type=str, default='.',
    help='Specify absolute or relative path to output directory, default = .')
args = parser.parse_args()


# preparing files and folders
ts = time.time()

p = Path(args.outfile)
pwm_files = Path(args.pwm_directory)

output_folder = Path(f'{p}', 'results', 'preprocessed_pwms', 'real', f'{ts}')
output_folder.mkdir(parents=True, exist_ok=True)

# creating dict of np.arrays with all users PWMs
# extracting protein_name from the name of PWM file
all_ppms = {}
for pwm in pwm_files.glob('*.txt'):
    name = ''
    with open(pwm) as f:
        current_ppm = []

        file_name = Path(pwm).stem
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

# processing output files
for protein_name, matrix in all_ppms.items():
    output_file = f'{protein_name}'
    output_file_path = output_folder / output_file
    np.save(output_file_path, matrix)