import re
import random
import argparse
import numpy as np
import datetime
import pybedtools
from pathlib import Path
from typing import List
from math import log2


def ppm_processing(ppm):  
    """ 
    converts users Position Probability Matrix (PPM) files into a dict 
    """
    all_ppms_to_process = {}
    preprocessed_ppms = Path(ppm)
    for ppm in preprocessed_ppms.glob('*.npy'):
        name = Path(ppm).stem
        loaded_ppm = np.load(ppm)
        all_ppms_to_process[name] = loaded_ppm
    return all_ppms_to_process


def ppm_to_seq_and_score(ppm, alphabet):
    """
    converts PPM into sequence and sequence score
    """
    sequence = ''
    seq_score = 0
    for position in ppm:
        nucleotide = np.random.choice(alphabet, 1, p=position)
        sequence += nucleotide[0]
        seq_score += log2(position[alphabet.index(nucleotide)]/0.25)
    seq_score = str(seq_score) # must be str (pybedtools condition)
    return sequence, seq_score


def reverse_complement_seq(sequence): 
    """ 
    takes sequence and returns its reverse complement 
    """
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    reverse_complement_seq = "".join(complement[base] for base in reversed(sequence))
    return reverse_complement_seq


def get_number_of_positions_for_each_reference(proportions, datasize):
    """ 
    creates dict with number of positions for every reference according to
    its length and chosen datasize; counts length of every reference
    as well as total length of all references
    """
    positions_by_reference = {}
    reference_lengths = {}
    total_len = 0
    with open(proportions) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                continue
            else:
                name, length, proportion = line.strip().split('\t')
                total_len += int(length)
                number_of_positions = int(float(proportion) * datasize)
                positions_by_reference[name] = number_of_positions
                reference_lengths[name] = int(length)
    return positions_by_reference, reference_lengths, total_len 


def randomfindMotif(chrom_sequence, seq_length, ppm, alphabet, header):
    """ 
    returns bedfile interval with the random position of binding motif in reference
    """ 
    binding_seq, score = ppm_to_seq_and_score(ppm, alphabet)
    reverse_complement_binding_seq = reverse_complement_seq(binding_seq)
    motif = random.choice([binding_seq, reverse_complement_binding_seq])

    if motif == binding_seq:
        strand = '+'
    else:
        strand = '-'

    start_searching_index = random.randint(int(0.05*seq_length), int(0.95*seq_length))

    searching_direction = random.choice(['right', 'left'])

    if searching_direction == 'right':
        start = chrom_sequence.find(motif, start_searching_index, seq_length)
    else:
        start = chrom_sequence.rfind(motif, 0, start_searching_index) 

    if start == -1:
        start = randomfindMotif(chrom_sequence, seq_length, ppm, alphabet, header)
    else:
        end = start+len(motif)
        bed_line = [header, start, end, '.', score, strand]
        return bed_line      


def positions_generator(name, ppm, datasize, alphabet, positions_by_reference,
    reference_lengths, total_len):
    """
    uses previous functions to produce output bedfile with
    random positions according to the input PPM
    """
    positions_from_ppm = {}
    ref_files = Path(args.reference)

    intervals = []

    for reference in ref_files.glob('*.fa*'):
        header = ''
        chrom_sequence = ''

        ref_path = Path(reference)
        header += ref_path.stem
        
        with ref_path.open("r", encoding='utf-8') as rf:
            for line in rf.readlines():
                if line.startswith('>'):
                    continue
                else:
                    chrom_sequence = line.strip()

        number_of_positions = positions_by_reference[header]
        seq_length = reference_lengths[header]

        for _ in range(int(number_of_positions)):
            interval = randomfindMotif(
                chrom_sequence, seq_length, ppm, alphabet, header)
            while interval == None:
                interval = randomfindMotif(
                    chrom_sequence, seq_length, ppm, alphabet, header)
            intervals.append(interval)

    output_file = f'{name}_random_positions.bed'
    output_file_path = output_dirs / output_file
    pybedtools.BedTool(intervals).saveas(output_file_path)


parser = argparse.ArgumentParser()
parser.add_argument('--alphabet', '-a', default=['A', 'C', 'G', 'T'],
    type=List[str], help='List of nucleotides in the order corresponding to the PWM;\
         default = ACGT')
parser.add_argument('--datasize', '-ds', default=10000, type=int,
    help='Number that specifies how many training positions user wants to create, \
        default = 10000')
parser.add_argument('--reference', '-r', type=str,
    help='Relative or absolute path to the folder containing preprocessed \
        reference fasta files', required=True)
parser.add_argument('--outfile', '-out', type=str, default='.',
    help='Specify absolute or relative path to output directory, default = .')
parser.add_argument('--position_probability_matrix', '-ppm', type=str, required=True,
    help='Name of the folder containing one or more preprocessed PPMs; \
        random PPM is created by default')
parser.add_argument('--proportions', '-prop', type=str, required=True,
    help='Relative or absolute path to the folder containing text file \
        with reference names and their proportions')                    
args = parser.parse_args()


# preparing files and folders
dt = datetime.datetime.now().strftime("%d:%m:%Y-%H:%M")
p = Path(args.outfile)
output_dirs = Path(f'{p}', 'results', 'final_random_positions', f'{dt}')
output_dirs.mkdir(parents=True, exist_ok=True)

# preparing prerequisities
alphabet = args.alphabet
datasize = int(args.datasize)

# preparing dict of all ppms that will be used to create random positions
ppm_to_process = ppm_processing(args.position_probability_matrix)
positions_by_reference, reference_lengths, total_len = get_number_of_positions_for_each_reference(
    args.proportions, datasize)

# producing final outputs
for name, ppm in ppm_to_process.items():
    positions_generator(name, ppm, datasize, alphabet, positions_by_reference, reference_lengths, total_len)