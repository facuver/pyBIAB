from io import ControlHeater, Buzzer ,Switch
from machine import Pin,I2C,RTC

import uasyncio as asyncio

import cfg , time , web, wifi





h = ControlHeater(Pin(2),freq = 100)
b = Buzzer(Pin(15))

rtc = RTC()
rtc.datetime((2020, 11, 27, 16, 19, 48, 0, 0)) # set a specific date and time




 # Starts the menu on the LCD

import ui

async def mainloop():
    ui.lcd_print(IP.ifconfig()[0])
    while True:
        
        #ui.update_all()
        await asyncio.sleep(2)
         

if __name__ == "__main__":
    
    ui.lcd_print(str("Connecting to ", cfg.wifi["ssid"]))
    IP = wifi.do_connect(cfg.wifi["ssid"],cfg.wifi["pass"])
    if IP == None:
        ui.lcd_print("Fail to connect, Starting AP")
        IP = wifi.start_ap()
    print(IP)
    
    
    asyncio.create_task(mainloop())
    web.app.run(host=IP.ifconfig()[0],port = 80,debug = True)

