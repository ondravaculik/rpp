import argparse
import pybedtools
from pybedtools.featurefuncs import midpoint
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('--infile', '-in', type=str, required=True,
    help='Absolute Path to bedfiles with binding sites positions')
parser.add_argument('--outfile', '-out', type=str, default='.',
    help='Specify absolute or relative path to output directory, default = .')                
args = parser.parse_args()


bed_files = Path(args.infile)
output_dir = Path(args.outfile)
output_dir.mkdir(parents=True, exist_ok=True)

for bedfile in bed_files.glob('*.bed'):
    bed_path = Path(bedfile)
    output_file_name = bed_path.stem + '_midpoints.bed'
    output_file_path = output_dir / output_file_name
    
    pybedtools.BedTool(bedfile)\
        .each(midpoint)\
        .saveas(output_file_path)