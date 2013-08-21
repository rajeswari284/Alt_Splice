#!/usr/bin/python

import os
import sys
import re

infile = sys.argv[1]
infile_handle = open(infile, 'r')
outfile = open('exon_location_info.txt', 'w')

for lines in infile_handle:
    if lines.startswith('#'):
        continue
    fields = lines.rstrip().split('\t')
    exon_starts = fields[8].rstrip(',').split(',')
    exon_stops = fields[9].rstrip(',').split(',')
    for site in range(len(exon_starts)):
        print >> outfile, fields[1] + '\t' + fields[2] + '\t' + fields[3] + '\t' + fields[4] + '\t' + fields[5] + '\t' + fields[6] + '\t' +  exon_starts[site] + '\t' + exon_stops[site]
    
