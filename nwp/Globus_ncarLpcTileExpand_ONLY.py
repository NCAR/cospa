#!/usr/bin/env python


######################################
#          GLOBUS CONFIGURATION
######################################


# Imports used in the configuration file
import os


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




#  ================================= 
#  ============mdv=============== 
#  ================================== 

# This one is broken into 3 pieces (g_0*, g_1*, g_2*) just to get around an error with an
# argument list getting too long.

archiveItems = {
    
"/d2/fieldData/ConvWx/mdv/blending/hrrr/15min/ncarLpcTileExpand/echoTops1":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "hrrr_15min_ncarLpcTileExpand_echoTops_%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/mdv/blending/hrrr/15min/ncarLpcTileExpand/echoTops/%Y%m%d/g_0*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size mostly 3745 
"expectedNumFiles": 3745,
#Size varies 67 - 742MB  use 200MB   200 000 
"expectedFileSize": 200000
 },

"/d2/fieldData/ConvWx/mdv/blending/hrrr/15min/ncarLpcTileExpand/echoTops2":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "hrrr_15min_ncarLpcTileExpand_echoTops_%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/mdv/blending/hrrr/15min/ncarLpcTileExpand/echoTops/%Y%m%d/g_1*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size mostly 3745 
"expectedNumFiles": 3745,
#Size varies 67 - 742MB  use 200MB   200 000 
"expectedFileSize": 200000
 },
 
"/d2/fieldData/ConvWx/mdv/blending/hrrr/15min/ncarLpcTileExpand/echoTops3":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "hrrr_15min_ncarLpcTileExpand_echoTops_%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/mdv/blending/hrrr/15min/ncarLpcTileExpand/echoTops/%Y%m%d/g_2*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size mostly 3745 
"expectedNumFiles": 3745,
#Size varies 67 - 742MB  use 200MB   200 000 
"expectedFileSize": 200000
 },
# This one is broken into 3 pieces (g_0*, g_1*, g_2*) just to get around an error with an
# argument list getting too long.
"/d2/fieldData/ConvWx/mdv/blending/hrrr/15min/ncarLpcTileExpand/digitalVil1":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "hrrr_15min_ncarLpcTileExpand_digitalVil_%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/mdv/blending/hrrr/15min/ncarLpcTileExpand/digitalVil/%Y%m%d/g_0*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size mostly 3745 
"expectedNumFiles": 3745
#Size varies 200MB - 2.2GB  don't use a size  
 },

"/d2/fieldData/ConvWx/mdv/blending/hrrr/15min/ncarLpcTileExpand/digitalVil2":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "hrrr_15min_ncarLpcTileExpand_digitalVil_%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/mdv/blending/hrrr/15min/ncarLpcTileExpand/digitalVil/%Y%m%d/g_1*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size mostly 3745 
"expectedNumFiles": 3745
#Size varies 200MB - 2.2GB  don't use a size  
 },

"/d2/fieldData/ConvWx/mdv/blending/hrrr/15min/ncarLpcTileExpand/digitalVil3":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "hrrr_15min_ncarLpcTileExpand_digitalVil_%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/mdv/blending/hrrr/15min/ncarLpcTileExpand/digitalVil/%Y%m%d/g_2*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size mostly 3745 
"expectedNumFiles": 3745
#Size varies 200MB - 2.2GB  don't use a size  
 }
}
