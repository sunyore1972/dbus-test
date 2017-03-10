# -*- coding: utf-8 -*-
from gi.repository import GLib
import dbus
import dbus.service
import dbus.mainloop.glib


CONNECT_NAME        = "com.pi.SenderConnectName"
SERVICE_PATH        = "/com/pi/SenderServicePath"
PUBILC_NAME         = "com.pi.SenderPublicName"
TARGET_CONNECT_NAME = "com.pi.ForwardConnectName"
TARGET_SERVICE_PATH = "/com/pi/ForwardServicePath"

class SendMessage(dbus.service.Object):
    def __init__(self, conn=None, object_path=None):
        dbus.service.Object.__init__(self, conn, object_path)

    
    def start(self):
	    print(">>>>>>>>>>>>>>>>>>>>>>>>>>> start send message servcie")


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    name = dbus.service.BusName(CONNECT_NAME, session_bus)

    busObject = session_bus.get_object(TARGET_CONNECT_NAME,TARGET_SERVICE_PATH)
    service = SendMessage(session_bus, SERVICE_PATH)
    service.start()
    for x in range(1,100):
        busObject.receive_data(str(x)+" hello, kyj",dbus_interface = PUBILC_NAME)

    mainloop = GLib.MainLoop()
    print("Running Send Message Service.")
    mainloop.run()
