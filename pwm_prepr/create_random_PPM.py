import argparse
import numpy as np
import datetime
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('--number', '-n', type=int,
    help='Number of random PPMs user wants to create', default=1)
parser.add_argument('--output_dir', '-od', type=str, help='Specify\
     working directory, where output should be placed, by either\
     relative or absolute PATH', default='.')
parser.add_argument('--seq_length', '-sl', default=8, type=int,
    help='Number that specifies how long will be the random training sequence')
args = parser.parse_args()


def randomppmCreator(seq_length):  # random PPM creating
    sequence_ppm_arrays = [np.random.dirichlet(
        np.ones(4), size=1) for i in range(0, seq_length)]
    sequenceppm = [(ppm[0].tolist()) for ppm in sequence_ppm_arrays]
    return sequenceppm


random_ppms = {}
for i in range(args.number):
    header = f'random_{i+1}'
    ppm = randomppmCreator(args.seq_length)
    random_ppms[header] = ppm


# preparing output files and folders
p = Path(args.output_dir)
dt = datetime.datetime.now().strftime("%d:%m:%Y-%H:%M")

# preparing output files and folders
output_folder = Path(f'{p}', 'results', 'preprocessed_pwms', f'{dt}')
output_folder.mkdir(parents=True, exist_ok=True)


for header, ppm in random_ppms.items():
    output_file = f'{header}'
    output_file_path = output_folder / output_file
    np.save(output_file_path, ppm)