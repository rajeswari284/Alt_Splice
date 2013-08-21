#!/usr/bin/python

import os
import sys

def extract_exon(input_loc, strand):
    chr_num = input_loc.split(':')[0]
    seq_start = input_loc.split(':')[1].split('..')[0]
    seq_end = input_loc.split(':')[1].split('..')[1]
    matched_transcript = ''
    num_exons = 0
    exon_start_site = 0
    exon_stop_site = 0

    exon_info_file = open('data/Homo_sapiens/knownGene.txt', 'r')
    for line in exon_info_file:
        fields = line.rstrip().split('\t')
        if fields[1] == chr_num and fields[2] == strand:
            if int(seq_start) >= int(fields[3]) and int(seq_end) <= int(fields[4]):
                if int(fields[7]) > num_exons:
                    num_exons = int(fields[7])
                    matched_transcript = line.rstrip()
                else:
                    num_exons = int(fields[7])

    exon_info_file.close()

    cols = matched_transcript.split('\t')
    exon_starts = cols[8].split(',')
    exon_stops = cols[9].split(',')
    exon_pos = False
    intron_pos = False

    for sites in range(len(exon_starts)):
        if exon_starts[sites] == '':
            continue
        if int(exon_starts[sites])+1 == int(seq_start) and int(exon_stops[sites]) == int(seq_end):
            exon_pos = True
            exon_start_site = int(seq_start)
            exon_stop_site = int(seq_end)
            print "The supplied positions matches an exon exactly..."
            break
        elif int(exon_starts[sites])+1 >= int(seq_start) and int(exon_stops[sites]) <= int(seq_end):
            exon_start_site = int(exon_starts[sites]) + 1
            exon_stop_site = int(exon_stops[sites])
            exon_pos = True
            print "The supplied sequence incorporates an exon within it...."
            break
        elif int(exon_starts[sites])+1 <= int(seq_start) and int(exon_stops[sites]) >= int(seq_end):
            exon_start_site = int(exon_starts[sites]) + 1
            exon_stop_site = int(exon_stops[sites])
            exon_pos = True
            print "The supplied sequence is located within an exon start and stop site..."
            break
        elif int(exon_starts[sites])+1 >= int(seq_start) and int(exon_stops[sites]) >= int(seq_end):
            exon_start_site = int(exon_starts[sites]) + 1
            exon_stop_site = int(exon_stops[sites])
            exon_pos = True
            print "The supplied sequence may have a portion of it within an exon..."
            break
        elif int(exon_stops[sites]) < int(seq_start):
            intron_pos = True

    if not exon_pos and intron_pos:
        print "The supplied sequence lies within an intron..."


    return exon_start_site, exon_stop_site


if __name__ == '__main__':
    location = sys.argv[1]
    extract_exon(location)
