from pathlib import Path
import argparse
import numpy as np
import time


def get_ppm_from_pwm(position_weight):
    return (2**(position_weight))/4


def createProbabilityVector(pwm):
    probabilityVector = get_ppm_from_pwm(pwm)
    probabilityVector = probabilityVector / \
        probabilityVector.sum(axis=1)[:, np.newaxis]
    return probabilityVector


parser = argparse.ArgumentParser()
parser.add_argument('--prob_weight_matrix', '-pwm', type=str, required=True,
    help='Relative or absolute path to the folder\
         containing one or multiple PWMs')
parser.add_argument('--outfile', '-out', type=str, default='.',
    help='Specify absolute or relative path to output directory, default = .')
args = parser.parse_args()


# preparing files and folders
ts = time.time()

p = Path(args.outfile)

output_folder = Path(f'{p}', 'results', 'preprocessed_pwms', 'real', f'{ts}')
output_folder.mkdir(parents=True, exist_ok=True)

# creating dict of np.arrays with all users PWMs
input_file = Path(args.prob_weight_matrix)
processed_ppms = {}

with open(input_file) as f:
    motif_name = ''
    pwm = []
    lines = f.readlines()
    for i, line in enumerate(lines):
        if i == 0 and not line.startswith('>'):
            break
        elif i < len(lines)-1:
            if line.startswith('>'):
                if motif_name == '':
                    motif_name = line.strip() 
                else:
                    processed_ppms[motif_name] = np.asfarray(
                        createProbabilityVector(np.asarray(pwm)))
                    motif_name = line.strip()
                    pwm = []                               
            else:
                position_pwm = [float(pos) for pos in line.strip().split()]
                pwm.append(position_pwm)                
        else:
            if line.strip() == '':
                processed_ppms[motif_name] = np.asfarray(
                    createProbabilityVector(np.asarray(pwm)))
            else:
                position_pwm = [float(pos) for pos in line.strip().split()]
                pwm.append(position_pwm)
                processed_ppms[name] = np.asfarray(
                    createProbabilityVector(np.asarray(pwm)))

# processing output files
for header, ppm in processed_ppms.items():
    output_file = f'{header[1:]}'
    output_file_path = output_folder / output_file
    np.save(output_file_path, ppm)