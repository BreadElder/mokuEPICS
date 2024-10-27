# $File: //ASP/proc/plat/ioc_templates/trunk/basic_ioc/{ioc_name}App/src/Makefile $
# $Revision: #7 $
# $DateTime: 2022/09/21 16:42:22 $
# Last checked in by: $Author: starritt $
#
TOP=../..

include $(TOP)/configure/CONFIG
include $(PYDEVSUP)/configure/CONFIG_PY

#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = MOKUIOC
# MOKUIOC.dbd will be created and installed
DBD += MOKUIOC.dbd

# MOKUIOC.dbd will be made up from these files:
MOKUIOC_DBD += base.dbd
MOKUIOC_DBD += system.dbd

ifdef BASE_7_0
# We are using EPICS 7.0 or later - pull in PV Access dbd files and libraries.
#
MOKUIOC_DBD += PVAServerRegister.dbd
MOKUIOC_DBD += qsrv.dbd

MOKUIOC_LIBS += nt
MOKUIOC_LIBS += pvAccess
MOKUIOC_LIBS += pvAccessCA
MOKUIOC_LIBS += pvAccessIOC
MOKUIOC_LIBS += pvData
MOKUIOC_LIBS += pvDatabase
MOKUIOC_LIBS += qsrv
endif

# Comment out Asyn, Autosave and or Sequencer support if not required.
#
# Asyn related dbd/libraries.
#
MOKUIOC_DBD += asyn.dbd
MOKUIOC_DBD += drvAsynIPPort.dbd
MOKUIOC_DBD += drvAsynSerialPort.dbd
MOKUIOC_LIBS += asyn

# Autosave related dbd/libraries.
#
MOKUIOC_DBD += asSupport.dbd
MOKUIOC_LIBS += autosave

# Sequencer related dbd/libraries.
#
MOKUIOC_LIBS += seq pv

# Calc related dbd/libraries.
# Needed by and must preceed stream.
#
MOKUIOC_DBD += calcSupport.dbd
MOKUIOC_LIBS += calc

# Sscan related dbd/libraries.
#
MOKUIOC_DBD += sscanSupport.dbd
MOKUIOC_LIBS += sscan

# Stream related dbd/libraries.
#
MOKUIOC_DBD += stream.dbd
MOKUIOC_LIBS += stream

# IOC Status related dbd/libraries.
#
MOKUIOC_DBD += IocStat.dbd
MOKUIOC_LIBS += IocStat

# Signal handling related dbd/libraries (Linux only)
#
MOKUIOC_DBD += signal_catch.dbd
MOKUIOC_LIBS += signal_catch

MOKUIOC_DBD  += pyDevSup.dbd
MOKUIOC_LIBS += pyDevSup$(PY_LD_VER)

# Arbitary process status
#
MOKUIOC_DBD += processStatus.dbd
MOKUIOC_LIBS += processStatus

# Service control
#
MOKUIOC_DBD += service_control.dbd
MOKUIOC_LIBS += service_control

# Include dbd files and libraries from all support applications
# needed by this IOC:
#

# MOKUIOC_registerRecordDeviceDriver.cpp derives from MOKUIOC.dbd
MOKUIOC_SRCS += MOKUIOC_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
MOKUIOC_SRCS_DEFAULT += MOKUIOCMain.cpp
MOKUIOC_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#MOKUIOC_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
MOKUIOC_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
include $(PYDEVSUP)/configure/RULES_PY
#----------------------------------------
#  ADD RULES AFTER THIS LINE

# end
