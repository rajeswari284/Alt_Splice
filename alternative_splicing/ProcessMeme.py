#!/usr/bin/python

import os
import sys

def execute(input_file, meme_output):

    meme_prog = os.environ['HOME'] + "/meme/bin/meme"
    if meme_output:
        os.system(meme_prog + " " + input_file + " -dna -o " + meme_output)
    else:
        os.system(meme_prog + " " + input_file + " -dna")
    
def download(input_file, meme_output):

    meme_response = raw_input("Do you already have MEME installed on your system : ")
    if meme_response == 'n':
        print "Preparing to install MEME on your system....."
        os.system("curl --remote-name ebi.edu.au/ftp/software/MEME/4.9.0/meme_4.9.0.tar.gz")
        os.system("tar -zxf meme_4.9.0.tar.gz")
        os.chdir("meme_4.9.0")
        home_dir = os.environ['HOME']
        os.system("./configure --prefix=" + home_dir + "/meme --with-url=http://meme.nbcr.net/meme")
        os.system("make")
        os.system("make test")
        os.system("make install")
        path_variable = os.environ['PATH']
        os.environ["PATH"] = os.environ["PATH"] + ":" + os.environ["HOME"] + "/meme"
        print os.environ['PATH']
        
        print "Congratulations!!! MEME has been successfully installed in your system...."
    
    execute(input_file, meme_output)

if __name__ == '__main__':
    input_file = sys.argv[1]
    download(input_file)
