from ev3 import *

"""
@author: thekitchenscientist@gmail.com
Published here:
http://blog.thekitchenscientist.co.uk/2015/01/commanding-ev3-from-linux-pc-part-4.html

The first example creates an object called fwd to which we bind the classi
called direct command. We can then call the functions of the direct command
using the magic dot. When you type fwd. on each line a list of the available
functions appear (in Spyder) which you can scroll through and choose
the correct one. Then when you type ( the object inspector tells you about
the commands this function accepts.
"""

# move forward
fwd = direct_command.DirectCommand()
fwd.add_output_speed(direct_command.OutputPort.PORT_C,100)
fwd.add_output_speed(direct_command.OutputPort.PORT_B,100)
fwd.add_output_start(direct_command.OutputPort.PORT_C)
fwd.add_output_start(direct_command.OutputPort.PORT_B)
fwd.add_timer_wait(1600)
fwd.add_output_stop(direct_command.OutputPort.PORT_C,
direct_command.StopType.BRAKE)
fwd.add_output_stop(direct_command.OutputPort.PORT_B,
direct_command.StopType.BRAKE)

"""
For the second example it is first necessary to create lists to hold
the xy coordinates of each thing we wish to display on the screen.
Also the text to display is specified. When writing to the screen
ui_draw_update is required to tell the EV3 when you want to display
the screen commands it has been given.
"""

# define circle xy coordinates

xy =[0 for i in range(2)]
xy[0] = 30
xy[1] = 60
xy2 =[0 for i in range(2)]
xy2[0] = 120
xy2[1] = 120
xy3 =[0 for i in range(2)]
xy3[0] = 70
xy3[1] = 40

Display_Text = "Hello World!"

draw_spots = direct_command.DirectCommand()
draw_spots.add_ui_draw_clean()
draw_spots.add_ui_draw_fillcircle(1,xy2,20)
draw_spots.add_ui_draw_fillcircle(1,xy,20)
draw_spots.add_ui_draw_selectfont(1)
draw_spots.add_ui_draw_text(1,xy3,Display_Text)
draw_spots.add_ui_draw_update()

"""
The LED mode is set in the next example and a timer on the EV3 is used to delay
execution of turning the LEDs off.
"""

#control LEDs

set_LEDs = direct_command.DirectCommand()
set_LEDs.add_set_leds(8)
set_LEDs.add_timer_wait(2000)
set_LEDs.add_set_leds(0)

"""
The touch sensor is easy to read and has a two modes to choose from get bumps &
get changes (no. releases or number of presses).
"""

#read bumps

read_bumps = direct_command.DirectCommand()
read_bumps.add_input_device_clr_changes(0)
read_bumps.add_timer_wait(3000)
read_bumps.add_input_device_get_bumps(0)

"""
The colour sensor took a bit of experimentation to get to work. The input ports
are not referred to by the numbers 1-4 but 0-3. Also the device type numbers
do not correspond to the list given in the library. Device_type = 7 will cause
the colour sensor to function correctly but will return the wrong
device_get_name. You can then access the reflective (0), ambient (1) and
colour (3) modes.
"""

#read colour

read_col = direct_command.DirectCommand()
read_col.add_input_device_ready_raw(3,2,7)
read_col.add_timer_wait(500)
read_col.add_input_device_get_name(3)

"""
To issue the command simply append .send(brick) to the name of the object you
wish to call. To read/use any messages from the sensors set the send command
as a variable:
x = read_col.send(brick)
print(x)
"""

with ev3.EV3() as brick:
    fwd.send(brick)
    draw_spots.send(brick)
    set_LEDs.send(brick)
