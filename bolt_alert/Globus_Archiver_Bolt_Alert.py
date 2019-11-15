#!/usr/local/python3/bin/python3

######################################
#          GLOBUS CONFIGURATION
######################################

###########
#cospa24
#archive.pl_data_list.BoltAlert_HOST.xml
###########


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
tempDir = "/home/nowcast/data/BoltAlert/archive/"

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


archiveItems = {

"/mdv/nsslMosaic3D/merged":
{
"tarFileName": "%Y%m%d_nsslMosaic3d_merged.tar",
"source": "/home/nowcast/data/BoltAlert/mdv/nsslMosaic3D/merged/%Y%m%d/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/bolt_alert/%Y/%m%d",
"cdDirTar": "/home/nowcast/data/",
#File size 700 ish. 
"expectedNumFiles": 700,
# range from 6GB to 11GB 6 000 000 000 
"expectedFileSize": 6000000000
 },

# All of the BoltAlert_lightning.tar directories came from cospa25 It used to be lightning.tar files
"mdv/ltg/USPLN":
{
"tarFileName": "%Y%m%d_BoltAlert_lightning.tar",
"source": "/home/nowcast/data/BoltAlert/mdv/ltg/USPLN/%Y%m%d/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/bolt_alert/%Y/%m%d",
"cdDirTar": "/home/nowcast/data/",
#File size varies.  Use 2300. 
"expectedNumFiles": 2300,
# 18MB varies 18 000 000 
"expectedFileSize": 18000000
 },

"spdb/ltg/USPLN":
{
"tarFileName": "%Y%m%d_BoltAlert_lightning.tar",
"source": "/home/nowcast/data/BoltAlert/spdb/ltg/USPLN/%Y%m%d*",
"destination": "/gpfs/csfs1/ral/aap/cwx/bolt_alert/%Y/%m%d",
"cdDirTar": "/home/nowcast/data/",
#File size 2 files data & index.   
"expectedNumFiles": 2302,
# varies from 2MB to 6MB use 3 000 000 
"expectedFileSize": 21000000
 },

"ascii/ltgCoLMA":
{
"tarFileName": "%Y%m%d_BoltAlert_lightning.tar",
"source": "/home/nowcast/data/BoltAlert/ascii/ltgCoLMA/%Y%m%d/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/bolt_alert/%Y/%m%d",
"cdDirTar": "/home/nowcast/data/",
#File size 1440 files.
"expectedNumFiles": 3742,
#Size  12MB 12 000 000 
"expectedFileSize": 33000000
 },

"spdb/ltg/CoLMA"
{
"tarFileName": "%Y%m%d_BoltAlert_lightning.tar",
"source": "/home/nowcast/data/BoltAlert/spdb/ltg/CoLMA/%Y%m%d.*",
"destination": "/gpfs/csfs1/ral/aap/cwx/bolt_alert/%Y/%m%d",
"cdDirTar": "/home/nowcast/data/",
#File size 2 files, index & data.
"expectedNumFiles": 3744,
#Size varies from 4 to 68K Use 12KB  012 000 
"expectedFileSize": 330012000
 },

"mdv/ltg/CoLMA"
{
"tarFileName": "%Y%m%d_BoltAlert_lightning.tar",
"source": "/home/nowcast/data/BoltAlert/mdv/ltg/CoLMA/%Y%m%d/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/bolt_alert/%Y/%m%d",
"cdDirTar": "/home/nowcast/data/",
#File size varies21 to 61 files.  use 30
"expectedNumFiles": 3774,
#Size varies from 172K to 492K. Use 200KB  200 000 
"expectedFileSize": 330212000
 },

"mdv/lmaFlashExtent":
{
"tarFileName": "%Y%m%d_BoltAlert_lightning.tar",
"source": "/home/nowcast/data/BoltAlert/mdv/lmaFlashExtent/%Y%m%d/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/bolt_alert/%Y/%m%d",
"cdDirTar": "/home/nowcast/data/",
#File size guess 200 files. New data, directory not up yet.
"expectedNumFiles": 3974,
#Size guess  1MB use 1 000 000 
"expectedFileSize": 331212000
 },


"spdb/ltg/NLDN_flashes":
{
"tarFileName": "%Y%m%d_lightning_NLDN_flashes.tar",
"source": "/home/nowcast/data/BoltAlert/spdb/ltg/NLDN_flashes/%Y%m%d.*",
"destination": "/gpfs/csfs1/ral/aap/cwx/bolt_alert/%Y/%m%d",
"cdDirTar": "/home/nowcast/data/",
#File size guess 2 files. New data, directory not up yet.
"expectedNumFiles": 2,
#Size guess  .5MB 500 000 
"expectedFileSize": 500000
 },

"mnt/ltg/":
{
"tarFileName": "%Y%m%d_lightning_ualf.tar",
"source": "/var/autofs/mnt/ltg/%Y%m%d*.ualf",
"destination": "/gpfs/csfs1/ral/aap/cwx/bolt_alert/%Y/%m%d",
"cdDirTar": "/var/autofs",
#File size guess 1440 files.
"expectedNumFiles": 1440,
#Size guess  5MB 5 000 000 
"expectedFileSize": 5000000
 }


}
