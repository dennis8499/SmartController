#!/usr/bin/python

import time
import signal

import scrollphathd
from scrollphathd.fonts import font5x7

def setup():
    scrollphathd.set_brightness(0.5)
	
def setDegree(msg):
    scrollphathd.clear()
    scrollphathd.flip(x=True, y=True)  
    scrollphathd.write_string(msg, x=3, y=0,font=font5x7, brightness=0.5)
    scrollphathd.show()
    scrollphathd.scroll()
	
def setMsg(msg):
    scrollphathd.clear()
    scrollphathd.flip(x=True, y=True) 
    scrollphathd.write_string(msg, x=0, y=0,font=font5x7, brightness=0.5)
    scrollphathd.show()
    scrollphathd.scroll()
def setBri(msg):
    if ((msg % 10) <= 10):
        scrollphathd.clear()
        scrollphathd.flip(x=True, y=True)  
	scrollphathd.write_string(str(msg), x=3, y=0,font=font5x7, brightness=0.5)
	scrollphathd.show()
	scrollphathd.scroll()
    elif ((msg % 10) > 10):
	scrollphathd.clear()
        scrollphathd.flip(x=True, y=True)  
	scrollphathd.write_string(str(msg), x=0, y=0,font=font5x7, brightness=0.5)
	scrollphathd.show()
	scrollphathd.scroll()

def setFan1():
    scrollphathd.clear()
    scrollphathd.flip(x=True, y=True)  
    scrollphathd.write_string(">", x=6, y=0,font=font5x7, brightness=0.5)
    scrollphathd.show()
    scrollphathd.scroll()

def setFan2():
    scrollphathd.clear()
    scrollphathd.flip(x=True, y=True) 
    scrollphathd.write_string(">>", x=3, y=0,font=font5x7, brightness=0.5)
    scrollphathd.show()
    scrollphathd.scroll()
	
def setFan3():
    scrollphathd.clear()
    scrollphathd.flip(x=True, y=True) 
    scrollphathd.write_string(">>>", x=0, y=0,font=font5x7, brightness=0.5)
    scrollphathd.show()
    scrollphathd.scroll()
	
def scroll():
    scrollphathd.scroll()


