#!/usr/bin/python3
from kivy.config import Config
from kivy.lang import Builder
from kivy.metrics import dp
import sys

Config.set("graphics","borderless","1")
Config.set("graphics","position","custom")
Config.set("graphics","left",sys.argv[1])
Config.set("graphics","top",sys.argv[2])
Config.set("graphics","resizable","0")

from kivy.core.window import Window 
from kivy.animation import  Animation
from kivy.clock import Clock
from kivymd.app import MDApp
import os
from main import BrightNessInfo,ControlSound, ControlMusic 

class WindowRoot(MDApp):
    
    BrightNessInfo = BrightNessInfo
    ControlSound = ControlSound
    ControlMusic = ControlMusic

    def build(self):
        self.theme_cls.theme_style = "Dark"
        Window.size = (dp(int(sys.argv[4])),dp(int(sys.argv[5])))
        return Builder.load_file(sys.argv[3])

    def on_pre_start(self,arg):
        Window.on_cursor_leave = self.stop

    def on_start(self):
        anim = lambda *largs : Animation(opacity=0,d=1).start(self.root.ids.hider)
        Clock.schedule_once(anim,1)
        Window.on_cursor_enter = lambda *largs : Clock.schedule_once(self.on_pre_start)
        if sys.argv[3] == "music.kv":
            Clock.schedule_interval(self.loopSong,0)

    def control_music(self,instance):

        if self.ControlMusic().get_current() == "Stopped":
            return 
        if instance.icon == "play":
            self.ControlMusic.play()
            instance.icon = "pause"
        else:
            self.ControlMusic.stop()
            instance.icon = "play"

    def loopSong(self,arg):

        self.root.ids.text_bar.text = self.ControlMusic().get_current()[:15]+"..."

    def get_icon(self,instance):

        if self.ControlMusic().get_current() != "Stopped":
            if os.popen("mpc status").read().split("\n")[1].startswith("[playing]"):
                return "pause"
            else:
                return "play"
        else:
            return  "exit-run"


WindowRoot().run()
