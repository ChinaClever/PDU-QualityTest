from ctrlset_mpdu.mpdu2 import  *
from ctrlset_mpdu.mpdu import  *
import os
import socket
import datetime
#import sys


sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
dest_ip,dest_port = ('127.0.0.1',10086)


if __name__ == '__main__':
    print(datetime.datetime.now())
    
    ver = MpduWeb.getCfg().get("mCfg", "mpdu_ver")
   
    #if( len(ver) == 0):
    #    message = '填入版本不能为空;0'
    #    sock.sendto(message.encode('utf-8-sig') , (dest_ip , dest_port))
    #    sys.exit(0)
    #if( 'P' in ver and 'C' in ver ):
    if( int(ver) == 1):
        app2 = Mpdu2()
        app2.start_fun(sock , dest_ip , dest_port)
        app2.close()
    else:
        app1 = Mpdu()
        app1.start_fun(sock , dest_ip , dest_port)
        app1.close()

