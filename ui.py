from upymenu import Menu, MenuAction, MenuNoop
from io import Switch
from machine import Pin, I2C
from i2c_lcd import I2cLcd
import cfg
def action_callback():
    print("callback action chosen")


submenu = Menu("Submenu")
submenu.add_option(MenuAction("Submenu Action1", callback= lambda : print("Test")))
submenu.add_option(MenuAction("Submenu Action2", callback=action_callback))
submenu.add_option(MenuAction("Submenu Action3", callback=action_callback))
submenu.add_option(MenuAction("Submenu Action4", callback=action_callback))
submenu.add_option(MenuAction("Submenu Action5", callback=action_callback))
submenu.add_option(MenuAction("Submenu Action6", callback=action_callback))
submenu.add_option(MenuAction("Submenu Action7", callback=action_callback))
submenu.add_option(MenuAction("Submenu Action8", callback=action_callback))
submenu.add_option(MenuAction("Submenu Action9", callback=action_callback))
submenu.add_option(MenuAction("return", lambda: submenu.parent()))


menu_action = MenuAction("Action", callback=action_callback)
menu = Menu("Main Menu")
menu.add_option(submenu)
menu.add_option(menu_action)
menu.add_option(MenuNoop("Nothing here"))



print("Started")

def startMenu():
    
    if menu.current == None:
        menu.start(lcd)
    else:
        menu.current.parent()
        if menu.current == None:
            update_all()
    
def nextMenu():
    if menu.current != None:
        menu.current.focus_next()
def prevMenu():
    if menu.current != None:
        menu.current.focus_prev()
def selectMenu():
    if menu.current != None:
        menu.current.choose()
    

sw0 = Switch(Pin(15, Pin.IN, Pin.PULL_DOWN), checks = 2, check_period = 10,cb= startMenu )
sw1 = Switch(Pin(2, Pin.IN, Pin.PULL_DOWN), checks = 2, check_period = 10, cb= nextMenu)
sw2 = Switch(Pin(4, Pin.IN, Pin.PULL_DOWN), checks = 2, check_period = 10,cb = prevMenu)
sw3 = Switch(Pin(16, Pin.IN, Pin.PULL_DOWN), checks = 2, check_period = 10,cb = selectMenu)



i2c = I2C(0, sda = Pin(13) , scl=Pin(12))
lcd = I2cLcd(i2c,63,4,20)


def update_all():
    lcd.clear()
    lcd.putstr(cfg.beer["Name"])
    lcd.move_to(15,0)
    lcd.putstr("15:20")
    lcd.move_to(0,1)
    lcd.putstr("  St  |  Mh  |  Bl  ")
    lcd.move_to(6,2)
    lcd.putstr("|")
    lcd.move_to(13,2)
    lcd.putstr("|")
    lcd.move_to(6,3)
    lcd.putstr("|")
    lcd.move_to(13,3)
    lcd.putstr("|")
    
    
    lcd.move_to(2,2)
    lcd.putstr(str(cfg.beer["strike_temp"]))
    
    lcd.move_to(9,2)
    lcd.putstr(str(cfg.beer["mash"]["temp"]))
    lcd.move_to(9,3)
    lcd.putstr(str(cfg.beer["mash"]["time"]))
    
    lcd.move_to(16,3)
    lcd.putstr(str(cfg.beer["boil_time"]))


def lcd_print(message):
    lcd.clear()
    lcd.putstr(message)
