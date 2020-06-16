#!/usr/bin/env python

######################################
#          GLOBUS CONFIGURATION
######################################

###########
#cospa23 6/20 now on cospa17
# Globus_Archiver_Epoch_Ops.py
###########


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

taskLabel =  f"Epoch_Ops_cospa17-daily-72-hour-archiver-%Y%m%d"

# I would recommend uncommenting the taskLabel definition below, but because of the way ConfigMaster currently works
# I cannot have __file__ in the default params.

# This uses the config file name as part of the label, but strips the extension and replaces '.' with '_'
#taskLabel =  f"{(os.path.splitext(os.path.basename(__file__))[0]).replace('.','_')}-%Y%m%d"

###############  TEMP DIR   ##################

# tempDir is used for:
#     - Staging Location for .tar Files

# Default, $TMPDIR if it is defined, otherwise $HOME if defined, otherwise '.'.
#tempDir = os.path.join(os.getenv("TMPDIR",os.getenv("HOME",".")), "GlobusArchiver-tmp")
tempDir = "/d1/archiver/"

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
archiveDayDelta=-3

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


archiveItems = {
    
"cmorph/3hr_data":
{
"tarFileName": "%Y%m%d_cmorph.tar",
"source": "/d1/fieldData/EpochOps/mdv/cmorph/3hr/%Y%m%d/",
"destination": "/gpfs/csfs1/ral/aap/cwx/epoch_ops/%Y/%m%d",
"cdDirTar": "/d1/fieldData",
#File sizes are 8 files 
"expectedNumFiles": 8,
#Sizes are 2.5MB 
"expectedFileSize": 2500000
 },

"/mdv/cmorph/3hr_data":
{
"tarFileName": "%Y%m%d_cmorph_climo.tar",
"source": "/d1/fieldData/EpochOps/mdv/cmorph/climo_3hr_ge0.667_30days/%Y%m%d/",
"destination": "/gpfs/csfs1/ral/aap/cwx/epoch_ops/%Y/%m%d",
"cdDirTar": "/d1/fieldData",
#File sizes are 4 files 
"expectedNumFiles": 4,
#Sizes are 140-190KB 
"expectedFileSize": 1500
 },

# data all * directories (20 total): gep01/ gep02/ gep03/
 # gep04/ gep05/ gep06/ gep07/ gep08/ gep09/ gep10/ gep11/ gep12/ gep13/ gep14/
 # gep15/ gep16/ gep17/ gep18/ gep19/ gep20/ 

"model/cmce":
{
"tarFileName": "%Y%m%d_cmce.tar",
"source": "/d1/fieldData/EpochOps/mdv/model/cmce/gep*/%Y%m%d/g_*",
"destination": "/gpfs/csfs1/ral/aap/cwx/epoch_ops/%Y/%m%d",
"cdDirTar": "/d1/fieldData",
#File sizes are 360 files 
"expectedNumFiles": 360,
#Sizes are(5MB per file, 2 per day per 20 directories) 50MB 
"expectedFileSize": 50000000
 },

"/mdv/model/cmceProbCloudTopOpt":
{
"tarFileName": "%Y%m%d_cmceProbCloudTopOpt.tar",
"source": "/d1/fieldData/EpochOps/mdv/model/cmceProbCloudTopOpt/%Y%m%d/g_*",
"destination": "/gpfs/csfs1/ral/aap/cwx/epoch_ops/%Y/%m%d",
"cdDirTar": "/d1/fieldData",
#File sizes are 27 files some of the time 
"expectedNumFiles": 27,
#Sizes are 1-6MB 
"expectedFileSize": 1000000
 },

"/mdv/model/cmceProbOpt":
{
"tarFileName": "%Y%m%d_cmceProbOpt.tar",
"source": "/d1/fieldData/EpochOps/mdv/model/cmceProbOpt/%Y%m%d/g_*",
"destination": "/gpfs/csfs1/ral/aap/cwx/epoch_ops/%Y/%m%d",
"cdDirTar": "/d1/fieldData",
#File sizes are 27 files some of the time
"expectedNumFiles": 27,
#Sizes are 1.9MB 
"expectedFileSize": 1900000
 },

"/mdv/model/epoch":
{
"tarFileName": "%Y%m%d_mdv_model_epoch.tar",
"source": "/d1/fieldData/EpochOps/mdv/model/epoch/%Y%m%d/g_*",
"destination": "/gpfs/csfs1/ral/aap/cwx/epoch_ops/%Y/%m%d",
"cdDirTar": "/d1/fieldData",
#File sizes are 36 files  
"expectedNumFiles": 36,
#Sizes are 1.1-1.3MB 
"expectedFileSize": 1100000
 },

"/mdv/model/epochCCT":
{
"tarFileName": "%Y%m%d_mdv_model_epochCCT.tar",
"source": "/d1/fieldData/EpochOps/mdv/model/epochCCT/%Y%m%d/g_*",
"destination": "/gpfs/csfs1/ral/aap/cwx/epoch_ops/%Y/%m%d",
"cdDirTar": "/d1/fieldData",
#File sizes are 36 files  
"expectedNumFiles": 36,
#Sizes are 650-768KB 
"expectedFileSize": 650000
 },

"/mdv/model/epochOpt":
{
"tarFileName": "%Y%m%d_mdv_model_epochOpt.tar",
"source": "/d1/fieldData/EpochOps/mdv/model/epochOpt/%Y%m%d/g_*",
"destination": "/gpfs/csfs1/ral/aap/cwx/epoch_ops/%Y/%m%d",
"cdDirTar": "/d1/fieldData",
#File sizes are 41 files 
"expectedNumFiles": 41,
#Sizes are 1.1 1.3MB 
"expectedFileSize": 1100000
 },

"/mdv/model/epochProbCloudTopOpt":
{
"tarFileName": "%Y%m%d_mdv_model_epochProbCloudTopOpt.tar",
"source": "/d1/fieldData/EpochOps/mdv/model/epochProbCloudTopOpt/%Y%m%d/g_*",
"destination": "/gpfs/csfs1/ral/aap/cwx/epoch_ops/%Y/%m%d",
"cdDirTar": "/d1/fieldData",
#File sizes are 41 files 
"expectedNumFiles": 41,
#Sizes are 2.1 2.4MB 
"expectedFileSize": 2100000
 },

# This next section can now be archived together.  

"model/gefs":
#gep00 thru gep20   
{
"tarFileName": "%Y%m%d_gefs_gep.tar",
"source": "/d1/fieldData/EpochOps/mdv/model/gefs/gep*/%Y%m%d/g_*",
"destination": "/gpfs/csfs1/ral/aap/cwx/epoch_ops/%Y/%m%d",
"cdDirTar": "/d1/fieldData",
#File size 720 ls */20151230/* | wc -w  
"expectedNumFiles": 720,
#Sizes are 760MB per directory, 80 directories 
"expectedFileSize": 76000000
 },

"/mdv/model/gefsProbCloudTopOpt":
{
"tarFileName": "%Y%m%d_mdv_model_gefsProbCloudTopOpt.tar",
"source": "/d1/fieldData/EpochOps/mdv/model/gefsProbCloudTopOpt/%Y%m%d/g_*",
"destination": "/gpfs/csfs1/ral/aap/cwx/epoch_ops/%Y/%m%d",
"cdDirTar": "/d1/fieldData",
#File sizes are 36 files 
"expectedNumFiles": 36,
#Sizes are mostly 12MB 
"expectedFileSize": 12000000
 },

"/mdv/model/gefsProbOpt":
{
"tarFileName": "%Y%m%d_mdv_model_gefsProbOpt.tar",
"source": "/d1/fieldData/EpochOps/mdv/model/gefsProbOpt/%Y%m%d/g_*",
"destination": "/gpfs/csfs1/ral/aap/cwx/epoch_ops/%Y/%m%d",
"cdDirTar": "/d1/fieldData",
#File sizes are 36 files 
"expectedNumFiles": 36,
#Sizes range from 1.4 -2.7MBB 
"expectedFileSize": 2600000
 },

"/spdb/cmceThresh":
{
"tarFileName": "%Y%m%d_spdb_cmceThresh.tar",
"source": "/d1/fieldData/EpochOps/spdb/cmceThresh/%Y%m%d*",
"destination": "/gpfs/csfs1/ral/aap/cwx/epoch_ops/%Y/%m%d",
"cdDirTar": "/d1/fieldData",
#File sizes are 2 files  
"expectedNumFiles": 2,
#Sizes are 30KB 
"expectedFileSize": 30000
 },

"/spdb/cmceThreshCtop30":
{
"tarFileName": "%Y%m%d_spdb_cmceThreshCtop30.tar",
"source": "/d1/fieldData/EpochOps/spdb/cmceThreshCtop30/%Y%m%d*",
"destination": "/gpfs/csfs1/ral/aap/cwx/epoch_ops/%Y/%m%d",
"cdDirTar": "/d1/fieldData",
#File sizes are 2 files  
"expectedNumFiles": 2,
#Sizes are 30KB 
"expectedFileSize": 30000
 },

"/spdb/cmceThreshCtop35":
{
"tarFileName": "%Y%m%d_spdb_cmceThreshCtop35.tar",
"source": "/d1/fieldData/EpochOps/spdb/cmceThreshCtop35/%Y%m%d*",
"destination": "/gpfs/csfs1/ral/aap/cwx/epoch_ops/%Y/%m%d",
"cdDirTar": "/d1/fieldData",
#File sizes are 2 files  
"expectedNumFiles": 2,
#Sizes are 30KB 
"expectedFileSize": 30000
 },

"/spdb/cmceThreshCtop40":
{
"tarFileName": "%Y%m%d_spdb_cmceThreshCtop40.tar",
"source": "/d1/fieldData/EpochOps/spdb/cmceThreshCtop40/%Y%m%d*",
"destination": "/gpfs/csfs1/ral/aap/cwx/epoch_ops/%Y/%m%d",
"cdDirTar": "/d1/fieldData",
#File sizes are 2 files  
"expectedNumFiles": 2,
#Sizes are 30KB 
"expectedFileSize": 30000
 },

"/spdb/gefsThresh":
{
"tarFileName": "%Y%m%d_spdb_gefsThresh.tar",
"source": "/d1/fieldData/EpochOps/spdb/gefsThresh/%Y%m%d*",
"destination": "/gpfs/csfs1/ral/aap/cwx/epoch_ops/%Y/%m%d",
"cdDirTar": "/d1/fieldData",
#File sizes are 2 files  
"expectedNumFiles": 2,
#Sizes are 40KB 
"expectedFileSize": 40000
 },

"/spdb/gefsThreshCtop30":
{
"tarFileName": "%Y%m%d_spdb_gefsThreshCtop30.tar",
"source": "/d1/fieldData/EpochOps/spdb/gefsThreshCtop30/%Y%m%d*",
"destination": "/gpfs/csfs1/ral/aap/cwx/epoch_ops/%Y/%m%d",
"cdDirTar": "/d1/fieldData",
#File sizes are 2 files  
"expectedNumFiles": 2,
#Sizes are 40KB ish
"expectedFileSize": 40000
 },

"/spdb/gefsThreshCtop35":
{
"tarFileName": "%Y%m%d_spdb_gefsThreshCtop35.tar",
"source": "/d1/fieldData/EpochOps/spdb/gefsThreshCtop35/%Y%m%d*",
"destination": "/gpfs/csfs1/ral/aap/cwx/epoch_ops/%Y/%m%d",
"cdDirTar": "/d1/fieldData",
#File sizes are 2 files  
"expectedNumFiles": 2,
#Sizes are 40KB ish
"expectedFileSize": 40000
 },

"/spdb/gefsThreshCtop40":
{
"tarFileName": "%Y%m%d_spdb_gefsThreshCtop40.tar",
"source": "/d1/fieldData/EpochOps/spdb/gefsThreshCtop40/%Y%m%d*",
"destination": "/gpfs/csfs1/ral/aap/cwx/epoch_ops/%Y/%m%d",
"cdDirTar": "/d1/fieldData",
#File sizes are 2 files  
"expectedNumFiles": 2,
#Sizes are 40KB ish
"expectedFileSize": 40000
 }


}
