#####################################################
#Makefile for C project
#please change name of TARGET INCPATH LIBS
#####################################################
TARGET        = dbus_csender
BUILDVERSION  = $(shell date +%Y%m%d)

CC            = gcc
CXX           = g++

DEFINES		  = -DBUILDVERSION=$(BUILDVERSION)
CFLAGS        = -pipe -O2 -Wall -W -D_REENTRANT $(DEFINES)
CXXFLAGS      = -Wall -g

INCPATH       = -I/usr/include/glib-2.0 \
				-I/usr/include/dbus-1.0 \
				-I/usr/lib/x86_64-linux-gnu/glib-2.0/include \
				-I/usr/lib/x86_64-linux-gnu/dbus-1.0/include
LDPATH        = 
LIBS          = -lrt -ldbus-1 -lglib-2.0

DESTDIR       = 

SOURCES       = $(wildcard *.c)
OBJECTS       = $(patsubst %.c,%.o,$(SOURCES))


all: $(TARGET)

$(TARGET):$(OBJECTS)  
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJECTS) $(LDPATH) $(LIBS)
	
%.o:%.c
	$(CC) $(CFLAGS) $(INCPATH) -c $<

clean:
	rm *.o $(TARGET)
