from machine import Pin, I2C, Timer
import os
import time
import ssd1306
from dht import DHT11
from pcf8523 import PCF8523

i2c = I2C(1, sda=Pin(23), scl=Pin(22))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
rtc = PCF8523(i2c)

clock_pin = Pin(12, Pin.IN, Pin.PULL_UP)
data_pin = Pin(21, Pin.IN, Pin.PULL_UP)
request_pin = Pin(27, Pin.OPEN_DRAIN, value = 1)

switch_A = Pin(15, Pin.IN, Pin.PULL_UP)
switch_B = Pin(32, Pin.IN,Pin.PULL_UP)
switch_C = Pin(14, Pin.IN, Pin.PULL_UP)

menu_items = []
menu_items.append("Live measurement")
menu_items.append("Sampling Time")
menu_items.append("Delete")
menu_items.append("Run record")
menu_items.append("net config")
current_state = "Menu"

active_item = 1
shift= 0
A_BP_state = 0
B_BP_state = 0
C_BP_state = 0
short_list = 0
data = []
count = 0
measurement = 0

a = 0
sampling_times = [5, 30, 60]
sampling_time = sampling_times[0]

time_ = rtc.datetime

def clock_callback(pin):
    global data, request_pin, count
    if data == [] :
        request_pin.value(1)
    bit = data_pin.value()
    data. append(bit)
    count += 1
    
def data_is_valid() :
    global data, convert_data
    convert_data = []
    
    if len(data) != 52 :
        return False
    for digit_number in range(13):
        convert_digit = 0
        for bit_position in range(4):
            convert_digit = convert_digit + (data[digit_number*4+bit_position] << bit_position)
        convert_data.append(convert_digit)
    if convert_data[0] != 15 or convert_data[1] != 15 or convert_data[2] != 15 or convert_data[3] != 15:
        return False
        
    elif convert_data[4] not in {0,8}:
        return False
    
    elif convert_data[11] not in [1,2,3,4,5]:
        return False
    elif convert_data[12] not in {0,1}:
        return False
    
    return True

def process_data():
    global convert_data,measurement
    measurement = 0
    for digit in [10,9,8,7,6,5]:
        measurement += convert_data[digit]*10**(10 - digit)
    measurement *= 10**-(convert_data[11])
    if convert_data[4] == 8:
        measurement *= -1
    measurement = round(measurement,3)
      
def request():
    global request_pin, data, count,enter
    data = []
    count = 0
    request_pin.value(0)
    
clock_pin.irq(clock_callback, Pin.IRQ_RISING)     
while True:
    
    start = time.ticks_ms()
    data =[]
    while not data_is_valid() :
        request()
        time.sleep_ms(100)
    process_data()
    
    prev_A_BP_state = A_BP_state
    prev_B_BP_state = B_BP_state
    prev_C_BP_state = C_BP_state
    A_BP_state = not switch_A.value()
    B_BP_state = not switch_B.value()
    C_BP_state = not switch_C.value()
    rising_A_BP = A_BP_state and (not prev_A_BP_state)
    rising_B_BP = B_BP_state and (not prev_B_BP_state)
    rising_C_BP = C_BP_state and (not prev_C_BP_state)
    
#     Coding of transitions
    if current_state == "Menu" and rising_B_BP==True and active_item == 1:
        current_state = "Live measurement"
        rising_B_BP = False
        
    if current_state == "Live measurement" and rising_B_BP :
        current_state = "Menu"
        rising_B_BP = False
        
    if current_state == "Menu" and rising_B_BP==True and active_item == 2:
        current_state = "Sampling Time"
        rising_B_BP = False
        
    if current_state == "Sampling Time" and rising_B_BP :
        current_state = "Menu"
        rising_B_BP = False
        
    if current_state == "Menu" and rising_B_BP==True and active_item == 3:
        current_state = "Delete"
        rising_B_BP = False
        
    if current_state == "Menu" and rising_B_BP==True and active_item == 4:
        previous_recorded_time_tick_ms = 0
        recording_start_time = rtc.datetime
        logFile = open((str(time.localtime(recording_start_time)[0]))+' - '+(str(time.localtime(recording_start_time)[1]))+' - '+(str(time.localtime(recording_start_time)[2]))+' - '+(str(time.localtime(recording_start_time)[3]))+'h'+(str(time.localtime(recording_start_time)[4]))+".csv", "a")
        logFile.write("value"+','+"date"+','+"time in h:m:s"+','+"time in s"+"\n")
        logFile.flush()
        current_state = "Run record"
        rising_B_BP = False
        
    if current_state == "Run record" and rising_B_BP :
        current_state = "Menu"
        rising_B_BP = False
    
    if current_state == "Menu" and rising_B_BP==True and active_item == 0:
        current_state = "net config"
        rising_B_BP = False
    
    if current_state == "net config" and rising_B_BP :
        current_state = "Menu"
        rising_B_BP = False
 
#     Coding of States
   
    
    if current_state == "Menu":
        if rising_A_BP:
            active_item -= 1
            shift -=1
        if rising_C_BP:
            active_item += 1
            shift +=1
        if shift < 0:
            shift=0
            active_item=1
        if shift > 4:
            shift = 4
            active_item = 5
        active_item = active_item % len(menu_items)
        short_list = menu_items[shift:shift+3] 
        line = 1
        item = 1
        oled.fill(0)
        for item in short_list:
            if active_item == line:
                h=0
                line_height = 10
                oled.text(item,10,(line-1)*10,1)
                h += line_height
            else:
                oled.text(item,10,(line-1)*10,1)
                oled.text('>',0,1)        
            line +=1
        oled.show()
    
            
    if current_state == "Live measurement":
        
        oled.fill(0)
        oled.text(str(measurement)+'mm',50,0,1)
        displayed_time = time.localtime(rtc.datetime)
        oled.text((str(displayed_time[3]))+':'+(str(displayed_time[4]))+':'+(str(displayed_time[5])),35,10,1)
        oled.text("btn_B to exit",15,20,1)
        oled.show()
        
   
        
    if current_state == "Delete" :
        oled.fill(0)
        oled.text(str(len([True for file in os.listdir() if ".csv" in file]))+ " files found",0,0,1)
        oled.text("btn_A to delete",0,10,1)
        oled.text("btn_B to exit",0,20,1)
        oled.show()
        if rising_A_BP==True :
            oled.fill(0)
            oled.text("files removed",10,10,1)
            oled.show()
            [os.remove(file) for file in os.listdir() if ".csv" in file]
            time.sleep(3)
            rising_A_BP=False
            current_state = "Menu"
        if rising_B_BP==True:
            rising_B_BP=False 
            current_state = "Menu"
            
    if current_state == "Sampling Time" :
        oled.fill(0)
        oled.text("btn_B to exit",0,0,1)
        oled.text("Sampling time:",0,10,1)
        oled.text(str(sampling_time),110,10,1)
        oled.text("btn_A to time",0,20,1)
        oled.show()
        if rising_A_BP==True:
            a += 1
            rising_A_BP = False
        sampling_time = sampling_times[a%len(sampling_times)]
    
    if current_state == "Run record" :
        if time.ticks_ms() > previous_recorded_time_tick_ms + sampling_time*1000:
            previous_recorded_time_tick_ms = time.ticks_ms()
            current_time = rtc.datetime
            recorded_time = time.localtime(current_time)
            logFile.write(str(measurement))
            logFile.write(",")
            logFile.write((str(recorded_time[0]))+'-'+(str(recorded_time[1]))+'-'+(str(recorded_time[2]))+','+(str(recorded_time[3]))+':'+(str(recorded_time[4]))+':'+(str(recorded_time[5])+','+(str(current_time-recording_start_time))+"\n"))
            logFile.flush()
            for i in range(10):
                oled.fill(0)
                oled.text(".",i,0,1)
                oled.text(".",i,10,1)
                oled.text(".",i,20,1)
                oled.text("recording data",15,0,1)
                oled.text("to .cvs file",15,10,1)
                oled.text("bnt_b to exit",15,20,1)
                oled.show()

            
        
        
    if current_state == "net config":
        oled.fill(0)
        oled.text("net config parametres" ,0,0,1)  
        oled.show()
    
    while time.ticks_diff(time.ticks_ms(), start) < 100:
        time.sleep_ms(10)     
