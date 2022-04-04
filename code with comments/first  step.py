from machine import Pin, I2C, Timer, SPI, SoftSPI  #Pins, timers and importing some protocols to comunicate.
import os #operating systems module
import sdcard	 #sdcard library 
import time # time module
import ssd1306 # oled screen library
from dht import DHT11 
from pcf8523 import PCF8523 # RTC library

spi=SoftSPI(sck=Pin(5),mosi=Pin(18),miso=Pin(19))
sd=sdcard.SDCard(spi,cs=Pin(33))
vfs=os.VfsFat(sd)
# SD card connection to pins and creating virtual file system.

i2c = I2C(1, sda=Pin(23), scl=Pin(22)) #connecting I2C to sda,scl pins.
oled = ssd1306.SSD1306_I2C(128, 32, i2c) # connecting oled as oled to i2c.
rtc = PCF8523(i2c) # connecting rtc to PCF8523 with i2c

clock_pin = Pin(12, Pin.IN, Pin.PULL_UP) # mitutuyo clock connected to esp 32 pin
data_pin = Pin(21, Pin.IN, Pin.PULL_UP) # mitutuyo data connected to esp 32 pin
request_pin = Pin(27, Pin.OPEN_DRAIN, value = 1) # mitutuyo request connected to esp 32 pin

switch_A = Pin(15, Pin.IN, Pin.PULL_UP) #defining  button A to a pin
switch_B = Pin(32, Pin.IN,Pin.PULL_UP) #defining  button B to a pin
switch_C = Pin(14, Pin.IN, Pin.PULL_UP) #defining  button C to a pin
               menu_items = [] # define menu_items as  array
menu_items.append("Live measurement") # append menu_items with "Live measurement"
menu_items.append("Sampling Time") # append menu_items with "Samling Time"
menu_items.append("Delete") # append menu_items with "Delete"
menu_items.append("Run record") # append menu_items with "Run record"
menu_items.append("net config") # append menu_items with "net config"
current_state = "Menu" # define current_state as "Menu" it shows that cerrent_state is menu at beginning

active_item = 1 # define active_item as international variable and it is equal to = 1, this variable indicates menu possition.
shift= 0 # define shift  as international variable and it is equal to = 0, this variable is for making a moving menu
A_BP_state = 0  # defines button A as international.
B_BP_state = 0  # defines button B as international.
C_BP_state = 0  # defines button C as international.
short_list = 0 # define short_list  as international variable and it is equal to = 0, this variable is for making a moving menu
data = [] # define data as array
count = 0 # define data as international variable.
measurement = 0 # define measurement as international variable.

a = 0 # define a as international variable.
sampling_times = [5, 30, 60] #define sampling_times as array and add sampling times variables.
sampling_time = sampling_times[0] # equales sampling_time to first digit of sampling_time.

time_ = rtc.datetime  