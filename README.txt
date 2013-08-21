************************************************
          Exon Array Analysis tool:
************************************************

This tool is used to perform downstream analysis of exon data. Given an exon sequence or location, this tool is used to extract the 3' and 5' intronic regions.
A bunch of intron sequences can then be analyzed to look for common motifs and further mapped to a sequnce with known function.

The source code is written in python and is packaged into modules.

Once the source code is installed on the system, cd into the alternative_splicing directory of the distribution and the program can be run in the following manner:

python extract_upstream_sequence.py <parameter list>

The entire list of available parameters along with their usage can be obtained through the following:

python extract_upstream_sequence.py --help

PREREQUISITES:

1: Python 2.7 or higher ;  Platform : Mac OS X (version 10.7 and higher)
2: Latest version of Biopython. This can be downloaded through the following link : http://biopython.org/DIST/docs/install/Installation.html#htoc22
3: Once downloaded and uncompressed, cd into the biopython * directory and run the following command to have a one step install of biopython
   python setup.py install
4: Latest version of the libpng package for Mac. This can be obtained from the folowing link : http://www.libpng.org/pub/png/libpng.html. Select either the .zip or .gz version (depending on the OS being installed on).
5: Once uncompressed, run the following commands:
   ./configure --prefix=/usr
    make check
    make install
6: Species genome data. This will be downloaded at the time of running the configuration script.

Currently, the software has been tested only on a Mac OS X (versions 10.7 and 10.8). 

The program either accepts a genomic coordinate type input or a sequence input. Given a genomic coordinate, the program extracts the exon sequence from the genome and then further strips out the 3' and 5' intronic regions.

Standard tools like Blat will always extract upto 100 upstream and downstream of the given exon sequence. But, in this tool, user has the flexibility to choose how many bases up and down would they require.

Given an exon sequence, the program first tries to map the sequence to its genome (using Blat) to extract the location coordinates. Once, the coordinates are obtained, the exon, 3' and 5' intronic sequences can be 
obtained through the same process as above.

The program can be run either in single or in batch mode. This information can be provided through the --mode switch. By default, the program is run in single mode. 

When run in batch mode using genomic coordinates as input type, the location file should be a tab delimited file with the following columns:
start	 stop	  chromosome#	     strand	 organism

The output of the program are 2 files : a tab delimited file and a fasta file. Both files contain sequences of the exon, 3' and 5' intronic regions along with strand information, location coordinates etc.

The fasta file obtained from here can be provided as input to the motif finding program MEME. This might extract useful motif information for the set of sequences and the output from MEME can further be given to MAST
to obtain known sequences where a similar motif can be found.
