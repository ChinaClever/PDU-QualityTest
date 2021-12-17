from quality_mpdu.mpdu2 import  *
from quality_mpdu.mpdu import  *
from quality_mpdu.mpdu_huawei import  *
import os
import socket
import datetime
#import sys


sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
dest_ip,dest_port = ('127.0.0.1',10086)


if __name__ == '__main__':
    print(datetime.datetime.now())
    
    ver = MpduWeb.getCfg().get("mCfg", "mpdu_ver")
   
    if( int(ver) == 2):
        app2 = Mpdu2()
        app2.start_fun(sock , dest_ip , dest_port)
        app2.close()
    elif(int(ver) == 1):
        app1 = Mpdu()
        app1.start_fun(sock , dest_ip , dest_port)
        app1.close()
    else:
        app3 = MpduHuawei()
        app3.start_fun(sock , dest_ip , dest_port)
        app3.close()
    sock.close()
    time.sleep(1)

