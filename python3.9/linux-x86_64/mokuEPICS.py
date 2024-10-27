### Support for Liquid Instruments Moku devices

from moku.instruments import Oscilloscope
from moku.instruments import SpectrumAnalyzer
import functools
import sys
import time

import devsup
from devsup.hooks import addHook
from devsup.util import StoppableThread

from weakref import WeakValueDictionary

# print to standard error.
#
errput = functools.partial(print, file=sys.stderr)

# Actual Driver to the moku, connects and configures the unit
class MokuConnection (StoppableThread):

    """ This class represents a moku connection. """

    OscCh1_data = []
    OscCh2_data = []
    OscCh3_data = []
    OscCh4_data = []
    OscTime_data = []

    SpecAnCh1_data = []
    SpecAnCh2_data = []
    SpecAnCh3_data = []
    SpecAnCh4_data = []
    SpecAnFreq_data = []

    port_name_map = {}
    # device setup
    DesInstrument = "Current"
    Curinstrument = "Oscilloscope"
    ip = '10.23.234.2'

    # do a settings thing when first setup
    SettingChanged = 1

    # device Defaults
    extnClk = 0 # external clock disabled
    aquire = 1

    #instrument defaults
    scope_default = 0
    OscAcquire = 1
    oscTimebaseLeft = -10e-3
    oscTimebaseRight = 10e-3
    oscDisableCh1 = 0
    oscDisableCh2 = 0
    oscDisableCh3 = 0
    oscDisableCh4 = 0

    # Spec An
    SpecAnAcquire = 1

    ## default connection is scope
    m = Oscilloscope(ip, force_connect=True)

    def __init__(self, name):

        super(MokuConnection, self).__init__()

        # The record list is a dictionary of _Record objects, indexed by
        # the record name. Technically this is a Moku_Record object associated
        # with the a devsup.db.Record object which is itself associated with
        # the actual EPICS record.
        #
        self._record_list = {}

        # Add this connection instance to the connection map.
        #
        MokuConnection.port_name_map[name] = self

        # Ensure the thread starts and stops nicely.
        #
        addHook('AfterIocRunning', self.start)
        addHook('AtIocExit', self.join)

        # Print a friendly message for the IOC shell
        #
        print(f"{self} connection created")


    def run(self):

        print("Starting the EPICS moku driver")

        #get the admin data at startup
        self.startupQuery()
            

        while self.shouldRun():
            # do the regular top level tasks
            #regularQuery()
            if self.DesInstrument == "Current":
                # go into the individual instrument tasks
                if self.Curinstrument == "Oscilloscope":
                    self.mokuOscilloscope()
                elif self.Curinstrument == "Spectrum Analyzer":
                    self.mokuSpecAn()
                else:
                    pass
            else:
                self.Curinstrument = self.DesInstrument
                self.m.relinquish_ownership()
                print(self.Curinstrument)
                time.sleep(4)
                
                if self.Curinstrument == "Oscilloscope":
                    self.m = Oscilloscope(self.ip, force_connect=True)
                    self.DesInstrument = "Current"
                elif self.Curinstrument == "Spectrum Analyzer":
                    
                    self.m = SpectrumAnalyzer(self.ip, force_connect=True)
                    self.DesInstrument = "Current"
                    
                else:
                    pass


    def startupQuery(self):
        # get the last cal date
        date = self.m.calibration_date()
        self.calDate = date["calibration_date"]

        # details of the device
        ver = self.m.describe()
        self.firmwareVer = ver["firmware"]
        self.versionAPI = ver["version"]
        self.hardwareMod = ver["hardware"]

        self.serialNumber = self.m.serial_number()
        
        self.devName = self.m.name()



    def regularQuery(self):
        pass
        ##### set settings
        # only go through this if the settings have changed
        # if self.SettingChanged:
        #     self.m.set_external_clock(self.extnClk)

        # ##### get Readbacks
        #  clk = self.m.get_extrnal_clock()
        #  self.extnClkRBV = clk["external"]

    def mokuSpecAn(self):
        
        if self.SpecAnAcquire:
            self.m.set_span(0,50e3)
            self.m.set_rbw("Auto")
            data = self.m.get_data()

            self.SpecAnCh1_data = data["ch1"]
            self.SpecAnCh2_data = data["ch2"]
            self.SpecAnCh3_data = data["ch3"]
            self.SpecAnCh4_data = data["ch4"]
            self.SpecAnFreq_data = data["frequency"]


    def mokuOscilloscope(self):
        
        #setup the scope settings
        self.OscilloscopeSettings()

        if self.OscAcquire:
            # probe the data
            data = self.m.get_data()
            
            #extract the data
            if ~self.oscDisableCh1:
                self.OscCh1_data = data["ch1"]
            if ~self.oscDisableCh2:
                self.OscCh2_data = data["ch2"]
            if ~self.oscDisableCh3:
                self.OscCh3_data = data["ch3"]
            if ~self.oscDisableCh4:
                self.OscCh4_data = data["ch4"]
            self.OscTime_data = data["time"]

    def OscilloscopeSettings(self):
        if self.scope_default:
            self.m.set_defaults()
        else:
            #trigger settings
            self.m.set_trigger(type="Edge", source="Input4",level=1)
            self.m.set_timebase(self.oscTimebaseLeft, self.oscTimebaseRight)
            
            if self.oscDisableCh1:
                self.m.disable_input(1)

            if self.oscDisableCh2:
                self.m.disable_input(2)

            if self.oscDisableCh3:
                self.m.disable_input(3)

            if self.oscDisableCh4:
                self.m.disable_input(4)

            #print(self.oscTimebaseLeft)
            #print(self.oscTimebaseRight)
            #self.m.set_source(1, "Input1")
    
    
    #self.intscan.interrupt()



#generate a list to track connections
#_mokus = WeakValueDictionary()
M = MokuConnection("MOKU")

# See if we already have this connection
# def getMoku(name):
#     try:
#         print("Connection Exists")
#         return _mokus[name]
#     except KeyError:
#         print("Making new connection")
#         M = MokuConnection(name)
#         _mokus[name] = M
#         return M

# monitor and change settings for the Mouku, connector to the PVs
class MokuWatcher(object):

    def __init__(self, rec, args):
        mokuPort, name = args.split(" ", 1)

        self.port = mokuPort
        self.mokuConn = M#getMoku(mokuPort)
        self.attr = name
        self.last = None

        #self.allowScan = self.mokuConn.intscan.add
        self.process = getattr(self, name)
        try:
            rec.UDF = 0
        except AttributeError:
            pass
    def detach(self, rec):
        pass
    
    #return the port string
    def getPort(self, rec, report):
        rec.VAL = self.port

    def getfwVer(self, rec, report):
        rec.VAL = self.mokuConn.firmwareVer

    def gethwMod(self, rec, report):
        rec.VAL = self.mokuConn.hardwareMod

    def getapiVer(self, rec, report):
        rec.VAL = self.mokuConn.versionAPI
    
    def getCalDate(self, rec, report):
        rec.VAL = self.mokuConn.calDate

    def getSerNo(self, rec, report):
        rec.VAL = self.mokuConn.serialNumber
        
    def getName(self, rec, report):
        rec.VAL = self.mokuConn.devName

    def getExtnClk(self, rec, report):
        rec.VAL = self.mokuConn.extnClkRBV

    def setExtnClk(self, rec, report):
        self.mokuConn.extnClk = rec.VAL
    
    def getOscDataCh1(self, rec, report):
        rec.VAL = self.mokuConn.OscCh1_data

    def getOscDataCh2(self, rec, report):
        rec.VAL = self.mokuConn.OscCh2_data
    
    def getOscDataCh3(self, rec, report):
        rec.VAL = self.mokuConn.OscCh3_data
    
    def getOscDataCh4(self, rec, report):
        rec.VAL = self.mokuConn.OscCh4_data

    def getOscDataTime(self, rec, report):
        rec.VAL = self.mokuConn.OscTime_data

    def setOscTimebaseLeft(self, rec, report):
        if rec.VAL < self.mokuConn.oscTimebaseRight:
            self.mokuConn.oscTimebaseLeft = rec.VAL

    def setOscTimebaseRight(self, rec, report):
        if rec.VAL > self.mokuConn.oscTimebaseLeft:
            self.mokuConn.oscTimebaseRight = rec.VAL

    def setOscDisableCh1(self, rec, report):
        self.mokuConn.oscDisableCh1 = rec.VAL

    def setOscDisableCh2(self, rec, report):
        self.mokuConn.oscDisableCh2 = rec.VAL
    
    def setOscDisableCh3(self, rec, report):
        self.mokuConn.oscDisableCh3 = rec.VAL

    def setOscDisableCh4(self, rec, report):
        self.mokuConn.oscDisableCh4 = rec.VAL

    def chngInstOsc(self, rec, report):
        if(rec.VAL):
            self.mokuConn.DesInstrument = "Oscilloscope"
    
    def chngInstSpecAn(self, rec, report):
        if(rec.VAL):
            self.mokuConn.DesInstrument = "Spectrum Analyzer"

    def getSpecAnDataCh1(self, rec, report):
        rec.VAL = self.mokuConn.SpecAnCh1_data

    def getSpecAnDataCh2(self, rec, report):
        rec.VAL = self.mokuConn.SpecAnCh2_data
    
    def getSpecAnDataCh3(self, rec, report):
        rec.VAL = self.mokuConn.SpecAnCh3_data
    
    def getSpecAnDataCh4(self, rec, report):
        rec.VAL = self.mokuConn.SpecAnCh4_data

    def getOscDataFreq(self, rec, report):
        rec.VAL = self.mokuConn.SpecAnFreq_data

# used in the IOC build, MokuWatcher is the function used for PVs
build = MokuWatcher  



        
            
            
            