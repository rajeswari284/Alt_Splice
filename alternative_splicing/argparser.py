#!/usr/bin/python

import os
import sys

def parse(parser):

    parsed_data = dict()
    args, unknown = parser.parse_known_args()
    if unknown:
        print "INCORRECT PARAMETERS HAVE BEEN SENT TO THE PROGRAM\n"
        print parser.print_help()
        sys.exit(1)

    location = args.location
    seq_file = args.seqfile
    mode = args.mode

    if args.type == '2':
        if location == '':
            print "THIS OPTION REQUIRES YOU TO ENTER GENOMIC COORDINATES....\n"
            print parser.print_help()
            sys.exit(1)
    else:
        if seq_file == '':
            print "THIS OPTION REQUIRES YOU TO ENTER A SEQUENCE FILE....\n"
            print parser.print_help()
            sys.exit(1)

    if mode == 'batch':
        print "Running program in Batch Mode.....\n"
        strand_info = args.strand
    else:
        print "Running program in Single Mode....\n"
        if args.strand == '+':
            strand_option = raw_input("You have selected the default plus strand. If this is correct, hit enter. If you would like to change the strand to minus, enter 2 : ")
            if strand_option == '2':
                print "The strand is now changed to minus."
                strand_info = '-'
            else:
                strand_info = args.strand
        else:
            strand_info = args.strand

    if mode == 'batch':
        input_org = args.organism
    else:
        if args.organism == 'Homo_sapiens':
            org_option = raw_input("You have selected the default organism Homo sapiens. If you want to continue with this, hit enter. If you would like to change, enter 9 to list all organism names : ")
            if org_option == '9':
                input_org = raw_input("Enter the organism name of your choice from the list below.\n" + \
                                          "Homo_sapiens\n" + \
                                          "Mus_musculus\n" + \
                                          "Gallus_gallus\n" + \
                                          ": ")
            else:
                input_org = args.organism
        else:
            input_org = args.organism

    bases = args.bases
    outfile = args.outfile
    meme_mode = args.meme

    parsed_data = {'type' : args.type,
                   'mode' : mode,
                   'location' : location,
                   'seq_file' : seq_file,
                   'strand' : strand_info,
                   'org' : input_org,
                   'bases' : bases,
                   'outfile' : outfile,
                   'meme' : meme_mode
                   }

    return parsed_data

if __name__ == '__main__':
    parse(parser)
