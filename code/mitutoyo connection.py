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