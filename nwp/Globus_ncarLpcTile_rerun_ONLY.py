#!/usr/bin/env python

# *=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
# ** Copyright UCAR (c) 1992 - 2006
# ** University Corporation for Atmospheric Research(UCAR)
# ** National Center for Atmospheric Research(NCAR)
# ** Research Applications Program(RAP)
# ** P.O.Box 3000, Boulder, Colorado, 80307-3000, USA
# ** All rights reserved. Licenced use only.
# ** Do not copy or distribute without authorization.
# *=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*

import os, sys
import string
import time
import calendar
from optparse import OptionParser

def gen_date_list(begin_date, end_date):
    """Generates a list of dates of the form yyyymmdd from a being date to end date
    Inputs:
      begin_date -- such as "20070101"
      end_date -- such as "20070103"
    Returns:
      date_list -- such as ["20070101","20070102","20070103"]
    """
    begin_tm = time.strptime(begin_date, "%Y%m%d")
    end_tm = time.strptime(end_date, "%Y%m%d")
    begin_tv = calendar.timegm(begin_tm)
    end_tv = calendar.timegm(end_tm)
    date_list = []
    for tv in range(begin_tv, end_tv+86400, 86400):
        date_list.append(time.strftime("%Y%m%d", time.gmtime(tv)))
    return date_list                         


def main():
    
    usage_str = " %prog begin_date end_date \n\tNote: begin_date and end_date should be in the format YYYYMMDD"
    parser = OptionParser(usage = usage_str)

    (options, args) = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(2)

    begin_date = args[0]
    end_date = args[1]

    mydatelist = gen_date_list(begin_date, end_date)

    log_dir = "/home/lisag/logs/"

    for mydate in mydatelist:
        command = "/home/lisag/git/GlobusArchiver/GlobusArchiver.py --archiveDateTimeString %s --config /home/lisag/git/cospa/nwp/Globus_ncarLpcTileExpand_ONLY.py | LogFilter -d %s -p GlobusArchiver_ncarLpcTileExpand_ONLY_rerun" % (mydate, log_dir)
        print(command)
        ret = os.system(command)
        if ret != 1:
            print("Error sending up to Globus Campaign Storage")

if __name__ == "__main__":

   main()
             
