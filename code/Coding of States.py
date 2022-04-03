
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
        oled.text(str(measurement)+'mm',40,0,1)
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
            
            file = open("/sd/sample.csv","a")
            file.write(str(measurement))
            file.write(",")
            file.write((str(recorded_time[0]))+'-'+(str(recorded_time[1]))+'-'+(str(recorded_time[2]))+','+(str(recorded_time[3]))+':'+(str(recorded_time[4]))+':'+(str(recorded_time[5])+','+(str(current_time-recording_start_time))+"\n"))
            file.close()
              
            for i in range(10):
                oled.fill(0)
                oled.text(".",i,0,1)
                oled.text(".",i,10,1)
                oled.text(".",i,20,1)
                oled.text("recording data",15,0,1)
                oled.text("to .csv file",15,10,1)
                oled.text("bnt_b to exit",15,20,1)
                oled.show()
                
    if current_state == "net config":
        oled.fill(0)
        oled.text("net config parametres" ,0,0,1)  
        oled.show()