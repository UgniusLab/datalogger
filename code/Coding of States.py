
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
        os.mount(sd,'/sd')
        file = open("/sd/sample.csv","w")
        file.write("value"+','+"date"+','+"time in h:m:s"+','+"time in s"+"\n")
        file.close
         
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
 