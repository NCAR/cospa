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



#  NWP archive started Jan 2018 and back archived the fall of 20017.

#  ================================= 
#  ============ascii=============== 
#  ================================== 
#extrap  directory  adding back into the blend archive 11/15/18

# The archiver would not calculate expectedFileSize for the first 4.
# Maybe because it was so small?  So they were commented out.
archiveItems = {
    
"ascii/bgWeightsGen24hr/extrap/":
{ 
"tarFileName": "bgWeightsGen24hr_extrap.%Y%m%d.tar",
"source": "/d2/fieldData/ConvWx/ascii/bgWeightsGen24hr/extrap/%Y%m%d.000000.ascii",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/"
#File size is 1 
#"expectedNumFiles": 1,
#Size   use 4KB  4 000 
#"expectedFileSize": 4000
 },

"ascii/bgWeightsGen24hr/model":
{
"tarFileName": "bgWeightsGen24hr_model.%Y%m%d.tar",
"source": "/d2/fieldData/ConvWx/ascii/bgWeightsGen24hr/model/%Y%m%d.000000.ascii",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/"
#File size is 1 
#"expectedNumFiles": 1,
#Size   use 4KB  4 000 
#"expectedFileSize": 4000
 },

"ascii/fssClimoGen24hr/mitllExtrap":
{
"tarFileName": "fssClimoGen24hr_mitllExtrap.%Y%m%d.tar",
"source": "/d2/fieldData/ConvWx/ascii/fssClimoGen24hr/mitllExtrap/%Y%m%d.000000.ascii",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/"
#File size is 1 
#"expectedNumFiles": 1,
#Size   use 4KB  4 000 
#"expectedFileSize": 4000
 },

"ascii/fssClimoGen24hr/ncarLpc":
{
"tarFileName": "fssClimoGen24hr_ncarLpc.%Y%m%d.tar",
"source": "/d2/fieldData/ConvWx/ascii/fssClimoGen24hr/ncarLpc/%Y%m%d.000000.ascii",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/"
#File size is 1 
#"expectedNumFiles": 1,
#Size   use 4KB  4 000 
#"expectedFileSize": 4000
 },

"mdv/blendingDynamic/dynamicWeightsTsmooth":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "dynamicWeightsTsmooth.%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/mdv/blendingDynamic/dynamicWeightsTsmooth/%Y%m%d/*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size  817 most consistent 
"expectedNumFiles": 817,
#Size varies from 109MB to 148MB use 120MB 120 000 000 
"expectedFileSize": 120000000
 },

"ascii/fcstObsDists":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "ascii_fcstObsDists.%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/ascii/fcstObsDists/%Y%m%d/*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size  all over the place 1801 is what it should be 
"expectedNumFiles": 1801,
#Size varies  use 56MB  56 000 000 
"expectedFileSize": 56000000
 },

"ascii/fcstObsDistsEchoTops":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "fcstObsDistsEchoTops.%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/ascii/fcstObsDistsEchoTops/%Y%m%d/*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size  all over the place 1801 is what it should be 
"expectedNumFiles": 1801,
#Size varies  use 28MB  28 000 000 
"expectedFileSize": 28000000
 },

"ascii/climoFcstObsDists":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "climoFcstObsDists.%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/ascii/climoFcstObsDists/%Y%m%d/*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size is 505 
"expectedNumFiles": 505,
#Size varies  use 17MB  17 000 000 
"expectedFileSize": 17000000
 },

"ascii/climoFcstObsDistsEchoTops":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "climoFcstObsDistsEchoTops.%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/ascii/climoFcstObsDistsEchoTops/%Y%m%d/*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size is 505 
"expectedNumFiles": 505,
#Size varies  use 7.3MB  7 300 000 
"expectedFileSize": 7300000
 },


#  ================================= 
#  ============netCDF=============== 
#  ================================== 

"/d2/fieldData/ConvWx/netCDF/mitll/VilMosaicFlags":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "VilMosaicFlags_%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/netCDF/mitll/VilMosaicFlags/%Y%m%d/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size 288 
"expectedNumFiles": 288,
#Size varies 96MB to 106MB use  100 000 
"expectedFileSize": 100000
 },

"/d2/fieldData/ConvWx/netCDF/mitll/EchoTopsMosaicFlags":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "EchoTopsMosaicFlags_%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/netCDF/mitll/EchoTopsMosaicFlags/%Y%m%d/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size 288 
"expectedNumFiles": 288,
#Size varies 137MB to 170MB use  150 000 
"expectedFileSize": 150000
 },

"/d2/fieldData/ConvWx/netCDF/mitll/ConvInitFlagForecast":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "ConvInitFlagForecast_%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/netCDF/mitll/ConvInitFlagForecast/%Y%m%d/*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size 9793 
"expectedNumFiles": 9793,
#Size 2.1GB  use  2 100 000 
"expectedFileSize": 2100000
},

"/d2/fieldData/ConvWx/netCDF/mitll/CwafProbForecastLow/":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "CwafProbForecastLow.%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/netCDF/mitll/CwafProbForecastLow/%Y%m%d/*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size  all over the place 1129 most consistent 
"expectedNumFiles": 1129,
#Size varies 60MB to 90MB use 70MB  70 000 000 
"expectedFileSize": 70000000
 },

"/d2/fieldData/ConvWx/netCDF/mitll/EchoTopsMosaic":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "EchoTopsMosaic.%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/netCDF/mitll/EchoTopsMosaic/%Y%m%d/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size  96 most consistent 
"expectedNumFiles": 96,
#Size varies 40MB to 100MB use 60MB  60 000 000 
"expectedFileSize": 60000000
 },

# JTH commenting these two out.  They will be added for specific lead times
# at the bottom.
# "/d2/fieldData/ConvWx/netCDF/mitll/HeuristicEchoTopsForecast":
#{
#"doStaging": True,
#"doZip": True, 
#"tarFileName": "HeuristicEchoTopsForecast.%Y%m%d.gz.tar",
#"source": "/d2/fieldData/ConvWx/netCDF/mitll/HeuristicEchoTopsForecast/%Y%m%d/*/*",
#"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
#"cdDirTar": "/d2/fieldData/ConvWx/",
##File size  96 most consistent 
#"expectedNumFiles": 96,
##Size varies 100MB to 1.6GB use 700MB  700 000 000 
#"expectedFileSize": 700000000
# },
#
#"/d2/fieldData/ConvWx/netCDF/mitll/HeuristicVilForecast":
#{
#"doStaging": True,
#"doZip": True, 
#"tarFileName": "HeuristicVilForecast.%Y%m%d.gz.tar",
#"source": "/d2/fieldData/ConvWx/netCDF/mitll/HeuristicVilForecast/%Y%m%d/*/*",
#"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
#"cdDirTar": "/d2/fieldData/ConvWx/",
##File size  96 most consistent 
#"expectedNumFiles": 96,
##Size varies 1.6GB to 3.2GB use 1.2GB  1 200 000 000 
#"expectedFileSize": 1200000000
# },

"/d2/fieldData/ConvWx/netCDF/mitll/VilMosaic":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "VilMosaic.%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/netCDF/mitll/VilMosaic/%Y%m%d/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size  96 most consistent 
"expectedNumFiles": 96,
#Size varies 65MB to 126MB use 90MB   90 000 000 
"expectedFileSize": 90000000
 },

#  ================================= 
#  ============mdv=============== 
#  ================================== 

"/d2/fieldData/ConvWx/mdv/blending/hrrr/15min/ncarLpcTileExpand/echoTops":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "hrrr_15min_ncarLpcTileExpand_echoTops_%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/mdv/blending/hrrr/15min/ncarLpcTileExpand/echoTops/%Y%m%d/*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size mostly 3745 
"expectedNumFiles": 3745,
#Size varies 67 - 742MB  use 200MB   200 000 
"expectedFileSize": 200000
 },

"/d2/fieldData/ConvWx/mdv/blending/hrrr/15min/ncarLpcTileExpand/digitalVil":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "hrrr_15min_ncarLpcTileExpand_digitalVil_%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/mdv/blending/hrrr/15min/ncarLpcTileExpand/digitalVil/%Y%m%d/*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size mostly 3745 
"expectedNumFiles": 3745
#Size varies 200MB - 2.2GB  don't use a size  
 },

"/d2/fieldData/ConvWx/mdv/verify/fssGridClimo/mitllExtrap/digitalVil/":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "fssGridClimo_mitllExtrap_digitalVil_%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/mdv/verify/fssGridClimo/mitllExtrap/digitalVil/%Y%m%d/*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size 817 
"expectedNumFiles": 817,
#Size varies 400 - 660MB  use 500MB   500 000 
"expectedFileSize": 500000
 },

"/d2/fieldData/ConvWx/mdv/verify/fssGridClimo/model/hrrr/15min/ncarLpc/digitalVil/":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "fssGridClimo_model_15min_digitalVil_%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/mdv/verify/fssGridClimo/model/hrrr/15min/ncarLpc/digitalVil/%Y%m%d/*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size 817 
"expectedNumFiles": 817,
#Size varies 400 - 650MB  use 500MB   500 000 
"expectedFileSize": 500000
 },

"/d2/fieldData/ConvWx/mdv/model/hrrr/15min/ncarLpc/digitalVil":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "ncarLpc_digitalVi.%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/mdv/model/hrrr/15min/ncarLpc/digitalVil/%Y%m%d/*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size  97 most consistent 
"expectedNumFiles": 97,
#Size varies from 226MB to 1.7GB use 700MB 700 000 000 
"expectedFileSize": 700000000
 },

"/d2/fieldData/ConvWx/mdv/model/hrrr/15min/ncarLpc/echoTops":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "echoTops.%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/mdv/model/hrrr/15min/ncarLpc/echoTops/%Y%m%d/*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size  3265 most consistent 
"expectedNumFiles": 3265,
#Size varies from 180MB to 675MB use 400MB 700 000 000 
"expectedFileSize": 400000000
 },

"/d2/fieldData/ConvWx/mdv/model/hrrr/15min/digitalVilDynCal":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "digitalVilDynCal.%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/mdv/model/hrrr/15min/digitalVilDynCal/%Y%m%d/*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size  1801 most consistent 
"expectedNumFiles": 1801,
#Size varies from 190MB to 675MB use 250MB 250 000 000 
"expectedFileSize": 250000000
 },

"/d2/fieldData/ConvWx/mdv/model/hrrr/15min/echoTopDynCal/":
{
"doStaging": True,
"doZip": True, 
"tarFileName": "echoTopDynCal.%Y%m%d.gz.tar",
"source": "/d2/fieldData/ConvWx/mdv/model/hrrr/15min/echoTopDynCal/%Y%m%d/*/*",
"destination": "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d",
"cdDirTar": "/d2/fieldData/ConvWx/",
#File size  1801 most consistent 
"expectedNumFiles": 1801,
#Size varies from 83MB to 669MB use 150MB 150 000 000 
"expectedFileSize": 150000000
 }
}

# Now add more archiveItems to the dictionary already created above.  These are for specific
# lead times (every half hour).

label_root_echo_tops =  "/d2/fieldData/ConvWx/netCDF/mitll/HeuristicEchoTopsForecast"
label_root_vil =        "/d2/fieldData/ConvWx/netCDF/mitll/HeuristicVilForecast"
source_root_echo_tops = "/d2/fieldData/ConvWx/netCDF/mitll/HeuristicEchoTopsForecast/%Y%m%d/g_*0000/f_000"
source_root_vil =       "/d2/fieldData/ConvWx/netCDF/mitll/HeuristicVilForecast/%Y%m%d/g_*0000/f_000"
tarFileNameEchoTops =   "HeuristicEchoTopsForecast_hr_gentimes.%Y%m%d.gz.tar"
tarFileNameVil =        "HeuristicVilForecast_hr_gentimes.%Y%m%d.gz.tar"
destination =           "/gpfs/csfs1/ral/aap/cwx/nwp/%Y/%Y%m%d"
cdDirTar =              "/d2/fieldData/ConvWx/"
doStaging = True
doZip =     True
expectedNumFiles = 24 # Looks like this needs to be one lead time at a time, cumulatively.
expectedFileSizeEchoTops =  700000000
expectedFileSizeVil      = 1200000000

# etc. for destination, cdDirTar, expectedNumFiles, expectedFileSize
# add all times here
for lead_time in "01800", "03600", "05400", "07200", "09000", "10800", "12600", "14400", "16200", "18000", "19800", "21600", "23400", "25200", "27000", "28800":
    # Create Echo Tops archiveItem for this lead time
    label = label_root_echo_tops + "-" + lead_time
    source = source_root_echo_tops + lead_time + ".nc"
    archiveItem = { "doStaging": doStaging,
                    "doZip" : doZip,
                    "tarFileName" : tarFileNameEchoTops,
                    "source": source,
                    "destination": destination,
                    "cdDirTar": cdDirTar,
                    "expectedNumFiles": expectedNumFiles,
                    "expectedFileSize": expectedFileSizeEchoTops
                  }
    # Add this archiveItem to the dictionary of archiveItems
    archiveItems[label] = archiveItem

    # Create the Vil archiveItem for this lead time
    label = label_root_vil + "-" + lead_time
    source = source_root_vil + lead_time + ".nc"
    archiveItem = { "doStaging": doStaging,
                    "doZip" : doZip,
                    "tarFileName" : tarFileNameVil,
                    "source": source,
                    "destination": destination,
                    "cdDirTar": cdDirTar,
                    "expectedNumFiles": expectedNumFiles,
                    "expectedFileSize": expectedFileSizeVil
                  }
    # Add this archiveItem to the dictionary of archiveItems
    archiveItems[label] = archiveItem
 
    # Increment the number of files for another lead time
    expectedNumFiles += 24
 
# If you want to see the complete list of archiveItems, you can uncomment the following print
# statement, then run this file as a separate program.  Note that it will all be on one line, so 
# it won't be easy to read.    
#print(archiveItems)
