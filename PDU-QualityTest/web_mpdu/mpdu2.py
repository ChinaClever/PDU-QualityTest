from quality_mpdu.mpdu_web import  *
import datetime

class Mpdu2(MpduWeb):

    def start_fun(self , sock , dest_ip , dest_port):
        cfg = self.cfgs
        security = cfg['security']
        if( int(security) == 0):
            self.ip_prefix = 'http://'
        else:
            self.ip_prefix = 'https://'
        self.sock = sock
        self.ip = dest_ip
        self.port = dest_port
        intRet , message = self.login()
        self.sendtoMainapp(message)
        if(intRet == 0):
            return
        intRet , message = self.checkVersion()
        self.sendtoMainapp(message)
        if(intRet == 0):
            return
            
        opLists = self.opThreshold()
        opLists.sort()
        
        self.changetocorrect()
        self.checkCorrectHtml()
        
        self.checkTitleBar2()
        if( int(cfg['series']) != 1 and int(cfg['series']) != 5 ):
            self.checkTitleBar3(opLists)
        if( int(cfg['series']) == 3 or int(cfg['series']) == 4 ):
            self.openOrOffTitleBar5( False )
            self.confirmTips( False )
            self.checkTitleBar5( False )
            self.openOrOffTitleBar5( True )
            #self.confirmTips( True )
            #self.checkTitleBar5( True )
        self.clearEnergy()
        
        self.setModbusMode()
        self.checkModbusMode()
        
        self.checkTime()
        self.clearLogs()
        self.resetFactory()
        
    def setModbusMode(self):
        self.divClick(3)
        if( int(self.cfgs['security']) == 1 ):
            time.sleep(1)
        time.sleep(0.35)
        self.driver.find_element_by_id("biao1").click()
        time.sleep(0.35)
        jsSheet = 'var j = document.getElementById(\"line-dev\").value;var a = document.getElementById(\"device\").value;var encodeName = encodeURI(encodeURI(a));var c = 0;var e = document.getElementById(\"beep\").value;var g = document.getElementById(\"slave\").value;var h = document.getElementById(\"baud\").value;var sBox = document.getElementById(\"sersonBox\").value;xmlset = createXmlRequest();xmlset.onreadystatechange = setdata_a;ajaxget(xmlset, \"/setdevice?a=\" + encodeName + \"&b=\" + c + \"&c=\" + e + \"&d=\" + g + \"&e=\" + h + \"&f=\" + j + \"&g=\" + sBox + \"&h=\" + {0} + \"&\")'
        self.execJs(jsSheet.format(int(self.cfgs['modbus'])))
        time.sleep(0.35)
        
    def checkModbusMode(self):
        time.sleep(0.35)
        self.driver.find_element_by_id("biao1").click()
        time.sleep(0.35)
        status , message = self.check( 'CascadeWay' , self.cfgs['modbus'] , 'IN/OUT级联方式')
        self.sendtoMainapp(message)
        
    def clearLogs(self):
        cfg = self.cfgs
        jsSheet = 'var xmlset = createXmlRequest();xmlset.onreadystatechange = setdata;var clearUrl = Encryption(\"/setlclear\");ajaxget(xmlset, clearUrl + \"?a=\" + {0} + \"&\")'
        if int(cfg['versions']) <= 14:
            jsSheet = 'var xmlset = createXmlRequest();xmlset.onreadystatechange = setdata;ajaxget(xmlset, \"/setlclear?a=\" + {0} + \"&\");'
        flag = False
        ListMessage = []
        ListMessage.append('报警日志清除失败;0')
        ListMessage.append('操作日志清除失败;0')
        
        self.divClick(6)
        time.sleep(1)
        if( int(self.cfgs['security']) == 1 ):
            time.sleep(2.5)
        for num in range(0, 2):
            self.execJs(jsSheet.format(num))
            time.sleep(0.35)
            self.driver.find_element_by_id('biao{0}'.format(num+1)).click()
            time.sleep(1)
            tt = self.driver.find_element_by_id('evenlognum').text
            if( tt != 'Total : 0'):
                self.sendtoMainapp(ListMessage[num])
                flag = True
        if(flag == False):    
            message = '清除日志成功;1'
            self.sendtoMainapp(message)
            
    def close(self):
        #print(datetime.datetime.now())
        try:
            time.sleep(1)
            self.driver.quit()
        #print(datetime.datetime.now())
        except:
            print("except")
        finally:
            time.sleep(5)
        
        

    def changetocorrect(self):
        cfg = self.cfgs
        ip = self.ip_prefix + cfg['ip_addr'] + '/correct.html'
        
        try:
            self.driver.get(ip)
        except:
            self.sendtoMainapp('账号密码错误;0')
            time.sleep(0.35)
            #self.sendtoMainapp('MAC-1')
            return
        else:
            time.sleep(0.35)
            self.driver.switch_to.default_content()
        

    def setCorrect2(self):
        cfg = self.cfgs
        
        jsSheet = 'var claerlimit = createXmlRequest();claerlimit.onreadystatechange = setdatlimit;ajaxget(claerlimit, \"/alllimit?a=\" +{limit1}+\"&b=\"+{limit2} +\"&c=\"+{limit3} + \"&d=\"+{limit4}+\"&e=\"+{limit5} +\"&f=\"+{limit6} + \"&g=\"+{limit7}+\"&h=\"+{limit8} +\"&i=\"+{limit9} + \"&j=\"+{limit10}+\"&k=\"+{limit11} + \"&l=\"+{limit12} +\"&m=\"+{limit13} + \"&n=\"+{limit14} +\"&\");'.format( limit1 = int(cfg['vol_min'])*10 , limit2 = int(cfg['vol_max'])*10 , limit3 = int(cfg['cur_min'])*100 , limit4 = int(cfg['cur_max'])*100 ,limit5 = int(cfg['tem_min']) , limit6 = int(cfg['tem_max']),limit7 = int(cfg['hum_min']) , limit8 = int(cfg['hum_max']) ,limit9 = int(cfg['output_min'])*100 , limit10 = int(cfg['output_crmin'])*100 , limit11 = int(cfg['output_crmax'])*100 , limit12 = int(cfg['output_max'])*100 , limit13 = int(cfg['cur_crmin'])*100 , limit14 = int(cfg['cur_crmax'])*100)
        
        self.execJs(jsSheet)
        time.sleep(0.25)
        
    def checkCorrectHtml(self):
        cfg = self.cfgs
        status , message = self.check( 'line1' , cfg['lines'] , '相数')
        self.sendtoMainapp(message)
        
        status , message = self.check( 'line2' , cfg['boards'] , '执行板数')
        self.sendtoMainapp(message)
        
        status , message = self.check( 'line8' , cfg['board_1'] , '第1块执行板输出位数')
        self.sendtoMainapp(message)
        status , message = self.check( 'line9' , cfg['board_2'] , '第2块执行板输出位数')
        self.sendtoMainapp(message)
        status , message = self.check( 'line10' , cfg['board_3'] , '第3块执行板输出位数')
        self.sendtoMainapp(message)
        
        status , message = self.check( 'line4' , cfg['loops'] , '回路数')
        self.sendtoMainapp(message)
        
        loop = int(cfg['loops'])
        if( loop >= 1):
            status , message = self.check( 'line5' , cfg['loop_1'] , '第1回路输出位数')
            self.sendtoMainapp(message)
        if( loop >= 2):
            status , message = self.check( 'line6' , cfg['loop_2'] , '第2回路输出位数')
            self.sendtoMainapp(message)
        if( loop >= 3):
            status , message = self.check( 'line7' , cfg['loop_3'] , '第3回路输出位数')
            self.sendtoMainapp(message)
        if( loop >= 4):
            status , message = self.check( 'cuit1' , cfg['loop_4'] , '第4回路输出位数')
            self.sendtoMainapp(message)
        if( loop >= 5):
            status , message = self.check( 'cuit2' , cfg['loop_5'] , '第5回路输出位数')
            self.sendtoMainapp(message)
        if( loop >= 6):
            status , message = self.check( 'cuit3' , cfg['loop_6'] , '第6回路输出位数')
            self.sendtoMainapp(message)
        
        status , message = self.check( 'line3' , cfg['breaker'] , '带不带断路器')
        self.sendtoMainapp(message)
        
        status , message = self.check( 'VerticalLevel' , cfg['level'] , '垂直/水平')
        self.sendtoMainapp(message)
        
        status , message = self.check( 'neutral' , cfg['standar'] , '标准/中性')
        self.sendtoMainapp(message)
        
        #status , message = self.check( 'serial' , cfg['modbus'] , 'IN/OUT级联方式')
        #self.sendtoMainapp(message)
        
        status , message = self.check( 'sensorbox' , cfg['envbox'] , '带不带传感器盒子')
        self.sendtoMainapp(message)
        
        status , message = self.check( 'type' , cfg['series'] , '系列')
        self.sendtoMainapp(message)
        
        status , message = self.check( 'language' , cfg['language'] , '中英文')
        self.sendtoMainapp(message)
        
        status , message = self.macAddrCheck( 'mac1' , 'mac地址')
        self.sendtoMainapp(message)
        
        self.driver.back()
        
    def checkTitleBar2(self):
        cfg = self.cfgs
        self.divClick(2)
        if( int(self.cfgs['security']) == 1 ):
            time.sleep(1)
        time.sleep(0.35)
        self.driver.find_element_by_id("titlebar2").click()
        time.sleep(0.35)
        
        self.setAlarmTcur()
        self.setNormalTcur()
        
        self.checkTcur()
        self.checkCcur()
        
        self.checkTvol()
        self.checkTem()
        #self.checkCurTem()
      
        self.checkHum()
        #self.checkCurHum()
        
        if( int(cfg['envbox']) == 1):
            self.checkEnvBoxTem()
            #self.checkEnvBoxCurTem()
      
            self.checkEnvBoxHum()
            #self.checkEnvBoxCurHum()
    
    
    
    def checkTcur(self):
        cfg = self.cfgs
        line = int(cfg['lines'])
        list=[]
        cfgStr = []
        outputStr = []
       
        for i in range(1 , line+1):
            list.append('Tcmin{0}'.format(i))
            list.append('Txcmin{0}'.format(i))
            list.append('Txcmax{0}'.format(i))
            list.append('Tcmax{0}'.format(i))
            cfgStr.append('cur_min')
            cfgStr.append('cur_crmin')
            cfgStr.append('cur_crmax')
            cfgStr.append('cur_max')
            outputStr.append('L{0}总电流最小值'.format(i))
            outputStr.append('L{0}总电流下临界值'.format(i))
            outputStr.append('L{0}总电流上临界值'.format(i))
            outputStr.append('L{0}总电流最大值'.format(i))
                    
        self.checkAndSendTitleBar3(list , cfgStr , outputStr , 1)
        
    def checkCcur(self):
        cfg = self.cfgs
        loop = int(cfg['loops'])
        list=[]
        cfgStr = []
        outputStr = []
       
        for i in range(1 , loop+1):
            list.append('cumin{0}'.format(i))
            list.append('cxmin{0}'.format(i))
            list.append('cxmax{0}'.format(i))
            list.append('cumax{0}'.format(i))
            cfgStr.append('cur_min')
            cfgStr.append('cur_crmin')
            cfgStr.append('cur_crmax')
            cfgStr.append('cur_max')
            outputStr.append('C{0}电流最小值'.format(i))
            outputStr.append('C{0}电流下临界值'.format(i))
            outputStr.append('C{0}电流上临界值'.format(i))
            outputStr.append('C{0}电流最大值'.format(i))
                    
        self.checkAndSendTitleBar3(list , cfgStr , outputStr , 7)
        
    def setCcur(self):
        cfg = self.cfgs
        loop = int(cfg['loops'])
        a , b , c , d = self.checkLoopValue(cfg['cur_min']),self.checkLoopValue(cfg['cur_crmin']),self.checkLoopValue(cfg['cur_crmax']),self.checkLoopValue(cfg['cur_max'])
        for i in range(14 , 15+loop):
            jsSheet = 'var slave1 = document.getElementById(\"slave\").value;var xmlset = createXmlRequest();xmlset.onreadystatechange = setdata;ajaxget(xmlset, \"/setlimit?a=\" + slave1 + \"&b=\" + {action} + \"&c=\" + {Tcmin} + \"&d=\" + {Tcmax} + \"&e=\" + {Txcmin}  + \"&f=\" + {Txcmax}+  \"&\");'.format( action = i , Tcmin = a*100 , Tcmax = d*100 , Txcmin = b*100 , Txcmax = c*100)
            self.execJs(jsSheet)
        
    def checkLoopValue(self , value):
        cfg = self.cfgs
        line = int(cfg['lines'])
        loop = int(cfg['loops'])
        fileValue = int(value)
        if( line == loop ):
            fileValue = int(value)
        elif( line == loop/2 ):
            if( int(value) % 2 == 1 ):
                fileValue = (int(value)+1)/2
            else:
                fileValue = int(value)/2
        elif( line == loop/4 ):
            if( int(value) % 2 == 1 ):
                fileValue = (int(value)+1)/4
            else:
                fileValue = int(value)/4
        return fileValue
    
    def checkTvol(self):
        cfg = self.cfgs
        line = int(cfg['lines'])
        list=[]
        cfgStr = []
        outputStr = []
       
        for i in range(1 , line+1):
            list.append('Tvmin{0}'.format(i))
            list.append('Tvmax{0}'.format(i))
            cfgStr.append('vol_min')
            cfgStr.append('vol_max')
            outputStr.append('L{0}总电压最小值'.format(i))
            outputStr.append('L{0}总电压最大值'.format(i))
        self.checkAndSendTitleBar3(list , cfgStr , outputStr , 2)
        
    def checkTem(self):
        list=[]
        cfgStr = []
        outputStr = []
       
        for i in range(1 , 2+1):
            list.append('Temmin{0}'.format(i))
            list.append('Temmax{0}'.format(i))
            cfgStr.append('tem_min')
            cfgStr.append('tem_max')
            outputStr.append('温度{0}最小值'.format(i))
            outputStr.append('温度{0}最大值'.format(i))
            
        self.checkAndSendTitleBar3(list , cfgStr , outputStr , 3)
        
    def checkCurTem(self):
        list=[]
        cfgStr = []
        outputStr = []
       
        for i in range(1 , 2+1):
            list.append('Tem{0}'.format(i))
            cfgStr.append('-')
            outputStr.append('温度{0}'.format(i))
            
        self.checkAndSendTitleBar3(list , cfgStr , outputStr , 8)
        
    def checkHum(self):
        list=[]
        cfgStr = []
        outputStr = []
       
        for i in range(1 , 2+1):
            list.append('Hummin{0}'.format(i))
            list.append('Hummax{0}'.format(i))
            cfgStr.append('hum_min')
            cfgStr.append('hum_max')
            outputStr.append('湿度{0}最小值'.format(i))
            outputStr.append('湿度{0}最大值'.format(i))
            
        self.checkAndSendTitleBar3(list , cfgStr , outputStr , 4)
        
    def checkCurHum(self):
        list=[]
        cfgStr = []
        outputStr = []
       
        for i in range(1 , 2+1):
            list.append('Hum{0}'.format(i))
            cfgStr.append('-')
            outputStr.append('湿度{0}'.format(i))
            
        self.checkAndSendTitleBar3(list , cfgStr , outputStr , 9)
        
    def checkEnvBoxTem(self):
        list=[]
        cfgStr = []
        outputStr = []
       
        for i in range(1 , 2+1):
            list.append('boxtemmin{0}'.format(i))
            list.append('boxtemmax{0}'.format(i))
            cfgStr.append('tem_min')
            cfgStr.append('tem_max')
            outputStr.append('温度{0}最小值'.format(i+2))
            outputStr.append('温度{0}最大值'.format(i+2))
            
        self.checkAndSendTitleBar3(list , cfgStr , outputStr , 5)
        
    def checkEnvBoxCurTem(self):
        list=[]
        cfgStr = []
        outputStr = []
       
        for i in range(1 , 2+1):
            list.append('boxtem{0}'.format(i))
            cfgStr.append('-')
            outputStr.append('湿度{0}'.format(i+2))
            
        self.checkAndSendTitleBar3(list , cfgStr , outputStr , 10)
        
    def checkEnvBoxHum(self):
        list=[]
        cfgStr = []
        outputStr = []
       
        for i in range(1 , 2+1):
            list.append('boxhummin{0}'.format(i))
            list.append('boxhummax{0}'.format(i))
            cfgStr.append('hum_min')
            cfgStr.append('hum_max')
            outputStr.append('湿度{0}最小值'.format(i+2))
            outputStr.append('湿度{0}最大值'.format(i+2))
            
        self.checkAndSendTitleBar3(list , cfgStr , outputStr , 6)
        
    def checkEnvBoxCurHum(self):
        list=[]
        cfgStr = []
        outputStr = []
       
        for i in range(1 , 2+1):
            list.append('boxhum{0}'.format(i))
            cfgStr.append('-')
            outputStr.append('湿度{0}'.format(i+2))
            
        self.checkAndSendTitleBar3(list , cfgStr , outputStr , 11)
        

    def checkAndSendTitleBar3(self , list , cfgStr , outputStr , case):
        cfg = self.cfgs
        zz = zip(list , cfgStr , outputStr)
        statusList = []
        messageList = []
        if( case < 7 ):
            for x,y,z in zz:
                status , message = self.checkStr( x , cfg[y] , z)
                statusList.append(status)
                messageList.append(message)
        elif( case == 7 ):
            for x,y,z in zz:
                status , message = self.checkStr2( x , cfg[y] , z)
                statusList.append(status)
                messageList.append(message)
        elif( case > 7 ):
            for x,y,z in zz:
                status , message = self.checkTemAndHum( x , z )
                statusList.append(status)
                messageList.append(message)
        
        phaseStr = zip(statusList , messageList)
        flag = False
        for x,y in phaseStr:
            if( x==0 or x==2 ):
                self.sendtoMainapp(y)
                flag = True
        if( flag == False):
            if( case == 1):
                self.sendtoMainapp("检查总电流最小值成功;1" )
                self.sendtoMainapp("检查总电流下临界值成功;1" )
                self.sendtoMainapp("检查总电流上临界值成功;1" )
                self.sendtoMainapp("检查总电流最大值成功;1" )
            elif( case == 2):
                self.sendtoMainapp("检查总电压最小值成功;1" )
                self.sendtoMainapp("检查总电压最大值成功;1" )
            elif( case == 3):
                self.sendtoMainapp("检查温度最小值成功;1" )
                self.sendtoMainapp("检查温度最大值成功;1" )
            elif( case == 4):
                self.sendtoMainapp("检查湿度最小值成功;1" )
                self.sendtoMainapp("检查湿度最大值成功;1" )
            elif( case == 5):
                self.sendtoMainapp("检查传感器盒子温度最小值成功;1" )
                self.sendtoMainapp("检查传感器盒子温度最大值成功;1" )
            elif( case == 6):
                self.sendtoMainapp("检查传感器盒子湿度最小值成功;1" )
                self.sendtoMainapp("检查传感器盒子湿度最大值成功;1" )
            elif( case == 7):
                self.sendtoMainapp("检查回路电流最小值成功;1" )
                self.sendtoMainapp("检查回路电流下临界值成功;1" )
                self.sendtoMainapp("检查回路电流上临界值成功;1" )
                self.sendtoMainapp("检查回路电流最大值成功;1" )
            elif( case == 8):
                self.sendtoMainapp("检查温度当前值成功;1" )
            elif( case == 9):
                self.sendtoMainapp("检查湿度当前值成功;1" )
            elif( case == 10):
                self.sendtoMainapp("检查传感器盒子温度当前值成功;1" )
            elif( case == 11):
                self.sendtoMainapp("检查传感器盒子湿度当前值成功;1" )
        statusList.clear()
        messageList.clear()
            
    def checkTitleBar3(self , opLists):
        cfg = self.cfgs
        self.divClick(2)
        
        if( int(self.cfgs['security']) == 1 ):
            time.sleep(1)
        time.sleep(0.35)
        self.driver.find_element_by_id("titlebar3").click()
        time.sleep(0.35)
        
        op = cfg['outputs']
        if( int(cfg['series']) == 2 or int(cfg['series']) == 4):#输出位
            list=[]
            cfgStr = []
            outputStr = []
           
            for i in range(1 , int(op)+1):
                list.append('min{0}'.format(i))
                list.append('xmin{0}'.format(i))
                list.append('xmax{0}'.format(i))
                list.append('max{0}'.format(i))
                cfgStr.append('output_min')
                cfgStr.append('output_crmin')
                cfgStr.append('output_crmax')
                cfgStr.append('output_max')
                outputStr.append('输出位{0}电流最小值'.format(i))
                outputStr.append('输出位{0}电流下临界值'.format(i))
                outputStr.append('输出位{0}电流上临界值'.format(i))
                outputStr.append('输出位{0}电流最大值'.format(i))
                j = 0
                while( j < len(opLists) ):
                    if( len(opLists[j]) != 0):
                        if( opLists[j][0] == i ):
                            index = opLists[j][6]
                            cfgStr[(i-1)*4]='op_{0}_min'.format(index)
                            cfgStr[(i-1)*4+1]='op_{0}_crmin'.format(index)
                            cfgStr[(i-1)*4+2]='op_{0}_crmax'.format(index)
                            cfgStr[(i-1)*4+3]='op_{0}_max'.format(index)
                            
                    j+=1
               
            zz = zip(list , cfgStr , outputStr)
            
            statusList = []
            messageList = []
            for x,y,z in zz:
                status , message = self.checkStr( x , cfg[y] , z) 
                statusList.append(status)
                messageList.append(message)
                
            opStr = zip(statusList , messageList)
            flag = False
            for x,y in opStr:
                if( x==0 or x==2 ):
                    self.sendtoMainapp( y )
                    flag = True
            if( flag == False):
                self.sendtoMainapp("检查输出位电流最小值成功;1" )
                self.sendtoMainapp("检查输出位电流下临界值成功;1" )
                self.sendtoMainapp("检查输出位电流上临界值成功;1" )
                self.sendtoMainapp("检查输出位电流最大值成功;1" )
        if( int(cfg['series']) == 3 or int(cfg['series']) == 4):#延时
            try:
                message =''
                self.driver.find_element_by_id('totalms')
            except NoSuchElementException:
                message =  '网页上找不到{0}ID;'.format('延时上电')
                self.sock.sendto(message.encode('utf-8') , (self.ip , self.port))
                return
            self.setItById('totalms', 1 , '上电延时')
            
            jsSheet = 'var slave = document.getElementById(\"slave\").value;var ms = parseFloat(document.getElementById(\"totalms\").value) ;xmlset2 = createXmlRequest();xmlset2.onreadystatechange = setdata2;ajaxget(xmlset2, \"/settime?a=\" + slave + \"&b=\" + {0}  + \"&\");'
            if( int(cfg['versions']) == 16 ):
                jsSheet = 'var setUrl = Encryption(\"/settime\");var slave = document.getElementById(\"slave\").value;var ms = parseFloat(document.getElementById(\"totalms\").value) ;xmlset2 = createXmlRequest();xmlset2.onreadystatechange = setdata2;ajaxget(xmlset2, setUrl+\"?a=\" + slave + \"&b=\" + {0}  + \"&\");'
            self.execJs(jsSheet.format(1))
            time.sleep(1)
            self.checkDelayTime(op)
    
    def confirmTips(self , onFlag ):
        cfg = self.cfgs
        op = int(cfg['outputs'])
        try:
            if( onFlag == True ):
                jsSheet = 'if(confirm("输出位指示灯是否顺序打开")){alert("确认顺序打开");}else{alert("不是顺序打开");}'
                self.execJs(jsSheet)
                while( True ):
                    alert = self.driver.switch_to_alert().text
                    if( alert == '输出位指示灯是否顺序打开' ):
                        time.sleep(1)
                    elif( alert == '确认顺序打开' ):
                        self.sendtoMainapp('输出位指示灯确认顺序打开;1')
                        break
                    elif( alert == '不是顺序打开' ):
                        self.sendtoMainapp('输出位指示灯不是顺序打开;0')
                        break
                
            else:
                jsSheet = 'if(confirm("输出位指示灯是否顺序关闭")){alert("确认顺序关闭");}else{alert("不是顺序关闭");}'
                self.execJs(jsSheet)
                while( True ):
                    alert = self.driver.switch_to_alert().text
                    if( alert == '输出位指示灯是否顺序关闭' ):
                        time.sleep(1)
                    elif( alert == '确认顺序关闭' ):
                        self.sendtoMainapp('输出位指示灯确认顺序关闭;1')
                        break
                    elif( alert == '不是顺序关闭' ):
                        self.sendtoMainapp('输出位指示灯不是顺序关闭;0')
                        break
            self.driver.switch_to.alert.accept()
        except  :
            print('exception')
        finally:
            time.sleep(op)
    
    def openOrOffTitleBar5(self , onFlag):
        cfg = self.cfgs
        #self.divClick(2)
        
        if( int(self.cfgs['security']) == 1 ):
            time.sleep(1)
        time.sleep(0.35)
        self.driver.find_element_by_id("titlebar5").click()
        time.sleep(0.35)
        if( onFlag == True ):
            self.driver.find_element_by_id('seton43').click()
            time.sleep(int(self.cfgs['outputs'])-6)
        else:
            self.driver.find_element_by_id('setoff43').click()
    
    def checkTitleBar5(self , onFlag):
        cfg = self.cfgs
        #self.divClick(2)
        
        if( int(self.cfgs['security']) == 1 ):
            time.sleep(1)
        time.sleep(0.35)
        self.driver.find_element_by_id("titlebar5").click()
        time.sleep(0.35)
        
        op = cfg['outputs']
        statusList = []
        messageList = []
        
        
        for i in range(1 , int(op)+1):
            sw = 'Csw{0}'.format(i)
            status , message = '' ,''
            if( onFlag == True):
                if( int(cfg['language']) == 1 ):
                    status , message = self.checkSWStr( sw , '开' , '开关{0}'.format(i))
                else:
                    status , message = self.checkSWStr( sw , 'ON' , '开关{0}'.format(i))
            else:
                if( int(cfg['language']) == 1 ):
                    status , message = self.checkSWStr( sw , '关' , '开关{0}'.format(i))
                else:
                    status , message = self.checkSWStr( sw , 'OFF' , '开关{0}'.format(i))
            statusList.append(status)
            messageList.append(message)
            
        msStr = zip(statusList , messageList)
        flag = False
        for x,y in msStr:
            if( x==0 or x==2):
                self.sendtoMainapp(y)
                flag = True
        if( flag == False):
            self.sendtoMainapp("网页开关状态检查成功;1" )
            
    def checkDelayTime(self , op):
        self.driver.find_element_by_id("titlebar3").click()
        time.sleep(1)
        statusList = []
        messageList = []
        for i in range(1 , int(op)+1):
            ms = 'ms{0}'.format(i)
            status , message = '' ,''
            if( int(self.cfgs['series']) == 3 or int(self.cfgs['series']) == 4):
                status , message = self.checkStr( ms , '1' , '上下电延时')
            else:
                status , message = self.checkStr( ms , '0' , '上下电延时')
            
            statusList.append(status)
            messageList.append(message)
            
        msStr = zip(statusList , messageList)
        flag = False
        for x,y in msStr:
            if( x==0 or x==2):
                self.sendtoMainapp(y)
                flag = True
        if( flag == False):
            self.sendtoMainapp("检查上下电延时成功;1" )
            
    def checkEnergy(self):
        cfg = self.cfgs
        statusList = []
        messageList = []
        line = int(cfg['lines'])
        for i in range(1 , line+1):
            Tenergy = 'Tenergy{0}'.format(i)
            status = 0
            try:
                tt = self.driver.find_element_by_id(Tenergy).text
                #print(tt)
                if( tt == '0' ):
                    status = 1
                    message ='L{0}清除电能成功;'.format(i)+str(1)
                else:
                    status = 0
                    message = 'L{0}清除电能失败;'.format(i)+str(0)
            except NoSuchElementException:
                message =  '网页上找不到{0}ID;'.format(Tenergy)+str(2)
                self.sendtoMainapp(message)
                continue
            
            statusList.append(status)
            messageList.append(message)
            
        TenergyStr = zip(statusList , messageList)
        flag = False
        for x,y in TenergyStr:
            if( x==0 or x==2 ):
                self.sendtoMainapp(y)
                flag = True
        if( flag == False):
            self.sendtoMainapp("清除电能成功;1" )  
        
    def clearEnergy(self):
        cfg = self.cfgs#Tenergy1Tenergy2Tenergy3
        self.divClick(2)#Cenergy1
        if( int(self.cfgs['security']) == 1 ):
            time.sleep(1)
        time.sleep(0.5)
        self.driver.find_element_by_id("titlebar4").click()
        time.sleep(0.5)
        
        #line = int(cfg['lines'])
        line = 3
        jsSheet = 'var slave1 = document.getElementById(\"slave\").value;var claerset = createXmlRequest();claerset.onreadystatechange = clearrec;ajaxget(claerset, \"/setenergy?a=\" + slave1 + \"&b=\" + {0}+\"&\");'
        if( int(cfg['versions']) == 16 ):
            jsSheet = 'var setUrl = Encryption(\"/setenergy\");var slave1 = document.getElementById(\"slave\").value;var claerset = createXmlRequest();claerset.onreadystatechange = clearrec;ajaxget(claerset, setUrl+\"?a=\" + slave1 + \"&b=\" + {0}+\"&\");'
        for i in range(1,line+1):
            self.execJs(jsSheet.format(i))
            time.sleep(1)
        time.sleep(6)
        self.driver.find_element_by_id("titlebar4").click()
        time.sleep(1)
        self.checkEnergy()
        
    def setTime(self):
        self.divClick(4)
        if( int(self.cfgs['security']) == 1 ):
            time.sleep(1)
        time.sleep(0.5)
        self.driver.find_element_by_id("biao6").click()
        time.sleep(0.5)
        jsSheet = 'var b = loctime.innerHTML;var g = parseInt(b.substr(8, 2), 10);var f = parseInt(b.substr(3, 2), 10);var a = parseInt(b.substr(0, 2), 10);var d = parseInt(b.substr(11, 2), 10);var e = parseInt(b.substr(14, 2), 10);var c = parseInt(b.substr(17, 2), 10);if (g.length < 2) {g = \"0\" + g}if (f.length < 2) {f = \"0\" + f}if (a.length < 2) {a = \"0\" + a}if (d.length < 2) {d = \"0\" + d}if (e.length < 2) {e = \"0\" + e}if (c.length < 2) {c = \"0\" + c}var xmlset = createXmlRequest();xmlset.onreadystatechange = setdata;ajaxget(xmlset, \"/setdtime?a=\" + g + \"&b=\" + f + \"&c=\" + a + \"&d=\" + d + \"&e=\" + e + \"&f=\" + c + \"&\")'
        
        self.execJs(jsSheet)
        time.sleep(0.25)
        #self.sendtoMainapp("检查时间成功;1" )
    
    def opThreshold(self):
        cfg = self.cfgs
        minList , maxList , enList , idList , crminList , crmaxList , indexList= [],[],[],[],[],[],[]
        minStr , maxStr , enStr , idStr , crminStr , crmaxStr = 'op_{0}_min','op_{0}_max','op_{0}_en','op_{0}_id','op_{0}_crmin','op_{0}_crmax'
        
        for i in range(1,7):
            minList.append(minStr.format(i))
            maxList.append(maxStr.format(i))
            enList.append(enStr.format(i))
            idList.append(idStr.format(i))
            crminList.append(crminStr.format(i))
            crmaxList.append(crmaxStr.format(i))
            indexList.append(i)
            
        lists =[[]for i in range(6)]
        zz = zip(minList , maxList , enList , idList , crminList , crmaxList,indexList)
        index = 0
        for min , max , en , id , crmin , crmax ,index in zz:
            if(int(cfg[id]) != 0 and int(cfg[en]) == 1):
                lists[index].append(int(cfg[id]))
                lists[index].append(int(cfg[en]))
                lists[index].append(int(cfg[min]))
                lists[index].append(int(cfg[crmin]))
                lists[index].append(int(cfg[crmax]))
                lists[index].append(int(cfg[max]))
                lists[index].append(index)
                index += 1
        return lists
    
    
    def checkTime(self):
        self.divClick(4)
        if( int(self.cfgs['security']) == 1 ):
            time.sleep(2)
        time.sleep(1)
        self.driver.find_element_by_id("biao6").click()
        time.sleep(1)
        
        nowTime = self.driver.find_element_by_id('loctime').text.split( )
        devTime = self.driver.find_element_by_id('devtime1').text.split( )
        if( nowTime[0] == devTime[0]):
            h1 , m1 , s1 = nowTime[1].split(':')
            t1 = int(h1)*3600 + int(m1)*60 + int(s1)
            h2 , m2 , s2 = devTime[1].split(':')
            t2 = int(h2)*3600 + int(m2)*60 + int(s2)
            if( abs( t1-t2 ) >= 30*60 ):
                self.sendtoMainapp("检查时间时分秒失败;0" )
                return False
            else:
                #print(abs(t1-t2))
                self.sendtoMainapp("检查时间成功;1" )
                return True
        else:
            self.sendtoMainapp("检查时间年月日失败;0" )
            return False