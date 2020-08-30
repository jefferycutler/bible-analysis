import os.path

infile="/home/jeffc/dev/bible-analysis/cnvsource/rawdata/eng-asv_vpl.xml"

#############################################
## verify the input file really exists
if not os.path.isfile(infile):
    print('!!!! PROBLEM - INPUT FILE NOT VALID !!!')
    exit(1)

trns_abbr=os.path.basename(infile).split('-')[1].split('.')[0]
print(trns_abbr)