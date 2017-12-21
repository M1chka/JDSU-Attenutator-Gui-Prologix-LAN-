#Code to connect and talk to the JDSU Attenuator using the Prologix TCP/IP GPIB device#
from wanglib import prologix

class Attenuator:
    def open(self, ip):
        #connect to attenuator using its IP address#
        print('connecting')
        self.plx = prologix.prologix_ethernet(ip)
        print('done')

    def setAtt(self,att):
        #set attenuation in dB#
        self.plx.write('ATT %s' % str(att))

    def getAtt(self):
        #get attenuation in dB#
        return float(self.plx.ask('ATT?'))

    def setWVL(self,wvl):
        #set WVL in nm#
        self.plx.write('WVL %sNM' % str(wvl))

    def getWVL(self):
        #get set WVL in nm#
        return float(self.plx.ask('WVL?'))*10**9

    def getWVLbound(self):
        #get WVK boundries of device in nm#
        minwvl=int(float(self.plx.ask('WVL? MIN'))*10**9)
        maxwvl=int(float(self.plx.ask('WVL? MAX'))*10**9)
        return minwvl,maxwvl

    def write(self,text):
        #write custom command to Attenuator#
        self.plx.write('%s' % text)

    def ask(self,text):
        #Ask custom command to Attenuator#
        self.plx.ask('%s' % text)