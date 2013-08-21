#/usr/bin/python

import os
import sys
import argparse
import re
from datetime import datetime
from collections import defaultdict
import extractSequence
import argparser
import BlatParser
import ProcessMeme
import PredictExon

'''
    This program is intended to extract upstream and downstream regions of a given exon.
    The input to the program can be either an exon sequence in the format of a fasta file
    or the location co-ordinates of the exon in the genome. If input is given as a sequence,
    The program will run blat to map the sequence back to the original genome, extract
    coordinates and then extract upstream and downstream regions.

    The output of this will be a fasta file containing 3' intron region sequence, intermediate
    exon and 5' intron sequence.

'''
        
def write_seq(upstream_seq, exon_sequence, downstream_seq, outfile, genome, seq_start, seq_end, strand):
    outfile_handle = open(outfile, 'a')    
    outfile_handle.write('Genome\tExon Location\t3\'Intron\tExon\t5\'Intron\tStrand\tEntry Created On\n')
    outfile_handle.write(genome + '\t' + str(seq_start) + '..' + str(seq_end) + '\t' + upstream_seq + '\t' + exon_sequence + '\t' + downstream_seq + '\t' + strand + '\t' + str(datetime.now()) + '\n')


def write_fasta(upstream_seq, exon_sequence, downstream_seq, outfile, genome, seq_start, seq_end, strand):
    outfile_handle = open(outfile + '.fasta', 'a')
    fasta_header = '>' + genome + '|' + str(seq_start) + '-' + str(seq_end) + '|' + str(datetime.now())
    outfile_handle.write(fasta_header + '\n')
    sequence = upstream_seq + exon_sequence + downstream_seq
    outfile_handle.write(sequence + '\n')

def run_blat(database_dir, temp_filename, blat_prog, query_seq_length, mode, genome, base_count, strand):

    done = False
    query_start = ""
    query_end = ""
    chr_num = ""

    for root, dirs, files in os.walk(database_dir):
        for f in files:
            database = database_dir + '/' + f
            cmd = blat_prog + ' ' + database + ' ' + temp_filename + ' blat_output.txt' + ' -out=blast8 -fastMap -minIdentity=99'
            os.system(cmd)

            blat_handle = open('blat_output.txt', 'r')
            for lines in blat_handle:
                fields = lines.rstrip().split('\t')
                query_start = fields[8]
                query_end = fields[9]
                chr_num = fields[1]
                sub_seq_length = fields[3]
                
                if int(sub_seq_length) == query_seq_length:
                    done = True
                    break
            if done:
                break
        sequence = ""

    if done:
        blat_handle.close()
        print "EXTRACTING UPSTREAM AND DOWNSTREAM REGIONS....."
        upstream_seq, exon_sequence, downstream_seq, strand = BlatParser.parse(mode, query_start, query_end, chr_num, genome, base_count, strand)
        print "Writing output to file...."
        write_seq(upstream_seq, exon_sequence, downstream_seq, outfile_name, genome, query_start, query_end, strand)
        write_fasta(upstream_seq, exon_sequence, downstream_seq, outfile_name, genome, query_start, query_end, strand)

    return done, query_start, query_end, chr_num


print "WELCOME TO THE UPSTREAM AND DOWNSTREAM REGION EXTRACTION TOOL"
print "*************************************************************\n"

parser = argparse.ArgumentParser(prog="Extract_upstream_sequence.py", description="Extract upstream and downstream regions")
parser.add_argument('--type', default=1, help='This option allows the user to choose what type of data they want to provide ' + \
                        'as input to the program. A value of 1 will allow them to use sequence data, whereas value of 2 is ' + \
                        'for location coordinates. Default value is 1')
parser.add_argument('--mode', default='single', help='This option allows user to choose single sequence as input or batch mode.' + \
                        'If not specified, default is single sequence mode.')
parser.add_argument('--location', default='', help='This option allows user to specify a single genomic location whose sequence needs ' + \
                        'to be extracted or a file with multiple genomic locations(Please refer to the README for details on location file format).' + \
                        'This is a mandatory option if choosing type 2.Location needs to be input in the following format, for example, chr12:1234..5678')
parser.add_argument('--seqfile', default='', help='This option allows user to specify a sequence filename whose upstream and downstream' + \
                        'region needs to be extracted. This is a mandatory option if choosing default type 1.')
parser.add_argument('--strand', default='+', help='This optional parameter allows a user to specify strand information.Correct strand is denoted by +' + \
                        'and reverse strand by -. Default is +')
parser.add_argument('--organism', default='Homo_sapiens', help='This optional parameter allows the program to search for the input sequence/coordinates ' + \
                        'in the specified genome. If not specified, will search against human genome.')
parser.add_argument('--bases', default=100, type=int, help='This parameter allows a user to specify how many bases upstream and downstream ' + \
                        'of the exon should be extracted. If not provided, it defaults to 100 bases upstream and downstream.')
parser.add_argument('--outfile', default='', help='This is an optional parameter to specify name for an output filename. ' + \
                        'Can be provided either as an absolute path or just filename alone. If not specified, will use a program generated filename.')
parser.add_argument('--meme', default=False, help='This is an optional parameter to specify if the output file needs to be sent to meme server ' + \
                        'for identification of motifs. By default, the switch is turned off.')

# The user supplied arguments are parsed
parsed_data = argparser.parse(parser)
mode = parsed_data['mode']
genome = parsed_data['org']
base_count = parsed_data['bases']
strand = parsed_data['strand']
location = parsed_data['location']
sequence_filename = parsed_data['seq_file']
meme_mode = parsed_data['meme']
sequence = ""

# Create output file name

if not parsed_data['outfile'] == '':
    if os.path.isabs(parsed_data['outfile']):
        out_name = parsed_data['outfile'].split('/')[-1]
        out_dir = parsed_data['outfile'].replace(out_name, '')
        print out_dir
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        outfile_name = parsed_data['outfile']
    else:
        if not os.path.exists("Results"):
            os.makedirs("Results")
        outfile_name = "Results/" + parsed_data['outfile']
else:
    if not os.path.exists("Results"):
        os.makedirs("Results")
    outfile_name = "Results/" + 'exon_sequence_in_' + genome


# The steps below are taken if the user provides genomic location input in correct format. 
# Using the location input, exon sequence, upstream and downstream regions 
# are extracted from the whole genome information
if parsed_data['type'] == '2':
    if re.match('chr\d+\:\d+\.\.\d+', location):
        print "User has provided genomic location as input data."
        if mode == 'batch':
            mode_response = raw_input('USER HAS PROVIDED BATCH MODE WITH A SINGLE LOCATION...PRESS ENTER TO CONTINUE PROGRAM OR PRESS 2 TO CHANGE MODE : ')
            if mode_response == '2':
                mode = 'single'

        exon_start, exon_end = PredictExon.extract_exon(location, strand)
            
        seq_start = location.split(':')[1].split('..')[0]
        seq_end = location.split(':')[1].split('..')[1]    
        chr_num = location.split(':')[0]
        file_path = 'data/' + genome + '/' + chr_num + '.fa'

        if exon_start == 0 or exon_end == 0:
            exon_start = int(seq_start)
            exon_end = int(seq_end)

        # This checks to make sure the complete genome file exists in the current directory.
        # If not present, program will terminate with a message
        try:
            file_handle = open(file_path, 'r')
        except IOError:
            print "The genome is not available in the current directory"
            sys.exit(1)
        # This step reads the genome data into a string
        
        for lines in file_handle:
            if lines.startswith('>'):
                continue
            else:
                sequence += lines.rstrip().lower()

        # Exon and its upstream and downstream sequences are extracted from the complete genome sequence
        print "EXTRACTING UPSTREAM AND DOWNSTREAM REGIONS...."
        upstream_seq, exon_sequence, downstream_seq = extractSequence.extract_single(sequence, strand, exon_start, exon_end, base_count)        
        sequence = ""
        if exon_sequence == '' or upstream_seq == '' or downstream_seq == '':
            print "The specified coordinates are unable to extract any sequence"
            sys.exit(1)

        # Output is written into a file
        print "WRITING OUTPUT TO " + outfile_name + "...."
        write_seq(upstream_seq, exon_sequence, downstream_seq, outfile_name, genome, seq_start, seq_end, strand)
        write_fasta(upstream_seq, exon_sequence, downstream_seq, outfile_name, genome, seq_start, seq_end, strand)

    elif os.path.exists(location):
        if mode == 'single':
            mode_response = raw_input('USER HAS PROVIDED SINGLE MODE WITH MULTIPLE LOCATIONS...PRESS ENTER TO CONTINUE PROGRAM OR PRESS 2 TO CHANGE MODE : ')
            if mode_response == '2':
                mode = 'batch' 

        print "User has supplied a file containing multiple genomic locations"
        loc_filename = open(location, 'r')
        for lines in loc_filename:
            [seq_start, seq_end, chr_num, strand, genome] = lines.rstrip('\n').split('\t')
            location = chr_num + ':' + seq_start + '..' + seq_end
            exon_start, exon_end = PredictExon.extract_exon(location, strand)
            file_path = open('data/' + genome + '/' + chr_num + '.fa', 'r')

            if exon_start == 0 or exon_end == 0:
                exon_start = int(seq_start)
                exon_end = int(seq_end)

            upstream_seq, exon_sequence, downstream_seq = extractSequence.extract_batch(file_path, strand, exon_start, exon_end, base_count)        

            print "WRITING OUTPUT TO " + outfile_name + "...."
            write_seq(upstream_seq, exon_sequence, downstream_seq, outfile_name, genome, seq_start, seq_end, strand)
            write_fasta(upstream_seq, exon_sequence, downstream_seq, outfile_name, genome, seq_start, seq_end, strand)

    else:
        print "Genomic location data has not been entered in the appropriate format"
        sys.exit(1)

# The steps below are taken if the user supplies sequence file as input. 
# The sequence is first mapped to the genome using Blat to extract genomic coordinates of the sequence. 
else:
    user_home = os.path.expanduser("~/")
    blat_prog = user_home + '/bin/x8664/blat'
    database_dir = './data/' + genome
    
    if mode == 'batch':
        print "USER HAS PROVIDED MULTIPLE SEQUENCES AS INPUT."
        seq_handler = open(sequence_filename, 'r')
        sequence = ""
        temp_filename = 'tmp.fa'

        print "Mapping sequences to genome using Blat...."

        for line in seq_handler:
            if line.startswith('>'):
                if len(sequence) > 0:
                    done = False
                    query_seq_length = len(sequence)
                    
                    temp_file.write(sequence + '\n')
                    temp_file.close()

                    [done, query_start, query_end, chr_num] = run_blat(database_dir, temp_filename, blat_prog, query_seq_length, mode, genome, base_count, strand)
                    sequence = ""                    

                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
                temp_file = open(temp_filename, 'w')
                temp_file.write(line.rstrip() + '\n')
            else:
                sequence += line.rstrip()

        if len(sequence) > 0:
            query_seq_length = len(sequence)
                    
            temp_file.write(sequence + '\n')
            temp_file.close()

            [done, query_start, query_end, chr_num] = run_blat(database_dir, temp_filename, blat_prog, query_seq_length, mode, genome, base_count, strand)
            sequence = ""

    else:
        print "USER HAS PROVIDED A SINGLE SEQUENCE AS INPUT."
        print "Mapping sequences to genome using Blat...."

        seq_handler = open(sequence_filename, 'r')
        sequence = ""
        for line in seq_handler:
            if line.startswith('>'):
                continue
            else:
                sequence += line.rstrip()

        query_seq_length = len(sequence)
        seq_handler.close()

        [done, query_start, query_end, chr_num] = run_blat(database_dir, sequence_filename, blat_prog, query_seq_length, mode, genome, base_count, strand)

if os.path.exists("tmp.fa"):
    os.remove("tmp.fa")

if meme_mode:
    meme_output = raw_input("Would you like to change the default output directory name for meme? If yes, specify name for output dir. Else, press enter : ")
    if meme_output:
        meme_output_dir = meme_output
    else:
        meme_output_dir = ''

    print "The output file of exons will now be sent to MEME server for identifying motifs....."
    ProcessMeme.download(outfile_name + '.fasta', meme_output_dir)
    
else:
    print "THANK YOU FOR USING OUR SOFTWARE"
