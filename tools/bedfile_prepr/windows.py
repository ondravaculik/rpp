import argparse
import pybedtools
import time
import numpy as np
from pathlib import Path


def window(line):
    start = line.start
    stop = line.stop
    length = stop - start
    if length > window_size:
        above = length - window_size
        rand = np.random.randint(0, above)
        new_start = start + rand
        new_stop = start + rand + window_size
    elif length < window_size:
        missing = window_size - length
        rand = np.random.randint(0, missing)
        new_start = start - rand
        new_stop = stop + (missing - rand)
    else:
        new_start = start
        new_stop = stop

    line.start = new_start
    line.stop = new_stop
    return line


parser = argparse.ArgumentParser()
parser.add_argument('--infile', '-in', type=str, required=True,
    help='Absolute Path to bedfiles with protein binding sites positions')
parser.add_argument('--window_size', '-ws', type=int, default=50,
    help='Define window size for each bedfile position, default=50')
parser.add_argument('--outfile', '-out', type=str, default='.',
    help='Specify absolute or relative path to output directory, default = .')                
args = parser.parse_args()


window_size = args.window_size

p = Path(args.outfile)
bed_files = Path(args.infile)

ts = time.time()

# preparing output files and folders
output_dir = Path(f'{p}', 'results', 'preprocessed_bedfiles', 'windows', f'{ts}')
output_dir.mkdir(parents=True, exist_ok=True)

for bedfile in bed_files.glob('*.bed'):
    bed_path = Path(bedfile)
    output_file_name = bed_path.stem + f'_window-{window_size}.bed'
    output_file_path = output_dir / output_file_name

    pybedtools.BedTool(bedfile)\
        .each(window)\
        .saveas(output_file_path)