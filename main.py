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
from kivy.uix.anchorlayout import AnchorLayout
from PIL import ImageGrab 
import datetime
import shutil
import os
import launch

class DI(AnchorLayout):
    
    pass


class ControlSound():

    # PulseAudio is require:w

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

    change_brightness = lambda self,value,*largs : os.system("echo {} > {}".format(value,self.backlight+"/brightness"))


class ControlMusic():
   
    #Ncmpcpp, mpd and mpc are required
    
    play = lambda *largs : os.system("mpc -q toggle")
    stop = lambda *largs : os.system("mpc -q pause")
    previous = lambda *largs : os.system("mpc -q prev")
    next_play = lambda *largs : os.system("mpc -q next")

    def get_current(self):
        music = os.popen("mpc -f %title% current").read().replace("\n","")
        if music in [""," ",None,"MPD error: Connection refused"]:
            return "Stopped"
        else:
            return music


def roundBattery(battery):
    if len(str(battery)) == 2 and int(str(battery)[:-1]) != 0 and battery < 100:
        return int(str(battery)[:-1]+"0")
    if len(str(battery)) == 3:
        return "high"
    else:
        return "low"


class KivBar(MDApp):

    screen_size = ImageGrab.grab().size
    bar_size = dp(50),screen_size[1]-screen_size[1]//10

    launcher = lambda *largs : os.system(launch.run)
    
    icon = launch.icon
    font = launch.default_font
    session = launch.session

    desktops = lambda *largs : os.popen("wmctrl -d").read().split("\n")[:-1]

    BatteryInfo = BatteryInfo
    animating = False
    title = "KivBar"

    def build(self):

        self.date = datetime.datetime.now().strftime("%H %M")
        self.theme_cls.theme_style = "Dark"
        self.bar = Builder.load_file("kvfiles/main.kv")
        Window.size = self.bar_size
        Window.on_cursor_leave = lambda *largs : self.animateBarPowerbutton(do=False)
        Window.on_close_request = lambda *largs : print
        return self.bar

    def add_desktop_widgets(self,arg):


        for count,i in enumerate(self.desktops()):

            widget = DI()
            widget.icon = "circle-outline" if "*" not in i else "circle"
            widget.count = count
            print(widget.count)

            self.root.ids.d_card.add_widget(widget)

    def update_current_desktop(self,arg):

        for count,desktop in enumerate(self.desktops()):
            if "*" in desktop:
                self.current_desktop = count

        for count,widget in enumerate(self.root.ids.d_card.children[::-1]):
            if count == self.current_desktop:
                widget.icon = "circle"
            else:
                widget.icon = "circle-outline"
    


    def update_time(self,arg):  
        self.date = datetime.datetime.now().strftime("%H %M")
        self.bar.ids.t1.text = self.date.split(" ")[0]
        self.bar.ids.t2.text = self.date.split(" ")[1]


    def update_battery(self,arg):

        status =  BatteryInfo.status()
        current = BatteryInfo.current_battery()

        self.bar.ids.battery.text  = str(current)+"%"

        if "Not" in status or "Discharging" in status:
            self.bar.ids.b_icon.icon = "battery-"+str(roundBattery(current))
            self.bar.ids.b_icon.icon_color = "#BDE51A"
        else:
           self.bar.ids.b_icon.icon = "battery-charging-"+str((roundBattery(current)))
           self.bar.ids.b_icon.icon_color = "#1AE51A"


    def on_start(self):

        cmd = ("sh -c 'sleep 2 && wmctrl -b add,sticky,skip_taskbar,above -r {}' &".format(self.title))
        print(cmd)
        os.system(cmd)
        Clock.schedule_once(self.add_desktop_widgets,0)
        Clock.schedule_interval(self.update_time,0)
        Clock.schedule_interval(self.update_battery,0)
        Clock.schedule_interval(self.update_current_desktop,0)
        

    def animateBarPowerbutton(self,do=True):

        if self.bar.ids.power_box.pos_hint  == {"center_y":-1,"center_x":0.5} and do == True and self.animating == False:
            Animation(pos_hint={"center_y":0.14,"center_x":0.5},opacity=1,d=0.3,t="in_out_bounce").start(self.bar.ids.power_box)
            Animation(pos_hint={"center_y":0.3,"center_x":0.5},d=0.2,t="in_out_bounce").start(self.bar.ids.time_card)
            Animation(pos_hint={"center_y":0.5,"center_x":0.5},d=0.1,t="in_out_bounce").start(self.bar.ids._card)
            self.animating = True
        else:
            self.animating = True
            Animation(pos_hint={"center_y":-1,"center_x":0.5},opacity=0,d=0.1,t="in_out_bounce").start(self.bar.ids.power_box)
            Animation(pos_hint={"center_y":0.12,"center_x":0.5},d=0.2,t="in_out_bounce").start(self.bar.ids.time_card)     
            Animation(pos_hint={"center_y":0.32,"center_x":0.5},d=0.3,t="in_out_bounce").start(self.bar.ids._card)
            def fix(*largs):
                self.animating = False 
            Clock.schedule_once(fix,0.3)

if __name__ == "__main__":
    KivBar().run()
