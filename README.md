# Refresh Web Page ( Web app in kiosk mode)
# Introduction
This script will refresh web page if no user activity recorded
Refresh timer is set when mouse click is registered
(PowerApps Kiosk user session times out - this is workaround)

# Dependencies
- pynput >= 1.7.6
- selenium >= 4.9.1

## Package as standalone executable
Install PyInstaller from PyPI:

>pip install pyinstaller

Go to your program’s directory and run:

>pyinstaller launcher.py --splash splashfile.png --debug bootloader --hidden-import "babel.numbers" --icon=small_icon.ico
