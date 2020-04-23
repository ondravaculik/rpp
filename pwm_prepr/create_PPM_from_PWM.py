from pathlib import Path
import argparse
import numpy as np
import datetime


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


p = Path(args.outfile)
input_file = Path(args.pwm)
suffix = input_file.suffix

# creating dict of np.arrays with all users PWMs
all_pwms = {}
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
                    all_pwms[motif_name] = np.asarray(pwm)
                    motif_name = line.strip()
                    pwm = []
            else:
                position_pwm = [float(pos) for pos in line.strip().split()]
                pwm.append(position_pwm)
        else:
            position_pwm = [float(pos) for pos in line.strip().split()]
            pwm.append(position_pwm)
            all_pwms[motif_name] = np.asarray(pwm)

# processing every PWM in the dict into a new one with PPMs
processed_ppms = {}
for name, pwm in all_pwms.items():
    processed_ppms[name] = np.asfarray(createProbabilityVector(pwm))

dt = datetime.datetime.now().strftime("%d:%m:%Y-%H:%M")

# preparing output files and folders
output_folder = Path(f'{p}', 'results', 'preprocessed_pwms', f'{dt}')
output_folder.mkdir(parents=True, exist_ok=True)

# creating output file
for header, ppm in processed_ppms.items():
    output_file = f'{header[1:]}'
    output_file_path = output_folder / output_file
    np.save(output_file_path, ppm)