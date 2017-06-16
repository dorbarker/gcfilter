#!/usr/bin/env python3

"""Filter FASTQ files by GC content.

Usage: gcfilter.py <lower> <upper> <fastq>

Arguments:
    lower   Inclusive lower bound on allowed GC content in the interval [0,1]
    upper   Inclusive upper bound on allowed GC content in the interval [0,1]
    fastq   Path to the FASTQ file
"""

import sys
from pathlib import Path
from docopt import docopt
from Bio import SeqIO

def load_fastq_data(path):
    '''Reads the FASTQ file located at `path` and
    returns a list of FASTQ sequences.
    '''

    with path.open('r') as fastq:
        return list(SeqIO.parse(fastq, 'fastq'))

def calculate_gc(sequence):
    '''Given a sequence, return the GC content'''
    seq = sequence.upper()

    return (seq.count('G') + seq.count('C')) / len(seq)

def filter_sequences(lower, upper, sequences):
    '''Filters sequences by GC content,
    and writes the filtered FASTQ to STDOUT
    '''
    selected_sequences = (rec for rec in sequences
                          if lower <= calculate_gc(rec.seq) <= upper)

    SeqIO.write(selected_sequences, sys.stdout, 'fastq')

def validate_arguments(args):
    '''Validate arguments and convert types'''

    def validate_gc_bound(bound):
        '''Validates the GC bound arguments'''

        msg = 'GC bounds must be numbers in the interval [0,1]'

        try:
            out = float(bound)

            if not 0 <= out <= 1:
                raise ValueError(msg)

        except ValueError:
            raise TypeError(msg)

        return out

    args['<lower>'] = validate_gc_bound(args['<lower>'])
    args['<upper>'] = validate_gc_bound(args['<upper>'])

    args['<fastq>'] = Path(args['<fastq>'])

    if not args['<fastq>'].exists():
        name = str(args['<fastq>'])
        raise OSError('{} does not exist.'.format(name))

    return args

def main():
    '''Main function. Runs all other functions'''

    args = validate_arguments(docopt(__doc__))

    sequences = load_fastq_data(args['<fastq>'])

    filter_sequences(args['<lower>'], args['<upper>'], sequences)

if __name__ == '__main__':
    main()
