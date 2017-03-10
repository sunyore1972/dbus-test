#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dbus/dbus-glib.h>
#include <dbus/dbus.h>
#include <unistd.h>

#define D_CONNECT_NAME		 "com.pi.SenderConnectName"
#define D_SERVICE_PATH		"/com/pi/SenderServicePath"
#define D_INTERFACE_NAME	 "com.pi.SenderPublicName"

#define D_TARGET_NAME		 "com.pi.ForwardConnectName"
#define D_TARGET_PATH		"/com/pi/ForwardServicePath"
#define D_TARGET_IFACE	     "com.pi.ForwardPublicName"

DBusConnection * connect_dbus(char *connection_name)
{
    DBusConnection *dbus;
    DBusError      err;
    int            ret;

    dbus_error_init(&err);
    dbus = dbus_bus_get(DBUS_BUS_SESSION, &err);    
    if(dbus == NULL){
        if(dbus_error_is_set(&err)){
    	    printf("ConnectionErr : %s\n", err.message);
            dbus_error_free(&err);
        }
        return NULL;
	}

    ret = dbus_bus_request_name(dbus, connection_name, DBUS_NAME_FLAG_REPLACE_EXISTING, &err);
    if(ret != DBUS_REQUEST_NAME_REPLY_PRIMARY_OWNER){
    	if(dbus_error_is_set(&err)){
    		printf("Name Err :%s\n",err.message);
        	dbus_error_free(&err);
    	}
        return NULL;
	}

    printf("%s\n",__func__);
    return dbus;
}

int method_arg_string_func(DBusMessage *msg, void *param) 
{
    DBusMessageIter arg;
    char * strparam = (char *)param;

    if(msg == NULL)
        return -1;

    if(param != NULL) {
        dbus_message_iter_init_append(msg, &arg);
        if(!dbus_message_iter_append_basic(&arg, DBUS_TYPE_STRING, &strparam)) {
            printf("Out of Memory\n");
            return -2;
        }
    }
    printf("%s\n",__func__);
    return 0;
}

int method_call_without_reply(DBusConnection * connection, 
							  const char *func, 
							  int (*argfunc)(DBusMessage *msg, void *param), 
							  void *param)
{
    DBusError err;
    DBusMessage * msg;
    dbus_uint32_t  serial =0;

    dbus_error_init(&err);
    msg = dbus_message_new_method_call(D_TARGET_NAME, D_TARGET_PATH, D_INTERFACE_NAME, func);
    //msg = dbus_message_new_method_call(D_TARGET_NAME, D_TARGET_PATH, D_TARGET_IFACE, func);
    if(msg == NULL){
        printf("Message is NULL\n");
        return -1;
    }

    if(argfunc != NULL) {
        if(argfunc(msg, param) < 0) {
            printf("set param of message faili\n");
            return -2;
        }
    }

    if(!dbus_connection_send(connection, msg, &serial)){
    	printf("Out of Memory\n");
        dbus_message_unref(msg);
        return -3;
    }

    dbus_connection_flush(connection);
    dbus_message_unref(msg);

    printf("%s\n",__func__);

    return 0;
}

void send_message(DBusConnection *dbus, char *receive_func, char *message) 
{
	method_call_without_reply(dbus, receive_func, method_arg_string_func, message);
}


int main() {
	DBusConnection * dbus = NULL;
	dbus = connect_dbus(D_CONNECT_NAME);
	if(dbus == NULL) {
		printf("bus connection fail\n");
		return -1;
	}

	send_message(dbus,"receive_data",">>>>>>>>>>>>>>>>>>>>> Hello World!");

    printf("%s\n",__func__);
	return 0;
}
