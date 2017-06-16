#!/usr/bin/env python3

#    gcfilter - Filters FASTQ files by GC content
#    Copyright (C) 2017 Dillon Barker
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""gcfilter - Filters FASTQ files by GC content
Copyright (C) 2017 Dillon Barker
program is free software: you can redistribute it and/or modify
under the terms of the GNU General Public License as published by
Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

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
