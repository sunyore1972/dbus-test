# -*- coding: utf-8 -*-

import sys
import time
from gi.repository import GLib
import dbus
import dbus.service
import dbus.mainloop.glib
import string

CONNECT_NAME         = "com.pi.ForwardConnectName"
SERVICE_PATH         = "/com/pi/ForwardServicePath"
PUBLIC_NAME          = "com.pi.ForwardPublicName"
CALLER_PUBLIC_NAME   = "com.pi.SenderPublicName"
RECEIVER_PUBLIC_NAME = "com.pi.ReceivePublicName"

class ForwardMessage(dbus.service.Object):
    def __init__(self, bus=None, path=None):
        super(ForwardMessage, self).__init__(bus, path)
    
    #@dbus.service.method(dbus_interface=CALLER_PUBLIC_NAME, in_signature='s') #match csender.c 1 
    @dbus.service.method(dbus_interface=PUBLIC_NAME, in_signature='s')      #match csender.c 2
    def receive_data(self, strmsg):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> receive data")
        print(strmsg)
        self.sig_forward_message(strmsg)

    @dbus.service.signal(dbus_interface=RECEIVER_PUBLIC_NAME)
    def sig_forward_message(self, strmsg):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> signal forward message")
    
    def start(self):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> start forward message service")


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus  = dbus.SessionBus()
    name = dbus.service.BusName(CONNECT_NAME, bus)
    forward = ForwardMessage(bus, SERVICE_PATH)

    forward.start()

    loop = GLib.MainLoop()
    loop.run()
