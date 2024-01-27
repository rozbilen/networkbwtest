#!/usr/bin/env python

from datetime import datetime
import time
import math
from tools import *

INTERVAL = 1            #   1 second
AVG_LOW_PASS = 0.2      #   Complemetary Filter

ifaces = {}

print "Loading Network Interfaces"
idata = GetNetworkInterfaces()
print "Filling tables"
for eth in idata:
    ifaces[eth["interface"]] = {
        "rxrate"            :   0,
        "txrate"            :   0,
        "avgrx"             :   0,
        "avgtx"             :   0,
        "toptx"             :   0,
        "toprx"             :   0,
        "sendbytes"         :   eth["tx"]["bytes"],
        "recvbytes"         :   eth["rx"]["bytes"],
        "rxdroppedpackets"  :   eth["rx"]["drop"],
        "txdroppedpackets"  :   eth["tx"]["drop"],
        "rxdroprate"        :   0,
        "txdroprate"        :   0        
    }
    
while True:
    idata = GetNetworkInterfaces()
    for eth in idata:
        if eth["interface"] == "aux":
            #   Calculate the Rate
            ifaces[eth["interface"]]["rxrate"]             =   (eth["rx"]["bytes"] - ifaces[eth["interface"]]["recvbytes"]) / INTERVAL
            ifaces[eth["interface"]]["txrate"]             =   (eth["tx"]["bytes"] - ifaces[eth["interface"]]["sendbytes"]) / INTERVAL
                                                           
            #   Set the rx/tx bytes                        
            ifaces[eth["interface"]]["recvbytes"]          =   eth["rx"]["bytes"]
            ifaces[eth["interface"]]["sendbytes"]          =   eth["tx"]["bytes"]
                                                           
            #   Calculate Rx/Tx interface Drop Rate            
            ifaces[eth["interface"]]["rxdroprate"]         =   (eth["rx"]["drop"] - ifaces[eth["interface"]]["rxdroppedpackets"]) / INTERVAL
            ifaces[eth["interface"]]["txdroprate"]         =   (eth["tx"]["drop"] - ifaces[eth["interface"]]["txdroppedpackets"]) / INTERVAL            
            
            #   Set the rx/tx drops
            ifaces[eth["interface"]]["rxdroppedpackets"]   =   eth["rx"]["drop"]
            ifaces[eth["interface"]]["txdroppedpackets"]   =   eth["tx"]["drop"]
            
            #   Calculate the Average Rate
            ifaces[eth["interface"]]["avgrx"]              =   int(ifaces[eth["interface"]]["rxrate"] * AVG_LOW_PASS + ifaces[eth["interface"]]["avgrx"] * (1.0-AVG_LOW_PASS))
            ifaces[eth["interface"]]["avgtx"]              =   int(ifaces[eth["interface"]]["txrate"] * AVG_LOW_PASS + ifaces[eth["interface"]]["avgtx"] * (1.0-AVG_LOW_PASS))
                                                           
            #   Set the Max Rates                          
            ifaces[eth["interface"]]["toprx"]              =   ifaces[eth["interface"]]["rxrate"] if ifaces[eth["interface"]]["rxrate"] > ifaces[eth["interface"]]["toprx"] else ifaces[eth["interface"]]["toprx"]
            ifaces[eth["interface"]]["toptx"]              =   ifaces[eth["interface"]]["txrate"] if ifaces[eth["interface"]]["txrate"] > ifaces[eth["interface"]]["toptx"] else ifaces[eth["interface"]]["toptx"]
            
            now = datetime.now()
            print now
            print "\tRX - MAX: %s AVG: %s CUR: %s DROPRATE: %s" %(ifaces[eth["interface"]]["toprx"],ifaces[eth["interface"]]["avgrx"],ifaces[eth["interface"]]["rxrate"],ifaces[eth["interface"]]["rxdroprate"])
            print "\tTX - MAX: %s AVG: %s CUR: %s DROPRATE: %s" %(ifaces[eth["interface"]]["toptx"],ifaces[eth["interface"]]["avgtx"],ifaces[eth["interface"]]["txrate"],ifaces[eth["interface"]]["txdroprate"])
            print ""    
        
    time.sleep(INTERVAL)

