import argparse
import pybedtools
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('--reference', '-r', type=str, required=True,
    help='Relative or absolute path to the folder containing preprocessed \
        reference fasta files')
parser.add_argument('--transcriptome', '-tr', type=str, required=True, 
    help='Path to the transcriptome bedfile')
parser.add_argument('--outfile', '-out', type=str, default='.', 
    help='Specify absolute or relative path to output directory, default = .')               
args = parser.parse_args()


ref_files = Path(args.reference)
output_dir = Path(args.outfile)
output_dir.mkdir(parents=True, exist_ok=True)

references = [Path(reference).stem for reference in ref_files.glob('*.fa*')]

transcriptome = args.transcriptome

transcriptome_name = Path(transcriptome).stem
transcriptome_bed_object = pybedtools.BedTool(args.transcriptome)

output_file_name = f'{transcriptome_name}_preprocessed.bed'
output_file_path = output_dir / output_file_name

pybedtools.BedTool(line for line in transcriptome_bed_object\
    if line.chrom in references)\
    .saveas(output_file_path)