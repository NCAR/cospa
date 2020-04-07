#!/usr/bin/env python3
# Lisa Goodrich

# Created when Campaign Storage filled up in March 2020.
# The Heuristic directories took up a lot of room and most of the data wasn't needed.  This was used to switch to a smaller data set, hourly gentimes and a subset of the lead times.  The tar file name has changed from:
# HeuristicEchoTopsForecast.%Y%m%d.gz.tar  to HeuristicEchoTopsForecast_hr_gentimes.%Y%m%d.gz.tar
# HeuristicVilForecast.%Y%m%d.gz.tar to HeuristicVilForecast_hr_gentimes.%Y%m%d.gz.tar
#Older data, 1/1/2019 - 3/7/2020 had to be brought down from the Campaign Storage, opened and re-archived with the smaller data set.

######################################
#          GLOBUS CONFIGURATION
######################################


# Imports used in the configuration file
import os
import socket
import datetime


#####################################
## GENERAL CONFIGURATION
#####################################

# GlobusArchiver.py submits one task to Globus
# This is used to identify the task on the Globus Web API
# Through painful trial and error, I have determined this cannot have a period in it.

taskLabel =  f"Blend_archiver-%Y%m%d"

# I would recommend uncommenting the taskLabel definition below, but because of the way ConfigMaster currently works
# I cannot have __file__ in the default params.

# This uses the config file name as part of the label, but strips the extension and replaces '.' with '_'
#taskLabel =  f"{(os.path.splitext(os.path.basename(__file__))[0]).replace('.','_')}-%Y%m%d"

###############  TEMP DIR   ##################

# tempDir is used for:
#     - Staging Location for .tar Files

# Default, $TMPDIR if it is defined, otherwise $HOME if defined, otherwise '.'.
#tempDir = os.path.join(os.getenv("TMPDIR",os.getenv("HOME",".")), "GlobusArchiver-tmp")
tempDir = "/d2/fieldData/ConvWx/GlobusArchive"
# You may want to keep the tmp area around for debugging
cleanTemp = True

###############  EMAIL   ##################

# Deliver a report to these email addresses
# Use a list of 3-tuples  ("name", "local-part", "domain")
emailAddresses = [("Lisa Goodrich", "lisag", "ucar.edu")] 

# This is the email address that will be used in the "from" field
fromEmail = emailAddresses[0]

# Format of email subject line. Can refer to errors, archiveDate, configFile, and host
#  notated in curly braces.
emailSubjectFormat = "{errors} with GlobusArchiver on {host} - {configFile} - {archiveDate}"

# format of date timestamp in email subject. This format will be used to substitute
# {archiveDate} in the emailSubjectFormat
emailSubjectDateFormat = "%Y/%m/%d"


#####################################
##  AUTHENTICATION          
#####################################

# You can define the endpoint directly  
# This default value is the NCAR CampaignStore 
# the value was obtained by running:
# $ globus endpoint search 'NCAR' --filter-owner-id 'ncar@globusid.org' | grep Campaign | cut -f1 -d' '
archiveEndPoint = "6b5ab960-7bbf-11e8-9450-0a6d4e044368"

# The refresh token is what lets you use globus without authenticating every time.  We store it in a local file.
# !!IMPORTANT!!!
# You need to protect your Refresh Tokens. 
# They are an infinite lifetime credential to act as you.
# Like passwords, they should only be stored in secure locations.
# e.g. placed in a directory where only you have read/write access
globusTokenFile = os.path.join(os.path.expanduser("~"),".globus-ral","refresh-tokens.json")


####################################
## ARCHIVE RUN CONFIGURATION
####################################

#########  Archive Date/Time  #################
#
# This is used to set the date/time of the Archive.
# The date/time can be substituted into all archive-item strings, by using
# standard strftime formatting.

# This value is added (so use a negative number to assign a date in the past) 
# to now() to find the archive date/time.
archiveDayDelta=-1

# If this is set, it overrides the archiveDayDelta.  If you want to use
# archiveDayDelta to set the Archive Date/Time, make sure this is 
# set to an empty string.  This string must be parseable by one of the
# format strings defined in archiveDateTimeFormats.
archiveDateTimeString=""

# You can add additional strptime formats
archiveDateTimeFormats=["%Y%m%d","%Y%m%d%H","%Y-%m-%dT%H:%M:%SZ"]

#####################################
#  ARCHIVE SUBMISSION CONFIGURATION
#####################################

# Set to False to process data but don't actually submit the tasks to Globus
submitTasks = True

# Number of seconds to wait to see if transfer completed
# Report error if it doesn't completed after this time
# Default is 21600 (6 hours)
transferStatusTimeout = 6*60*60

####################################
## ARCHIVE ITEM CONFIGURATION
####################################
# TODO: better documentation of these fields in archiveItems

# source 

# doZip        is optional, and defaults to False
# tar_filename is optional and defaults to "".  TAR is only done if tar_filename is a non-empty string
#              if multiple archiveItems have the same tar_filename, 
# transferArgs is a placeholder and not yet implemented.

# use sync_level to specify when files are overwritten:

# "exists"   - If the destination file is absent, do the transfer.
# "size"     - If destination file size does not match the source, do the transfer.
# "mtime"    - If source has a newer modififed time than the destination, do the transfer.
# "checksum" - If source and destination contents differ, as determined by a checksum of their contents, do the transfer. 



#  NWP archive started Jan 2018 and back archived the fall of 20017.

# Modified Heuristic Forecasts.  Smaller size.

label_root_echo_tops =  "/d2/fieldData/ConvWx/netCDF/mitll/HeuristicEchoTopsForecast"
label_root_vil =        "/d2/fieldData/ConvWx/netCDF/mitll/HeuristicVilForecast"
source_root_echo_tops = "/d1/fieldData/ConvWx/archive/convert/netCDF/mitll/HeuristicEchoTopsForecast/%Y%m%d/g_*0000/f_000"
source_root_vil =       "/d1/fieldData/ConvWx/archive/convert/netCDF/mitll/HeuristicVilForecast/%Y%m%d/g_*0000/f_000"
tarFileNameEchoTops =   "HeuristicEchoTopsForecast_hr_gentimes.%Y%m%d.gz.tar"
tarFileNameVil =        "HeuristicVilForecast_hr_gentimes.%Y%m%d.gz.tar"
destination =           "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d"
cdDirTar =              "/d1/fieldData/ConvWx/archive/convert/"
doStaging = True
doZip =     True
expectedNumFiles = 24 # Looks like this needs to be one lead time at a time, cumulatively.
expectedFileSizeEchoTops =  700000000
expectedFileSizeVil      = 1200000000

archiveItems = {} # Start with empty dictionary

# etc. for destination, cdDirTar, expectedNumFiles, expectedFileSize
# add all times here
for lead_time in "01800", "03600", "05400", "07200", "09000", "10800", "12600", "14400", "16200", "18000", "19800", "21600", "23400", "25200", "27000", "28800":
    # Create Echo Tops archiveItem for this lead time
    label = label_root_echo_tops + "-" + lead_time
    source = source_root_echo_tops + lead_time + ".nc"
    
    # Add this archiveItem to the dictionary of archiveItems
    archiveItems[label] = { "doStaging": doStaging,
                            "doZip" : doZip,
                            "tarFileName" : tarFileNameEchoTops,
                            "source": source,
                            "destination": destination,
                            "cdDirTar": cdDirTar,
                            "expectedNumFiles": expectedNumFiles,
                            "expectedFileSize": expectedFileSizeEchoTops
                          }


    # Create the Vil archiveItem for this lead time
    label = label_root_vil + "-" + lead_time
    source = source_root_vil + lead_time + ".nc"
    
    # Add this archiveItem to the dictionary of archiveItems
    archiveItems[label] = { "doStaging": doStaging,
                            "doZip" : doZip,
                            "tarFileName" : tarFileNameVil,
                            "source": source,
                            "destination": destination,
                            "cdDirTar": cdDirTar,
                            "expectedNumFiles": expectedNumFiles,
                            "expectedFileSize": expectedFileSizeVil
                          }

    # Increment the number of files for another lead time
    expectedNumFiles += 24

#print('-------------------------------------------- archiveItems ------------------------------------------')
#print(archiveItems)
#print('----------------------------------------------------------------------------------------------------')

