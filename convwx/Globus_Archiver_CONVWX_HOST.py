#!/usr/local/python-3.7


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
tempDir = "/d1/archiveLisa/GlobusArchiver24hr_CONVWX/"

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
archiveDayDelta=-1

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

archiveItems = {

"ConvWx/mdv/model/hrrr/ncep/vilEchoTop":
    {
    "tarFileName":"%Y%m%d_hrrr_ncep_vilEchoTop.tar",	
    "source": "/home/nowcast/data/ConvWx/mdv/model/hrrr/ncep/vilEchoTop/%Y%m%d/g_*/*",
    "destination": "/gpfs/csfs1/ral/aap/cwx/convwx/%Y/%m%d",	
    "cdDirTar": "/home/nowcast/data",	
    # expected number of files 1513	
    "expectedNumFiles": 1513,	
    # file sizes vary a lot. 1.6 to 2 GB use 15 00 000 000-->	
    "expectedFileSize": 1500000000
    },

#  ************************** 
#  INGEST DIRECTORIES         
#  ************************** 

"mdv/mitll/derived/digitalVil":
    {
    "tarFileName":"%Y%m%d_mitll_digitalVil.tar",	
    "source": "/home/nowcast/data/ConvWx/mdv/mitll/derived/digitalVil/%Y%m%d/*",	
    "destination": "/gpfs/csfs1/ral/aap/cwx/convwx/%Y/%m%d",	
    "cdDirTar": "/home/nowcast/data"	
    },

"mdv/mitll/derived/VILforVerify":
    {
    "tarFileName":"%Y%m%d_mitll_derived_VILforVerify.tar",	
    "source": "/home/nowcast/data/ConvWx/mdv/mitll/derived/VILforVerify/%Y%m%d/*",
    "destination": "/gpfs/csfs1/ral/aap/cwx/convwx/%Y/%m%d",	
    "cdDirTar": "/home/nowcast/data",	
    # expected number of files 96	
    "expectedNumFiles": 96,	
    # file sizes vary a lot. 100MB 100 000 000-->	
    "expectedFileSize": 100000000	
    },

"ConvWx/netCDF/mitll/EchoTop":
    {
    "tarFileName":"%Y%m%d_netCDF.tar",	
    "source": "/home/nowcast/data/ConvWx/netCDF/mitll/EchoTop/%Y%m%d/*",	
    "destination": "/gpfs/csfs1/ral/aap/cwx/convwx/%Y/%m%d",	
    "cdDirTar": "/home/nowcast/data"	
    },
 
"ConvWx/netCDF/mitll/VIL":
    {
    "tarFileName":"%Y%m%d_netCDF.tar",	
    "source": "/home/nowcast/data/ConvWx/netCDF/mitll/VIL/%Y%m%d/*",	
    "destination": "/gpfs/csfs1/ral/aap/cwx/convwx/%Y/%m%d",	
    "cdDirTar": "/home/nowcast/data"	
    },
 
"mdv/mitll/derived/extrapEchoTopsFcst":
     {
     "tarFileName":"%Y%m%d_mitll_fcst.tar",	
    "source": "/home/nowcast/data/ConvWx/mdv/mitll/derived/extrapEchoTopsFcst/%Y%m%d/g_*",	
    "destination": "/gpfs/csfs1/ral/aap/cwx/convwx/%Y/%m%d",	
    "cdDirTar": "/home/nowcast/data",	
    # expected number of files 3265	
    "expectedNumFiles": 3265,	
    # file sizes vary a lot. 410MB to 900MB use 400MB  400 000 000-->	
    "expectedFileSize": 400000000	
    },
 
"mdv/mitll/derived/extrapVilFcst":
    {
    "tarFileName":"%Y%m%d_mitll_fcst.tar",	
    "source": "/home/nowcast/data/ConvWx/mdv/mitll/derived/extrapVilFcst/%Y%m%d/g_*",	
    "destination": "/gpfs/csfs1/ral/aap/cwx/convwx/%Y/%m%d",	
    "cdDirTar": "/home/nowcast/data",	
    # expected number of files 3265	
    "expectedNumFiles": 6530,	
    # file sizes vary a lot. 1.4GB to 3GB use 2GB  2 000 000 000-->	
    "expectedFileSize": 2400000000
    },


#  ****************************
#  BLENDING DIRECTORIES        
#  ****************************

"mdv/blending/hrrr/15min/ncarLpcTile/echoTops":
     {
    "tarFileName":"%Y%m%d_blended_fcst.tar",
    "source": "/home/nowcast/data/ConvWx/mdv/blending/hrrr/15min/ncarLpcTile/echoTops/%Y%m%d/g_*",
    "destination": "/gpfs/csfs1/ral/aap/cwx/convwx/%Y/%m%d",
    "cdDirTar": "/home/nowcast/data",
    # File sizes 3265
    "expectedNumFiles": 3265,
    # Sizes are varying from 180MB - 300MB  Use 100MB or 100 000 000
    "expectedFileSize": 100000000
    },
 
"mdv/blending/hrrr/15min/ncarLpcTile/digitalVil":
    {
    "tarFileName":"%Y%m%d_blended_fcst.tar",
    "source": "/home/nowcast/data/ConvWx/mdv/blending/hrrr/15min/ncarLpcTile/digitalVil/%Y%m%d/g_*",
    "destination": "/gpfs/csfs1/ral/aap/cwx/convwx/%Y/%m%d",
    "cdDirTar": "/home/nowcast/data",
    # File sizes 3265
    "expectedNumFiles": 6530,
    # Sizes are varying from 300MB - 600MB  Use 300MB or 300 000 000
    "expectedFileSize": 400000000
    },
  
"ConvWx/grib/model/hrrr/ncep/hrrr.date/conus":
    {
    "tarFileName":"%Y%m%d_hrrr_t0_wrfsubf.tar",
    "source": "/home/nowcast/data/ConvWx/grib/model/hrrr/ncep/hrrr.%Y%m%d/conus/hrrr.t0*",
    "destination": "/gpfs/csfs1/ral/aap/cwx/convwx/%Y/%m%d",
    "cdDirTar": "/home/nowcast/data",
    #  File size 19 per hour times 9 hours
    "expectedNumFiles": 171,
    # Using 24 hours is 70GB. Since the files are so large it was decided to
    #Only use 8 hours or 9 for ease of archiving.
    #Sizes 24.3GB
    #2.7GB per hour times 9 hours 24.3GB or 240 000 000 000
    "expectedFileSize": 240000000000
    }
 }

