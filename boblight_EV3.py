# -*- coding: utf-8 -*-
"""
Created on Sat Jan 31 19:02:16 2015

@author: thekitchenscientist@gmail.com
"""
import time
import subprocess
from ev3 import *

def rd_snr():
    snr = direct_command.DirectCommand()
    snr.add_input_device_ready_raw3(1,4,29)         
    with ev3.EV3() as brick:
        x = snr.send(brick)
        print(x[0])
        return x[0]

def hex_to_rgb(value):
    #value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb
    

x = 100

#movement loop
while (x > -1):
            snr_rds = rd_snr()
            time.sleep(0.1)
            y = rgb_to_hex(snr_rds)
            print(y)
            #subprocess.call(["sudo","boblightd"])
            subprocess.call(["sudo","boblight-constant",y]) 
            time.sleep(1)
            subprocess.call(["sudo","killall","boblight-constant"])
