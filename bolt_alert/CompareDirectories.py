#!/usr/local/anaconda3/bin/python

'''
Created on Nov 21, 2019

@author: jhancock

Program for Lisa to use and modify to compare contents of pairs of directories, to compare
what is intended to be archived to what actually was archived.  
'''

import subprocess

# dir_pairs is a list of directory pairs, where each pair is a list of two directories (list of lists)
# Lists are created with square brackets (as opposed to dictionaries, which is braces {})
# List elements are separated by commas.
# Replace these test directories with the ones you want to check.
#                           Source                                                 Archived
dir_pairs = [
    ['/home/nowcast/data/BoltAlert/ascii/ltgCoLMA/20191203/*', '/home/nowcast/data/BoltAlert/archive/test/BoltAlert/ascii/ltgCoLMA/20191203/*'],
    ['/home/nowcast/data/BoltAlert/mdv/lmaFlashExtent/20191203/*', '/home/nowcast/data/BoltAlert/archive/test/BoltAlert/mdv/lmaFlashExtent/20191203/*'],
    ['/home/nowcast/data/BoltAlert/mdv/ltg/CoLMA/20191203/*', '/home/nowcast/data/BoltAlert/archive/test/BoltAlert/mdv/ltg/CoLMA/20191203/*'],
    ['/home/nowcast/data/BoltAlert/mdv/ltg/USPLN/20191203*', '/home/nowcast/data/BoltAlert/archive/test/BoltAlert/mdv/ltg/USPLN/20191203*'],
    ['/home/nowcast/data/BoltAlert/spdb/ltg/CoLMA/20191203.*', '/home/nowcast/data/BoltAlert/archive/test/BoltAlert/spdb/ltg/CoLMA/20191203.*'],
    ['/home/nowcast/data/BoltAlert/spdb/ltg/USPLN/20191203*', '/home/nowcast/data/BoltAlert/archive/test/BoltAlert/spdb/ltg/USPLN/20191203*'],
    ['/home/nowcast/data/BoltAlert/spdb/ltg/NLDN_flashes/20191203.*', '/home/nowcast/data/BoltAlert/archive/test/BoltAlert/spdb/ltg/NLDN_flashes/20191203.*'],
# Changed the date. 1203 already removed.
    ['/var/autofs/mnt/ltg/20191208*.ualf', '/home/nowcast/data/BoltAlert/archive/test/mnt/ltg/20191208*.ualf'],
    ['/home/nowcast/data/BoltAlert/mdv/nsslMosaic3D/merged/20191203/', '/home/nowcast/data/BoltAlert/archive/test/BoltAlert/mdv/nsslMosaic3D/merged/20191203/']

            ] 

if __name__ == '__main__':   # Main program
    for dir_pair in dir_pairs:  # Iterate over directory pairs.
        print('Number of files comparison:')
        for index in range(2):  # Iterate over the two directories.
            command = 'ls ' + dir_pair[index] + ' | wc -w' # The command to get the number of files in the directory
            output = subprocess.getoutput(command) #
            print('# Files:', output, '     ' + dir_pair[index])
            
            
            
        # If the the dirs end in /* do the size comparison, but drop off the /* first.
        # Else of they end in * (but not /*), blow it off altogether.
        # Else if they don't end in * at all, go ahead and do it with the dirs as is
        blow_off_size_comparison = True
        
        if dir_pair[0][-1] == '*' and dir_pair[1][-1] == '*':
            # Both end in *
            if dir_pair[0][-2] == '/' and dir_pair[1][-2] == '/':
                # Both end in /*
                blow_off_size_comparison = False
                # Trim off the /*  from each
                dir_pair[0] = dir_pair[0][:-2]
                dir_pair[1] = dir_pair[1][:-2]
            else:
                # Both end in *, but (at least one) not /*, so blow it off
                pass
        elif dir_pair[0][-1] != '*' and dir_pair[1][-1] != '*':
            # Neither end in *, so leave them as is, and do the compare
            blow_off_size_comparison = False
            
        if not blow_off_size_comparison:
            print('Size comparison:')
            for index in range(2):  # Iterate over the two directories.  range(2) returns a list: [0, 1]
                command = 'du -sh ' + dir_pair[index]  # The command to check size of the directory
                output = subprocess.getoutput(command) #
                print('Size:', output)
        print('--------------------------------------------------------------')
