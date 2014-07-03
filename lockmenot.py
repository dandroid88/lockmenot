import dbus.mainloop.glib; dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
from gi.repository import GObject
import NetworkManager
import os
import subprocess
import atexit
import sys

def disable_lock_screen():
    os.system('dconf write /org/gnome/desktop/screensaver/lock-enabled false')

@atexit.register
def enable_lock_screen():
    os.system('dconf write /org/gnome/desktop/screensaver/lock-enabled true')

def get_current_ssid():
    process = subprocess.Popen(['iwgetid', '-r'], stdout=subprocess.PIPE)
    return ''.join(process.communicate()[0]).strip()

def disable_if_ssid_matches(ssid):
    if get_current_ssid() == ssid:
        disable_lock_screen()

def handle_state_change(state_change_code):
    global SSID
    if 70 == state_change_code:
        disable_if_ssid_matches(SSID)
    else:
        enable_lock_screen()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Usage: python lockmenot SSID_NAME'
        exit()
    global SSID
    SSID = sys.argv[1]
    disable_if_ssid_matches(SSID)
    NetworkManager.NetworkManager.connect_to_signal('StateChanged', handle_state_change)
    loop = GObject.MainLoop()
    loop.run()
