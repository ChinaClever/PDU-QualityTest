from ctrlset_mpdu.mpdu_web import  *
import datetime

class MpduHuawei(MpduWeb):
       
    def start_fun(self , sock , dest_ip , dest_port):
        cfg = self.cfgs
        self.ip_prefix = 'http://'
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
        self.setCorrect2()
        self.setCorrect1()
        time.sleep(5)
        self.login()
        self.changetocorrect()
        self.checkCorrectHtml()
        
        
        self.checkTitleBar2()
        if( int(cfg['series']) != 1 ):
            self.checkTitleBar3(opLists)
        self.clearEnergy()
        self.setTime()
        self.clearLogs()
    

    def clearLogs(self):
        jsSheet = 'var xmlset = createXmlRequest();xmlset.onreadystatechange = setdata;ajaxget(xmlset, \"/setlclear?a=\" + {0} + \"&\");'
        flag = False
        ListMessage = []
        ListMessage.append('报警日志清除失败;0')
        ListMessage.append('操作日志清除失败;0')
        self.divClick(6)
        time.sleep(1)
        for num in range(0, 2):
            self.execJs(jsSheet.format(num))
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
        time.sleep(1.5)
        #print(datetime.datetime.now())
        self.driver.quit()
        #print(datetime.datetime.now())
        time.sleep(3)
        

    def changetocorrect(self):
        cfg = self.cfgs
        ip = self.ip_prefix + cfg['ip_addr'] + '/correct.html'
        
        try:
            self.driver.get(ip)
        except:
            self.sendtoMainapp('账号密码错误;0')
            time.sleep(0.35)
            self.sendtoMainapp('MAC-1')
            return
        else:
            time.sleep(1)
            self.driver.switch_to.default_content()
    
    def setCorrect1(self):
        cfg = self.cfgs
        
        if (len(cfg['mac']) > 5  ):#NoSuchElementException
            strMac =  cfg['mac']
        try:
            self.driver.find_element_by_id('mac1')
        except NoSuchElementException:
            return
        v = self.driver.find_element_by_id('mac1').get_attribute('value')
        if( '2C:26:5F:' not in v):
            v = strMac
        else:
            self.sendtoMainapp('MAC-1')
        jsSheet1 = 'var claerset = createXmlRequest();claerset.onreadystatechange = setmac;ajaxget(claerset, \"/correct?a=\" +1+\"&b=\"+{type}+\"&c=\"+{language} + \"&d=\"+\"{mac1}\" +\"&\");'.format(type = cfg['series'] , language = cfg['language'] , mac1 = v)
        self.execJs(jsSheet1)
        time.sleep(1)
        self.driver.back()
        self.divClick(7)
        time.sleep(0.35)
        self.driver.find_element_by_id("biao1").click()
        time.sleep(0.35)
        jsSheet1 = 'var xmlset = createXmlRequest();xmlset.onreadystatechange = setdata;ajaxget(xmlset, \"/setsys?a=\" + 0 + \"&\");'
        self.execJs(jsSheet1)
        time.sleep(0.25)
        

    def setCorrect2(self):
        cfg = self.cfgs  
        
        jsSheet = 'var claerlimit = createXmlRequest();claerlimit.onreadystatechange = setdatlimit;ajaxget(claerlimit, \"/alllimit?a=\" +{limit1}+\"&b=\"+{limit2} +\"&c=\"+{limit3} + \"&d=\"+{limit4}+\"&e=\"+{limit5} +\"&f=\"+{limit6} + \"&g=\"+{limit7}+\"&h=\"+{limit8} +\"&i=\"+{limit9} + \"&j=\"+{limit10}+\"&k=\"+{limit11} + \"&l=\"+{limit12} +\"&m=\"+{limit13} + \"&n=\"+{limit14} +\"&\");'.format( limit1 = cfg['vol_min'] , limit2 = cfg['vol_max'] , limit3 = int(cfg['cur_min'])*10 , limit4 = int(cfg['cur_max'])*10 ,limit5 = cfg['tem_min'] , limit6 = cfg['tem_max'],limit7 = cfg['hum_min'] , limit8 = cfg['hum_max'] ,limit9 = int(cfg['output_min'])*10 , limit10 = int(cfg['output_crmin'])*10 , limit11 = int(cfg['output_crmax'])*10 , limit12 = int(cfg['output_max'])*10 , limit13 = int(cfg['cur_crmin'])*10 , limit14 = int(cfg['cur_crmax'])*10)
        self.execJs(jsSheet)
        time.sleep(0.25)
        
    def checkCorrectHtml(self):
        cfg = self.cfgs
       
        status , message = self.check( 'type' , cfg['series'] , '系列')
        self.sendtoMainapp(message)
        
        status , message = self.check( 'language' , cfg['language'] , '中英文')
        self.sendtoMainapp(message)
        if (len(cfg['mac']) > 5  ):
            status , message = self.macAddrCheck( 'mac1' , cfg['mac'] , 'mac地址')
            self.sendtoMainapp(message)
        
        self.driver.back()
        
        
        
    def checkTitleBar2(self):
        cfg = self.cfgs
        self.divClick(2)
        time.sleep(0.35)
        self.driver.find_element_by_id("titlebar2").click()
        time.sleep(0.35)
        
        line , loop = 3 , 2
        list=[]
        cfgStr = []
        outputStr = []
        for i in range(1 , 1+1):
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
        list.clear()
        cfgStr.clear()
        outputStr.clear()
        
        for i in range(1 , line+1):
            list.append('Tvmin{0}'.format(i))
            list.append('Tvmax{0}'.format(i))
            cfgStr.append('vol_min')
            cfgStr.append('vol_max')
            outputStr.append('L{0}总电压最小值'.format(i))
            outputStr.append('L{0}总电压最大值'.format(i))
        self.checkAndSendTitleBar3(list , cfgStr , outputStr , 2)
        list.clear()
        cfgStr.clear()
        outputStr.clear()
        
        for i in range(1 , 2+1):
            list.append('Temmin{0}'.format(i))
            list.append('Temmax{0}'.format(i))
            cfgStr.append('tem_min')
            cfgStr.append('tem_max')
            outputStr.append('温度{0}最小值'.format(i))
            outputStr.append('温度{0}最大值'.format(i))
            
        self.checkAndSendTitleBar3(list , cfgStr , outputStr , 3)
        list.clear()
        cfgStr.clear()
        outputStr.clear()
        
        for i in range(1 , 2+1):
            list.append('Hummin{0}'.format(i))
            list.append('Hummax{0}'.format(i))
            cfgStr.append('hum_min')
            cfgStr.append('hum_max')
            outputStr.append('湿度{0}最小值'.format(i))
            outputStr.append('湿度{0}最大值'.format(i))
            
        self.checkAndSendTitleBar3(list , cfgStr , outputStr , 4)
        list.clear()
        cfgStr.clear()
        outputStr.clear()
    

    def checkAndSendTitleBar3(self , list , cfgStr , outputStr , case):
        cfg = self.cfgs
        zz = zip(list , cfgStr , outputStr)
        statusList = []
        messageList = []
        for x,y,z in zz:
            #Tvmin = self.driver.find_element_by_id(x).get_attribute('value')
            status , message = self.checkStr( x , cfg[y] , z)
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
                self.sendtoMainapp("设置总电流最小值成功;1" )
                self.sendtoMainapp("设置总电流下临界值成功;1" )
                self.sendtoMainapp("设置总电流上临界值成功;1" )
                self.sendtoMainapp("设置总电流最大值成功;1" )
            elif( case == 2):
                self.sendtoMainapp("设置总电压最小值成功;1" )
                self.sendtoMainapp("设置总电压最大值成功;1" )
            elif( case == 3):
                self.sendtoMainapp("设置温度最小值成功;1" )
                self.sendtoMainapp("设置温度最大值成功;1" )
            elif( case == 4):
                self.sendtoMainapp("设置湿度最小值成功;1" )
                self.sendtoMainapp("设置湿度最大值成功;1" )
        statusList.clear()
        messageList.clear()
            
    def checkTitleBar3(self , opLists):
        cfg = self.cfgs
        self.divClick(2)
        time.sleep(0.35)
        self.driver.find_element_by_id("titlebar3").click()
        time.sleep(0.35)
        
        op = 24
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
                            if( int(cfg['series']) == 3 or int(cfg['series']) == 4):
                                totalms = 1
                            else:
                                totalms = 0
                            jsSheet = 'xmlset = createXmlRequest();xmlset.onreadystatechange = setdata;ajaxget(xmlset, \"/setunitlimit?a=\" + {action} + \"&b=\" + {min} + \"&c=\" + {xmin} + \"&d=\" + {xmax}+ \"&e=\" + {max}+ \"&f=\" + {ms} +  \"&\");'.format( action = i , min = opLists[j][2]*10 , xmin = opLists[j][3]*10 , xmax = opLists[j][4]*10 , max = opLists[j][5]*10 , ms = totalms)
                            self.execJs(jsSheet)
                            time.sleep(0.25)
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
                self.sendtoMainapp("设置输出位电流最小值成功;1" )
                self.sendtoMainapp("设置输出位电流下临界值成功;1" )
                self.sendtoMainapp("设置输出位电流上临界值成功;1" )
                self.sendtoMainapp("设置输出位电流最大值成功;1" )
        if( int(cfg['series']) == 3 or int(cfg['series']) == 4):#延时
            try:
                message =''
                self.driver.find_element_by_id('totalms')
            except NoSuchElementException:
                message =  '网页上找不到{0}ID;'.format('延时上电')
                self.sock.sendto(message.encode('utf-8') , (self.ip , self.port))
                return
            self.setItById('totalms', 1 , '上电延时')
            jsSheet = 'var ms = parseFloat(document.getElementById(\"totalms\").value);var xmlset = createXmlRequest();xmlset.onreadystatechange = setdata;ajaxget(xmlset, \"/settime?a=\" + ms + \"&\");'
            self.execJs(jsSheet)
            time.sleep(0.35)
            self.checkDelayTime(op)
            
    def checkDelayTime(self , op):
        statusList = []
        messageList = []
        for i in range(1 , int(op)+1):
            ms = 'ms{0}'.format(i)
            status , message = self.checkStr( ms , '1' , '上下电延时')
            statusList.append(status)
            messageList.append(message)
            
        msStr = zip(statusList , messageList)
        flag = False
        for x,y in msStr:
            if( x==0 or x==2):
                self.sendtoMainapp(y)
                flag = True
        if( flag == False):
            self.sendtoMainapp("设置上下电延时成功;1" )
            
    def checkEnergy(self):
        cfg = self.cfgs
        statusList = []
        messageList = []
        line  = 3 
        
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
        time.sleep(0.5)
        self.driver.find_element_by_id("titlebar4").click()
        time.sleep(0.5)
        
        jsSheet = 'var claerset = createXmlRequest();claerset.onreadystatechange = clearrec;ajaxget(claerset, \"/setenergy?a=\" + {0}+\"&\");'
        for i in range(1 , 4):
            self.execJs(jsSheet.format(i))
            time.sleep(1)
        time.sleep(1)
        self.driver.find_element_by_id("titlebar4").click()
        time.sleep(1)
        self.checkEnergy()
        
    def setTime(self):
        self.divClick(4)
        time.sleep(0.35)
        self.driver.find_element_by_id("biao6").click()
        time.sleep(0.35)
        jsSheet = 'var b = loctime.innerHTML;var g = parseInt(b.substr(8, 2), 10);var f = parseInt(b.substr(3, 2), 10);var a = parseInt(b.substr(0, 2), 10);var d = parseInt(b.substr(11, 2), 10);var e = parseInt(b.substr(14, 2), 10);var c = parseInt(b.substr(17, 2), 10);if (g.length < 2) {g = \"0\" + g}if (f.length < 2) {f = \"0\" + f}if (a.length < 2) {a = \"0\" + a}if (d.length < 2) {d = \"0\" + d}if (e.length < 2) {e = \"0\" + e}if (c.length < 2) {c = \"0\" + c}var xmlset = createXmlRequest();xmlset.onreadystatechange = setdata;ajaxget(xmlset, \"/setdtime?a=\" + g + \"&b=\" + f + \"&c=\" + a + \"&d=\" + d + \"&e=\" + e + \"&f=\" + c + \"&\")'
        self.execJs(jsSheet)
        time.sleep(0.25)
        self.sendtoMainapp("设置时间成功;1" )
    
    def opThreshold(self):
        cfg = self.cfgs
        minList , maxList , enList , idList , crminList , crmaxList = [],[],[],[],[],[]
        minStr , maxStr , enStr , idStr , crminStr , crmaxStr = 'op_{0}_min','op_{0}_max','op_{0}_en','op_{0}_id','op_{0}_crmin','op_{0}_crmax'
        
        for i in range(1,7):
            minList.append(minStr.format(i))
            maxList.append(maxStr.format(i))
            enList.append(enStr.format(i))
            idList.append(idStr.format(i))
            crminList.append(crminStr.format(i))
            crmaxList.append(crmaxStr.format(i))
            
        lists =[[]for i in range(6)]
        zz = zip(minList , maxList , enList , idList , crminList , crmaxList)
        index = 0
        for min , max , en , id , crmin , crmax in zz:
            if(int(cfg[id]) != 0 and int(cfg[en]) == 1):
                lists[index].append(int(cfg[id]))
                lists[index].append(int(cfg[en]))
                lists[index].append(int(cfg[min]))
                lists[index].append(int(cfg[crmin]))
                lists[index].append(int(cfg[crmax]))
                lists[index].append(int(cfg[max]))
                index += 1
        return lists
            