import supervisor
import storage
#from keyboard import Keyboard
supervisor.disable_autoreload()

# Go into read-only mode with the filesystem if
# Esc is held down during boot
# Param in storage is relative to circuit python
# False means it's R/W for python, not host computer
#if Keyboard.is_esc():
#    storage.remount("/", readonly=False)

