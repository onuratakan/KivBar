# KivBar
*A **taskbar** bar made in kivy*

> ![image 1](https://user-images.githubusercontent.com/68729523/190897762-8a78bbd1-3926-4100-8932-f5a1e451ee42.png)
> _Preview in bspwm_. Wallpaper at [HERE](https://cdna.artstation.com/p/assets/images/images/014/306/200/large/c-home-akalil.jpg?1543420107)

### Installation 

> Install distribution provided python

* Install Deps
```shell
pip3 install kivy kivymd pillow
```
* Clone repo
```shell
git clone https://github.com/T-Dynamos/KivBar ~/.config/kivybar
```

For sound you need [pulseaudio](http://pulseaudio.org/)
and for music you need mpd , ncmpcpp and mpc ( Basic knowleged that how it works) .

### Running

Just append this line to your window manger's rc file. For eg, `~/.confgi/bspwm/bswpmrc` in bspwm

```shell
exec cd ~/.config/kivbar && python3 main.py > ~/.kivbar.log 2>&1 &
```

### Configuring

Configration file is `~/.config/kivybar/launch.py` you can set launcher icon there


Report bugs in [issues](https://github.com/T-Dynamos/KivBar/issues)
