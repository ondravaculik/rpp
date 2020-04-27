import argparse
import numpy as np
import time
from pathlib import Path


def randomPPMcreator(seq_length):  
    sequence_ppm_arrays = [np.random.dirichlet(
        np.ones(4), size=1) for i in range(0, seq_length)]
    sequenceppm = [(ppm[0].tolist()) for ppm in sequence_ppm_arrays]
    return sequenceppm


parser = argparse.ArgumentParser()
parser.add_argument('--number', '-n', type=int,
    help='Number of random PPMs user wants to create', default=1)
parser.add_argument('--seq_length', '-sl', default=7, type=int,
    help='Number that specifies how long will be the random training sequence')
parser.add_argument('--outfile', '-out', type=str, default='.',
    help='Specify absolute or relative path to output directory, default = .')    
args = parser.parse_args()


seq_length = args.seq_length

random_ppms = {}
for i in range(args.number):
    header = f'random_{i+1}'
    ppm = randomPPMcreator(seq_length)
    random_ppms[header] = ppm

# preparing output files and folders
p = Path(args.outfile)
ts = time.time()

# preparing output files and folders
output_folder = Path(f'{p}', 'results', 'preprocessed_pwms', 'random', f'{ts}')
output_folder.mkdir(parents=True, exist_ok=True)

for header, ppm in random_ppms.items():
    output_file = f'{header}'
    output_file_path = output_folder / output_file
    np.save(output_file_path, ppm)