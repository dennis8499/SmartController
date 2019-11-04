#!/usr/bin/python
import time
import scrollphathd
from scrollphathd.fonts import font5x7

BRIGHTNESS = 0.3

def setTime():
    scrollphathd.clear()
    hour = time.strftime("%I")
    minute = time.strftime("%M")	
    Ihour = int(hour)
    Iminute = int(minute) / 10
    if((Ihour % 10) < 10):
        #msg = str(Ihour) + time.strftime(":%M")
	msg = str(Ihour) + ":" + str(Iminute) + "1"
	scrollphathd.write_string(msg,x=0,y=0,font=font5x7,brightness=BRIGHTNESS)
	scrollphathd.flip(x=True, y=True) 
	scrollphathd.show()
    else:
	scrollphathd.write_string(time.strftime("%I:%M"),x=0,y=0,font=font5x7,brightness=BRIGHTNESS)
	scrollphathd.flip(x=True, y=True) 
	scrollphathd.show()

def off():
    scrollphathd.clear()
