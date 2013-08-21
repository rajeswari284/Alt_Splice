#!/usr/bin/python

import os
import sys
import extractSequence
import PredictExon

def parse(mode, query_start, query_end, chr_num, genome, base_count, strand):

    exon_sequence = ""
    upstream_seq = ""
    downstream_seq = ""
    sequence = ""
    alt_query_start = ""
    alt_query_end = ""
    file_path = 'data/' + genome + '/' + chr_num + '.fa'
    
    if query_start == '' or query_end == '' or chr_num == '':
        print "The input sequence could not be mapped to any genomic sequence data"
        sys.exit(1)

    if mode == 'batch':
        if query_start > query_end:
            strand = '-'
        else:
            strand = '+'
    else:
        if query_start > query_end:
            if strand == '+' :
                print "USER SUPPLIED SEQUENCE IS PRESENT ON THE OPPOSITE STRAND (-)."
                print "Changing strand information....."
                #response = raw_input("Enter 2 to change strand : ")
                #if response == '2':
                strand = '-'
        else:
            if strand == '-':
                print "USER SUPPLIED SEQUENCE IS PRESENT ON THE OPPOSITE STRAND (+)."
                print "Changing strand information....."
                #response = raw_input("Enter 2 to change strand : ")
                #if response == '2':
                strand = '+'

    if strand == '+':
        alt_query_start = query_start
        alt_query_end = query_end
    elif strand == '-':
        alt_query_start = query_end
        alt_query_end = query_start
        
    try:
        file_handle = open(file_path, 'r')
    except IOError:
        print "The genome is not available in the current directory."
        sys.exit(1)

    for lines in file_handle:
        if lines.startswith('>'):
            continue
        sequence += lines.rstrip().lower()

    file_handle.close()

    location = chr_num + ':' + alt_query_start + '..' + alt_query_end
    exon_start, exon_end = PredictExon.extract_exon(location, strand)

    if exon_start == 0 or exon_end == 0:
        exon_start = int(alt_query_start)
        exon_end = int(alt_query_end)

    upstream_seq, exon_sequence, downstream_seq = extractSequence.extract_single(sequence, strand, exon_start, exon_end, base_count)
    sequence = ""

    if exon_sequence == '' or upstream_seq == '' or downstream_seq == '':
        print "The specified coordinates are unable to extract any sequence."
        sys.exit(1)

    return upstream_seq, exon_sequence, downstream_seq, strand


if __name__=='__main__':
    parse()
