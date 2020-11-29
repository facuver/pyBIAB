import machine
from machine import Pin , PWM ,Timer
import uasyncio as asyncio

class ControlHeater():
    def __init__(self,pin,freq = 100):
        print("Startin PWM in ",pin)
        self.pwm = PWM(pin, freq= freq,duty = 0)
        
        
    def update(self,value):
        self.pwm.duty(value)
        print("pwm duty: ",value)
        
    def max(self):
        self.pwm.duty(1023)
        print("pwm Max")
        
        
    def off(self):
        self.pwm.duty(0)
        print("pwm OFF")

class Buzzer():
    def __init__(self,pin):
        self.b = PWM(pin,freq=500,duty = 0)
        print('buzzer at: ',pin)
        
    async def tone(self,times):    
        for i in range(times):
            print("BEEP")
            self.b.duty(500)
            await asyncio.sleep_ms(500)
            self.b.duty(00)
            await asyncio.sleep_ms(500)

class Switch():
    """Switch Class
 
    Class for defining a switch. Uses internal state to debounce switch in
    software. To use switch, check the "new_value_available" member and the
    "value" member from the application.
    """
    def __init__(self, pin, checks=3, check_period=100 , cb = None):
        self.cb = cb
        self.pin = pin
        self.pin.irq(handler=self._switch_change,
                     trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)
 
        self.debounce_timer = Timer(-1)
        self.new_value_available = False
        self.value = None
        self.prev_value = None
        self.debounce_checks = 0
        self.checks = checks
        self.check_period = check_period
 
    def _switch_change(self, pin):
        self.value = pin.value()
 
        # Start timer to check for debounce
        self.debounce_checks = 0
        self._start_debounce_timer()
 
        # Disable IRQs for GPIO pin while debouncing
        self.pin.irq(trigger=0)
 
    def _start_debounce_timer(self):
        self.debounce_timer.init(period=self.check_period, mode=Timer.ONE_SHOT,
                                 callback=self._check_debounce)
 
    def _check_debounce(self, _):
        new_value = self.pin.value()
 
        if new_value == self.value:
            self.debounce_checks = self.debounce_checks + 1
 
            if self.debounce_checks == self.checks:
                # Values are the same, debouncing done
 
                # Check if this is actually a new value for the application
                if self.prev_value != self.value:
                    self.new_value_available = True
                    self.prev_value = self.value
                    if self.value:
                        self.cb()
                # Re-enable the Switch IRQ to get the next change
                self.pin.irq(handler=self._switch_change,
                             trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)
            else:
                # Start the timer over to make sure debounce value stays the same
                self._start_debounce_timer()
        else:
            # Values are not the same, update value we're checking for and
            # delay again
            self.debounce_checks = 0
            self.value = new_value
            self._start_debounce_timer()
    
