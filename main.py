#!/usr/bin/python3
from kivy.config import Config
from kivy.lang import Builder
from kivy.metrics import dp

Config.set("graphics","borderless","1")
Config.set("graphics","position","custom")
Config.set("graphics","left","36")
Config.set("graphics","top","35")
Config.set("graphics","resizable","0")

from kivy.core.window import Window 
from kivy.animation import  Animation
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.behaviors import *
from PIL import ImageGrab 
import datetime
import shutil
import os
import launch

class ControlSound():

    # PulseAudio is required

    get_volume = lambda : os.popen("pactl get-sink-volume 0 ").read().split("/")[1]
    increase_volume = lambda volume : os.system("pactl set-sink-volume 0 {}".format(volume))


class BatteryInfo():

    # Acpitools is required 

    current_battery = lambda : int(os.popen("acpi -V").read().split("\n")[0].split(",")[1].split("%")[0])
    status = lambda : str(os.popen("acpi -V").read().split("\n")[0].split(",")[0].split(":")[-1]) 


class BrightNessInfo():
 
    backlight = "/sys/class/backlight/"+os.listdir("/sys/class/backlight")[0]
    current_brightness = lambda self,*largs : int(open(self.backlight+"/brightness","r").read()) 
    max_brightness = lambda self,*largs : int(open(self.backlight+"/max_brightness","r").read())

    change_brightness = lambda self,value,*largs : os.system("echo {} > /sys/class/backlight/intel_backlight/brightness".format(value))


class ControlMusic():
   #Ncmpcpp, mpd, mpc and kunst are required
    
    play = lambda *largs : os.system("mpc -q toggle && kunst --size 60x60 --silent ")
    stop = lambda *largs : os.system("mpc -q pause")
    previous = lambda *largs : os.system("mpc -q prev && kunst --size 60x60 --silent")
    next_play = lambda *largs : os.system("mpc -q next && kunst --size 60x60 --silent")

    def get_current(self):
        music = os.popen("mpc -f %title% current").read().replace("\n","")
        if music in [""," ",None,"MPD error: Connection refused"]:
            return "Stopped"
        else:
            return music


def roundBattery(battery):
    if len(str(battery)) == 2 and int(str(battery)[:-1]) != 0 and battery < 91:
        return battery+(10-int(str(battery)[-1:]))

    if len(str(battery)) == 3:
        return battery
    else:
        return ""


class SideBar(MDApp):

    screen_size = ImageGrab.grab().size
    bar_size = dp(50),screen_size[1]-screen_size[1]//10

    launcher = lambda *largs : os.system(launch.run)
    powermenu = lambda *largs : os.system(launch.powermenu)
    icon = launch.icon

    BatteryInfo = BatteryInfo


    def build(self):

        self.date = datetime.datetime.now().strftime("%H %M")
        self.theme_cls.theme_style = "Dark"
        self.bar = Builder.load_file("main.kv")
        Window.size = self.bar_size
        Window.on_cursor_leave = lambda *largs : self.animateBarPowerbutton(do=False)
        return self.bar


    def update_time(self,arg):  
        self.date = datetime.datetime.now().strftime("%H %M")
        self.bar.ids.t1.text = self.date.split(" ")[0]
        self.bar.ids.t2.text = self.date.split(" ")[1]


    def update_battery(self,arg):

        status =  BatteryInfo.status()
        current = BatteryInfo.current_battery()

        self.bar.ids.battery.text  = str(current)+"%"

        if "Not" in status or "Discharging" in status:
            self.bar.ids.b_icon.icon = "battery-"+str(roundBattery(current)) if str(roundBattery(current)) != "" else "battery"
            self.bar.ids.b_icon.icon_color = "#BDE51A"
        else:
           self.bar.ids.b_icon.icon = "battery-charging-"+str((roundBattery(current)))
           self.bar.ids.b_icon.icon_color = "#1AE51A"


    def on_start(self):

        Clock.schedule_interval(self.update_time,0)
        Clock.schedule_interval(self.update_battery,0)
        
        

    def animateBarPowerbutton(self,do=True):
        if self.bar.ids.power_box.pos_hint == {"center_y":-1,"center_x":0.5} and do == True:
            Animation(pos_hint={"center_y":0.14,"center_x":0.5},d=0.3,t="in_out_bounce").start(self.bar.ids.power_box)
            Animation(pos_hint={"center_y":0.3,"center_x":0.5},d=0.3,t="in_out_bounce").start(self.bar.ids.time_card)
            Animation(pos_hint={"center_y":0.5,"center_x":0.5},d=0.3,t="in_out_bounce").start(self.bar.ids._card)
        else: 
            Animation(pos_hint={"center_y":-1,"center_x":0.5},d=0.2,t="in_out_bounce").start(self.bar.ids.power_box)
            Animation(pos_hint={"center_y":0.12,"center_x":0.5},d=0.2,t="in_out_bounce").start(self.bar.ids.time_card)     
            Animation(pos_hint={"center_y":0.32,"center_x":0.5},d=0.2,t="in_out_bounce").start(self.bar.ids._card)


if __name__ == "__main__":
    SideBar().run()