# -*- coding: utf-8 -*-
import sys
import time
from gi.repository import GLib
import dbus
import dbus.service
import dbus.mainloop.glib
import string

CONNECT_NAME = "com.pi.ReceiveConnectName"
SERVICE_PATH = "/com/pi/ReceiveServicePath"
PUBILC_NAME  = "com.pi.ReceivePublicName"

class ReceiveMessage(dbus.service.Object):

    def __init__(self, bus=None, path=None):
        super(ReceiveMessage, self).__init__(bus, path)
    
    def start(self):
        print(">>>>>>>>>>>>>>>>>>>>>>>>> start receive message")
        bus.add_signal_receiver(self.sig_receive_message_handler,
                                dbus_interface = PUBILC_NAME, 
                                signal_name = "sig_forward_message")    

    def sig_receive_message_handler(self,message):
        print(">>>>>>>>>>>>>>>>>>>>>>>>> recveive message handling")
        print(message)

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus  = dbus.SessionBus()
    name = dbus.service.BusName(CONNECT_NAME, bus)
    receive = ReceiveMessage(bus, SERVICE_PATH)

    receive.start()

    loop = GLib.MainLoop()
    loop.run()
