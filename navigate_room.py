# -*- coding: utf-8 -*-
"""
Created on Sat Jan 31 19:02:16 2015

@author: thekitchenscientist@gmail.com
Using robot detailed here:
http://blog.thekitchenscientist.co.uk/2015/02/ev3-python-maze-solv3r.html

This code was to try out gathering sensor data and issuing commands over bluetooth to LEGO EV3. 
Due to poorly paired motors the robot moves in jerks rather than fluidly to keep the left and right rotations in sync.
The code assumes the following wiring configuration:

    Port B - LH motor
    Port C - RH motor
    Port 1 - Forward facing IR sensor
    Port 2 - Right facing colour sensor
    Port 4 - Forward facing touch sensor

"""

import time
from ev3 import *

# move robot
def mv_rbt(direction,turn_ratio,step):
    mv = direct_command.DirectCommand()
    mv.add_output_ready(direct_command.OutputPort.PORT_C | direct_command.OutputPort.PORT_B)
    mv.add_output_step_sync(direct_command.OutputPort.PORT_C | direct_command.OutputPort.PORT_B,direction,turn_ratio,step,1)
    with ev3.EV3() as brick:
        mv.send(brick)
                
def stop_rbt():
    stop = direct_command.DirectCommand()
    stop.add_output_stop(direct_command.OutputPort.PORT_C | direct_command.OutputPort.PORT_B,1)
    with ev3.EV3() as brick:
        stop.send(brick)
        
def rd_snr():
    snr = direct_command.DirectCommand()
    snr.add_input_device_ready_si(0,0,33)
    snr.add_input_device_ready_si(1,2,29)      
    snr.add_input_device_get_bumps(3)    
    with ev3.EV3() as brick:
        x = snr.send(brick)
        print(x)
        return x

def rst_tch():
    chk2 = direct_command.DirectCommand()    
    chk2.add_input_device_clr_all(3)
    with ev3.EV3() as brick:
       chk2.send(brick)

def LEDs(pattern):
    LED =  direct_command.DirectCommand()
    LED.add_set_leds(pattern)
    with ev3.EV3() as brick:
        LED.send(brick)

#set up initial conditions
rst_tch()
time.sleep(0.3)
snr_rds = rd_snr()
start_count = snr_rds[2]

x = 100
LED_col = 0
power = 55

#movement loop
while (x > -1):
            LEDs(LED_col)
            snr_rds = rd_snr()
            current_count = snr_rds[2]
            time.sleep(1)
            

            if current_count <= start_count:
                mv_rbt(power,0,100)
                x = snr_rds[0]
                LED_col = 1
            else:
                current_col = snr_rds[1]
                if current_col == 0.0:
                    mv_rbt(-35,0,350)
                    mv_rbt(40,120,240)
                    mv_rbt(40,0,100)                
                    mv_rbt(40,120,240)
                else:
                    mv_rbt(-45,0,350)
                    mv_rbt(40,-120,240)
                    mv_rbt(40,0,100)                
                    mv_rbt(40,-120,240)
                start_count = snr_rds[2]

            #slow down if close to wall
            if x < 25:
                power = 30
                LED_col = 3


else:
   LEDs(2)
   stop_rbt()
