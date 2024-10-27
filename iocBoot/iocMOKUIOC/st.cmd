#!../../bin/linux-x86_64/MOKUIOC
#
# $File: //ASP/proc/plat/ioc_templates/trunk/basic_ioc/iocBoot/ioc{ioc_name}/st.cmd $
# $Revision: #8 $
# $DateTime: 2022/06/30 13:02:20 $
# Last checked in by: $Author: starritt $
#

## You may have to change MOKUIOC to something else
## everywhere it appears in this file

< envPaths

# Usually set by epics.service script
epicsEnvSet ("IOCNAME", "MOKUIOC")
epicsEnvSet ("IOCSH_PS1","MOKUIOC> ")

cd ${TOP}

## Register all support components
dbLoadDatabase "dbd/MOKUIOC.dbd"
MOKUIOC_registerRecordDeviceDriver pdbbase

py "import mokuEPICS"

# Parameters
# 1  port name
# 2  IP
#
#py "mokuEPICS.createConnection('MOKUDEV', '10.23.234.2')"

## Load record instances
#
# Set hash table size
#
dbPvdTableSize (4096)

# Allow epics service script to initiate clean shutdown by performing
#   caput MOKUIOC:exit.PROC 1
#
dbLoadRecords ("${EPICS_BASE}/db/softIocExit.db", "IOC=${IOCNAME}")

# Load standard bundle build status and IOC (and host) monitoring records.
#
dbLoadRecords ("${BUNDLESTATUS}/db/build.template", "IOC=${IOCNAME}")
dbLoadRecords ("${IOCSTATUS}/db/IocStatus.template", "IOC=${IOCNAME}")

dbLoadTemplate ("db/moku.substitutions")

cd ${TOP}/iocBoot/${IOC}
iocInit

# Catch SIGINT and SIGTERM - do an orderly shutdown
#
catch_sigint
catch_sigterm

# system firewall_update - obsolete
# Install manage_epics_firewall_rules service if needs be.
# Run manage_epics_firewall_rules --help for details.

# Dump all record names
#
dbl > /asp/logs/ioc/${IOCNAME}/${IOC}.dbl

## Autosave monitor set-up.
#
#create_monitor_set ("example.req", 30)

## Start any sequence programs
#seq sncxxx, "param1=value1, param2=value2"

# end
