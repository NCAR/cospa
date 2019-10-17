#!/usr/bin/env python3


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
 
# tempDir is used for:
#     - Staging Location for .tar Files
# Default, $TMPDIR if it is defined, otherwise $HOME if defined, otherwise '.'.
#tempDir = os.path.join(os.getenv("TMPDIR",os.getenv("HOME",".")), "GlobusArchiver-tmp")
tempDir = "/home/nowcast/data/ConvWx/GlobusArchiver48hr_CONVWX"

###############  EMAIL   ##################
# Deliver a report to these email addresses
# Use a list of 3-tuples  ("name", "local-part", "domain")

emailAddresses = [("Lisa Goodrich", "lisag", "ucar.edu")] 

# This is the email address that will be used in the "from" field
fromEmail = emailAddresses[0];

#####################################
##  AUTHENTICATION          
#####################################

# You can define the endpoint directly  
# This default value is the NCAR CampaignStore 
# the value was obtained by running:
# $ globus endpoint search 'NCAR' --filter-owner-id 'ncar@globusid.org' | grep Campaign | cut -f1 -d'      

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

######################
# Archive Date/Time
#
# This is used to set the date/timme of the Archive.
# The date/time can be substituted into all archive-item strings, by using
# standard strftime formatting.

# This value is added (so use a negaative number to assign a date in the past) 
# to now() to find the archive date/time.
archiveDayDelta=-2

# If this is set, it overrides the archiveDayDelta.  If you want to use
# archiveDayDelta to set the Archive Date/Time, make sure this is 
# set to an empty string.  This string must be parseable by one of the
# format strings defined in archiveDateTimeFormats.
archiveDateTimeString=""

# You can add additional strptime
archiveDateTimeFormats=["%Y%m%d","%Y%m%d%H","%Y-%m-%dT%H:%M:%SZ"]

# You may want to keep the tmp area around for debugging
# As of 9/9/19 the archiver won't run if this is 'True'
# For the time being, leave this 'False'
cleanTemp = True

####################################
## ARCHIVE ITEM CONFIGURATION
####################################

# TODO: transfer-args are currently ignored

# do_zip is optional, and defaults to False.  It's also not working as of 9/9/19
# transferLabel is optional, and defaults to the item key + "-%Y%m%d"
# tar_filename is optional and defaults to "".  TAR is only done if tar_filename is a non-empty string
# transferArgs is a placeholder and not yet implemented.


######################
## ConvWx archive
######################


############
# cospa 27
# archive.pl_data_list.CONVWX_HOST_48_hours.xml
############

# **************************** 
# BLENDING DIRECTORIES         
# **************************** 


# this Archive directory needs 48 hours to complete

archiveItems = {
"mdv/verify/fssGridClosestClimo/model/hrrr/15min/ncarLpc/digitalVil":
    {
    "tarFileName":"%Y%m%d_fssGridClosestClimo.tar",
    "source": "/home/nowcast/data/ConvWx/mdv/verify/fssGridClosestClimo/model/hrrr/15min/ncarLpc/digitalVil/%Y%m%d/g_*",
    "destination": "/gpfs/csfs1/ral/aap/cwx/convwx/%Y/%m%d",
    "cdDirTar": "/home/nowcast/data",
    #File sizes 241 
    "expectedNumFiles": 241,
    #Sizes are varying from 51MB - 97MB  Use 50MB or 50 000 000 
    "expectedFileSize": 50000000
    },

# this Archive directory needs 48 hours to complete
"mdv/verify/fssGridClosestClimo/mitllExtrap/digitalVil":
    {
    "tarFileName":"%Y%m%d_fssGridClosestClimo.tar",
    "source": "/home/nowcast/data/ConvWx/mdv/verify/fssGridClosestClimo/mitllExtrap/digitalVil/%Y%m%d/g_*",
    "destination": "/gpfs/csfs1/ral/aap/cwx/convwx/%Y/%m%d",
    "cdDirTar": "/home/nowcast/data",
    #File size 241 
    "expectedNumFiles": 482,
    #Sizes are varying from 78MB - 100MB  Use 70MB or 70 000 000 
    "expectedFileSize": 120000000
    },

# this Archive directory needs 48 hours to complete  
"mdv/blendingDynamic/dynamicWeights":
    {
    "tarFileName":"%Y%m%d_dynamicWeights.tar",
    "source": "/home/nowcast/data/ConvWx/mdv/blendingDynamic/dynamicWeights/%Y%m%d/g_*",
    "destination": "/gpfs/csfs1/ral/aap/cwx/convwx/%Y/%m%d",
    "cdDirTar": "/home/nowcast/data",
    #File size 241.  Use 241 
    "expectedNumFiles": 241,
    #Sizes are varying from 95MB - 107MB  Use 97MB or 97 000 000 
    "expectedFileSize": 97000000
    }

}

