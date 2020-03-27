import argparse
import pybedtools
import numpy as np
from pathlib import Path


def window(line):
    np.random.seed(window_seed)
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
parser.add_argument('--window_seed', '-seed', type=int, default=101,
    help='Define seed for np.random to get reproducible data, default=101')
parser.add_argument('--outfile', '-out', type=str, required=True,
    help='Specify Path to output folder or use stdout by default')                
args = parser.parse_args()


window_size = args.window_size
window_seed = args.window_seed

bed_files = Path(args.infile)
output_dir = Path(args.outfile)
output_dir.mkdir(parents=True, exist_ok=True)

for bedfile in bed_files.glob('*.bed'):
    bed_path = Path(bedfile)
    output_file_name = bed_path.stem + f'_window-{window_size}.bed'
    output_file_path = output_dir / output_file_name
    pybedtools.BedTool(bedfile)\
        .each(window)\
        .saveas(output_file_path)