#!/usr/bin/python

import os
import sys
from Bio.Seq import Seq
from Bio.Alphabet import NucleotideAlphabet

def extract_single(seq, strand_info, seq_start, seq_end, bases):

    if strand_info == '-':
        dna = Seq(seq, NucleotideAlphabet())
        seq_comp = dna.complement()
        #complement = {'a':'t','c':'g','g':'c','t':'a','n':'n'}
        #seq_comp = "".join([complement[nt.lower()] for nt in seq])
        exon_sequence = ((str(seq_comp[seq_start-1:seq_end]))[::-1]).upper()

        upstream_start = seq_end
        upstream_end = seq_end + bases
        upstream_seq = (str(seq_comp[upstream_start:upstream_end]))[::-1]

        downstream_start = (seq_start - 1) - bases
        downstream_end = seq_start - 1
        downstream_seq = (str(seq_comp[downstream_start:downstream_end]))[::-1]
    else:
        exon_sequence = (seq[seq_start-1:seq_end]).upper()

        upstream_start = (seq_start - 1) - bases
        upstream_end = seq_start - 1
        upstream_seq = seq[upstream_start:upstream_end]

        downstream_start = seq_end
        downstream_end = seq_end + bases
        downstream_seq = seq[downstream_start:downstream_end]

    return upstream_seq, exon_sequence, downstream_seq

def extract_batch(loc_file, strand, seq_start, seq_end, bases):
    
    sequence = ""
    for lines in loc_file:
        if lines.startswith('>'):
            continue
        else:
            sequence += lines.rstrip().lower()

    upstream_seq, exon_sequence, downstream_seq = extract_single(sequence, strand, seq_start, seq_end, bases)    
    sequence = ""

    return upstream_seq, exon_sequence, downstream_seq

if __name__ == '__main__':
    seq = sys.argv[1]
    strand = sys.argv[2]
    seq_start = sys.argv[3]
    seq_end = sys.argv[4]
    bases = 100
    mode = 'batch'
    extract_single(seq, strand, seq_start, seq_end, bases)
    extract_batch(loc_file, bases)
