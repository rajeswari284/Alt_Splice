#!/usr/bin/python

import os
import sys
import time
import shutil

# This is the first script to be run after installing the exon_array module.

original_path = os.getcwd()
user_home = os.path.expanduser("~/")
machtype = os.environ['MACHTYPE']

os.environ['MACHTYPE'] = 'x8664'

blat_response = raw_input("Do you already have BLAT installed on your system (y/n) : ")
if blat_response == 'n':
    print "Blat will now be installed on your system"
    print "Please change the value of the MACHTYPE variable in your system to be x8664. If this is not done, BLAT will not compile."
    print "Also make sure that the libpng-dev package is installed on your system. If not, go ahead and install using this link : http://www.libpng.org/pub/png/libpng.html"
    
    time.sleep(20)
    
    if not os.path.exists("data"):
        os.makedirs("data")
    else:
        shutil.rmtree("data")
        os.makedirs("data")

    if machtype != 'x8664':
       print "The value of machtype is not correct. Please change the value and re-run the script again"
       sys.exit(1)
    
    if not os.path.exists(user_home + 'bin'):
        os.makedirs(user_home +'bin')
        os.makedirs(user_home + 'bin/' + machtype)
    else:
        shutil.rmtree(user_home + 'bin')
        os.makedirs(user_home +'bin')
        os.makedirs(user_home + 'bin/' + machtype)

    os.environ['PATH'] = os.environ['PATH'] + ":" + os.environ['HOME'] + "/bin/x8664"

    os.system("curl --remote-name http://users.soe.ucsc.edu/~kent/src/blatSrc35.zip")
    if not os.path.exists(user_home + 'Downloads/blatSrc35.zip'):
        shutil.move('blatSrc35.zip', user_home + 'Downloads')
    else:
        os.remove(user_home + 'Downloads/blatSrc35.zip')
        shutil.move('blatSrc35.zip', user_home + 'Downloads')

    if os.path.exists(user_home + 'Downloads/blatSrc'):
        shutil.rmtree(user_home + 'Downloads/blatSrc')

    os.chdir(user_home + 'Downloads')
    os.system("unzip blatSrc35.zip")
    os.chdir("blatSrc")
    os.system("make clean")
    os.system("make")
    print "CONGRATULATIONS!!!BLAT WAS SUCCESSFULLY INSTALLED ON YOUR SYSTEM."
    time.sleep(10)
        
if os.path.exists(original_path + '/data/Homo_sapiens'):
    print "All settings are complete. You can now use the software for your analysis."
    sys.exit(1)
else:
    print "The software automatically installs the human genome data for you. In case if you are working with any other genome, " + \
        "please make sure you have the species genome downloaded separately within the data directory."

    print "Starting download of human genome data....This might take some time depending on the size of the genome being downloaded."
    os.chdir(user_home + 'Downloads')
    os.system("curl --remote-name http://hgdownload.soe.ucsc.edu/goldenPath/hg19/bigZips/chromFa.tar.gz")
    
    if not os.path.exists(original_path + '/data/Homo_sapiens')
        os.makedirs(original_path + '/data/Homo_sapiens')
    else:
        shutil.rmtree(original_path + '/data/Homo_sapiens')
        os.makedirs(original_path + '/data/Homo_sapiens')

    download_dir = original_path + '/data/Homo_sapiens'
    print download_dir
    os.system("tar -xvf chromFa.tar.gz -C " + download_dir)
    print "Download complete."
