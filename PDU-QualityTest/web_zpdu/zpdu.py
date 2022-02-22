from quality_zpdu.zpdu_web import  *
import datetime

class Zpdu(ZpduWeb):
       
    def start_fun(self , sock , dest_ip , dest_port):
        cfg = self.cfgs
        self.sock = sock
        self.ip = dest_ip
        self.port = dest_port
        intRet , message = 0 , ''
        if(cfg['ip_prefix'] == 'https://'):
            intRet , message = self.login1()
            self.sendtoMainapp(message)
            if(intRet == 0):
                return
        
        intRet , message = self.login2()
        self.sendtoMainapp(message)
        if( intRet == 0 ):
            return
        
        intRet , message = self.changetodebug()
        self.sendtoMainapp(message)
        if(intRet == 0):
            return
        
        self.checkdebughtml()
        time.sleep(0.5)
        
        self.getParameter(int(cfg['devzpdutype']))
        
        intRet , message = self.changetoset()
        self.sendtoMainapp(message)
        if(intRet == 0):
            return
        self.checksethtml()
        time.sleep(1)
        
        self.driver.back()
        self.driver.back()
        
        if(int(cfg['series']) == 3 or int(cfg['series']) == 4):
            self.setDelay()##
        self.checkOpValue()##
        self.checkSensorValue()
        self.clearEnergy()##
        self.checkEnergy()##
        if(int(cfg['series']) == 3 or int(cfg['series']) == 4):
            self.openOrCloseOp( False )##
            self.checkOp( False )##
            self.openOrCloseOp( True )##
            self.checkOp( True )##
        self.checkTime()
        self.resetfactory()
        
        #self.driver.find_elements_by_class_name('treeview')[1].click()
        #time.sleep(1)
        #self.driver.find_elements_by_class_name('menuItem')[6].click()
        #time.sleep(1)
        #self.driver.switch_to.frame('iframe2_d')
        #self.setItById('d0', 0 , '温度1最小值')
        #self.setItById('e0', 0  , '温度1下限值')
        #self.setItById('f0', 39  , '温度1上限值')
        #self.setItById('g0', 139  , '温度1最大值')
        #self.driver.find_element_by_id('h0').click()
        #self.execJs('setdata()')
        #time.sleep(5)

    def checkLanguage(self):
        cfg = self.cfgs
    try:
        flag = True
        it = self.driver.find_element_by_id('lang_4').text
        if( 'Name' in it ):
            flag = False
        if(int(cfg['language']) == 0 and flag == False):
            self.sendtoMainapp('检查语言失败(填写为中文，网页是英文);0')
        elif(int(cfg['language']) == 1 and flag == True):
            self.sendtoMainapp('检查语言失败(填写为y英文，网页是中文);0')
        else:
            self.sendtoMainapp('检查语言成功;1')
    except:
        print('检查语言错误')
    
    def getParameter(self , v ):
        #cfg['lines']cfg['loops']cfg['series']cfg['devzpdutype']
        cfg = self.cfgs
        if( (v >= 5 and v <= 8) or
            (v >= 13 and v <= 16) ):
            cfg['lines'] = 3
        else:
            cfg['lines'] = 1
            
        if( v >= 1 and v <= 4):
            cfg['loops'] = 2
        elif(v >= 5 and v <= 8):
            cfg['loops'] = 3
        elif(v >= 9 and v <= 12):
            cfg['loops'] = 4
        elif(v >= 13 and v <= 16):
            cfg['loops'] = 6
        else:
            cfg['loops'] = 1
            
        if( v%4 ):
            cfg['series'] = v%4
        else:
            cfg['series'] = 4
            
    def close(self):
        time.sleep(0.1)
        #print(datetime.datetime.now())
        self.driver.quit()
        #print(datetime.datetime.now())
        time.sleep(3)
        

    def changetodebug(self):
        cfg = self.cfgs
        ip = cfg['ip_prefix'] + cfg['ip_addr'] + '/debug.html'
        
        try:
            self.driver.get(ip)
        except:
            return 0,'账号密码错误;0'
        else:
            time.sleep(1)
            self.driver.switch_to.default_content()
            return 1,'账号密码正确;1'
    
    def changetoset(self):
        cfg = self.cfgs
        ip = cfg['ip_prefix'] + cfg['ip_addr'] + '/set.html'
        
        try:
            self.driver.get(ip)
        except:
            return 0,'set 页面不存在'
        else:
            time.sleep(1)
            self.driver.switch_to.default_content()
            return 1,'set 页面存在'
    
    def setCorrect1(self):
        cfg = self.cfgs
        time.sleep(2)
        if (len(cfg['mac']) > 5  ):#NoSuchElementException
            strMac =  cfg['mac']
        try:
            self.driver.find_element_by_id('mac')
        except NoSuchElementException:
            message = '无法找到MAC控件;0'
            self.sendtoMainapp(message)
            time.sleep(0.35)
            self.sendtoMainapp('MAC-1')
        v = self.driver.find_element_by_id('mac').get_attribute('value')
        if( '2C:26:5F:' not in v):
            v = strMac
            self.setItById('mac', cfg['mac'], 'Mac地址')
            time.sleep(3)
            self.execJs(cfg['setmaccontrolid'])
            time.sleep(1)
            #else:
            #    return 1
        else:
            self.sendtoMainapp('MAC-1')
        

    def checkId(self , id):
        try:
            it = self.driver.find_element_by_xpath(id)
        except NoSuchElementException:
            msg = '网页上找不到{0};1'.format(id)
            self.sendtoMainapp(msg)
            return 0
        else:
            return 1
    
    def checkCorrectHtml(self):
        cfg = self.cfgs
      
        if (len(cfg['mac']) > 5  ):
            status , message = self.macAddrCheck( 'mac' , cfg['mac'] , 'mac地址')
            self.sendtoMainapp(message)
        
        self.driver.back()
        
    def checkMacAddress(self):
        cfg = self.cfgs
        try:
            self.driver.find_element_by_id('mac')
        except NoSuchElementException:
            message = '检查MAC地址时，无法找到MAC控件;0'
            self.sendtoMainapp(message)
            time.sleep(0.35)
            return
        v = self.driver.find_element_by_id('mac').get_attribute('value')
        if( '2C:26:5F:' not in v):
            message = 'MAC设置失败%s;0'%v
            self.sendtoMainapp(message)
        else:
            message = 'MAC设置成功%s;1'%v
            self.sendtoMainapp(message)
    
    def checkdebughtml(self):
        cfg = self.cfgs
        time.sleep(2)
        self.checkMacAddress()
        status , message = self.check( 'bb' , cfg['level'] , '屏幕显示方向')
        self.sendtoMainapp(message)
        status , message = self.checkStr( 'cc' , cfg['devzpdutype'] , '设备类型')
        self.sendtoMainapp(message)
        strId = ''
        strCfgs = ''
        showMessage = ''
        for i in range(1,7):
            strId = 'C{0}'.format(i)
            strCfgs = 'loop_op{0}'.format(i)
            showMessage = 'C{0}回路输出位'.format(i)
            status , message = self.check( strId , cfg[strCfgs] , showMessage)
            self.sendtoMainapp(message)
        for i in range(1,7):
            strId = 'd{0}'.format(i)
            strCfgs = 'loop_smallloop{0}'.format(i)
            showMessage = 'C{0}回路小回路'.format(i)
            status , message = self.check( strId , cfg[strCfgs] , showMessage)
            self.sendtoMainapp(message)
        for i in range(1,4):
            strId = 'L{0}'.format(i)
            strCfgs = 'line_op{0}'.format(i)
            showMessage = 'L{0}相输出位'.format(i)
            status , message = self.check( strId , cfg[strCfgs] , showMessage)
            self.sendtoMainapp(message)
        status , message = self.check( 'ee' , cfg['standar'] , '版本类型')
        self.sendtoMainapp(message)
        
    def checksethtml(self):
        cfg = self.cfgs
        strId = ''
        strCfgs = ''
        showMessage = ''
        status , message = self.check( 'a1' , cfg['type'] , '型号')
        self.sendtoMainapp(message)
        status , message = self.check( 'a2' , cfg['hw_version'] , '硬件版本')
        self.sendtoMainapp(message)
        status , message = self.check( 'a3' , cfg['protocol_version'] , '通讯协议版本')
        self.sendtoMainapp(message)
        status , message = self.check( 'a4' , cfg['rated_voltage'] , '额定电压')
        self.sendtoMainapp(message)
        status , message = self.check( 'a5' , cfg['rated_current'] , '额定电流')
        self.sendtoMainapp(message)
        status , message = self.check( 'a6' , cfg['rated_frequency'] , '额定频率')
        self.sendtoMainapp(message)
        status , message = self.check( 'a7' , cfg['lines'] , '相位数')
        self.sendtoMainapp(message)
        status , message = self.check( 'a8' , cfg['breaker'] , '断路器类型')
        self.sendtoMainapp(message)
        
        list=[]
        cfgStr = []
        outputStr = []
        for i in range(1,49):
            strId = 'b{0}'.format(i)
            strCfgs = 'zpduopcur_{0}_max'.format(i)
            showMessage = '输出位{0}'.format(i)
            a = '0'
            if int(cfg[strCfgs]) == 16:
                a = '1'
            list.append(strId)
            cfgStr.append(a)
            outputStr.append(showMessage)
            #status , message = self.check( strId , a , showMessage)
            #self.sendtoMainapp(message)
        self.checkAndSendTitleBar3(list , cfgStr , outputStr , 1)
            
    def setDelay(self):
        cfg = self.cfgs
        try:
            self.driver.find_elements_by_class_name('treeview')[1].click()
            time.sleep(1)
            self.driver.find_elements_by_class_name('menuItem')[5].click()
            time.sleep(1)
            self.driver.switch_to.frame('iframe2_c')
            for i in range(0 , int(cfg['outputs'])):
                self.setItById('d{0}'.format(i), 1 , '输出位开关延时')
                it = self.driver.find_element_by_id('k{0}'.format(i))
                if not it.is_selected():
                    it.click()
            self.execJs('setdata()')
            for i in range(0 , int(cfg['outputs'])):
                str = 'k{0}'.format(i)
                it = self.driver.find_element_by_id(str)
                if it.is_selected():
                    it.click()
            self.execJs('setdata()')
            self.sendtoMainapp('设置输出位开关延时;1')            
        except:
            print('设置延时错误')
    
    def checkOpValue(self):
        cfg = self.cfgs
        try:
            self.driver.refresh()
            self.driver.find_elements_by_class_name('treeview')[1].click()
            time.sleep(1)
            self.driver.find_elements_by_class_name('menuItem')[5].click()
            time.sleep(1)
            self.driver.switch_to.frame('iframe2_c')
            list=[]
            cfgStr = []
            outputStr = []
            for i in range(0 , int(cfg['outputs'])):
                if(int(cfg['series']) == 3 or int(cfg['series']) == 4):
                    str = 'd{0}'.format(i)
                    list.append(str)
                    cfgStr.append('1')
                    outputStr.append('输出位{0}开关延时'.format(i+1))
                    
                if(int(cfg['series']) == 2 or int(cfg['series']) == 4):
                    str = 'e{0}'.format(i)
                    list.append(str)
                    cfgStr.append(cfg['zpduopcur_{0}_min'.format(i+1)])
                    outputStr.append('输出位{0}最小值'.format(i+1))
                    str = 'f{0}'.format(i)
                    list.append(str)
                    cfgStr.append(cfg['zpduopcur_{0}_crmin'.format(i+1)])
                    outputStr.append('输出位{0}下临值'.format(i+1))
                    str = 'g{0}'.format(i)
                    list.append(str)
                    cfgStr.append(cfg['zpduopcur_{0}_crmax'.format(i+1)])
                    outputStr.append('输出位{0}上临值'.format(i+1))
                    str = 'h{0}'.format(i)
                    list.append(str)
                    cfgStr.append(cfg['zpduopcur_{0}_max'.format(i+1)])
                    outputStr.append('输出位{0}最大值'.format(i+1))
            self.checkAndSendTitleBar3(list , cfgStr , outputStr , 2)    
        except:
            print('检查输出位阈值错误')
    
    def checkTem(self):
        cfg = self.cfgs
        try:
            list=[]
            cfgStr = []
            outputStr = []
            for i in range(0 , 2):
                list.append('d{0}'.format(i))
                cfgStr.append(cfg['tem_min'])
                outputStr.append('温度{0}最小值'.format(i+1))
                list.append('e{0}'.format(i))
                cfgStr.append(cfg['tem_crmin'])
                outputStr.append('温度{0}下临界值'.format(i+1))
                list.append('f{0}'.format(i))
                cfgStr.append(cfg['tem_crmax'])
                outputStr.append('温度{0}上临界值'.format(i+1))
                list.append('g{0}'.format(i))
                cfgStr.append(cfg['tem_max'])
                outputStr.append('温度{0}最大值'.format(i+1))
            self.checkAndSendTitleBar3(list , cfgStr , outputStr , 3)
        except:
            print('检查温度值错误')
    
    def checkHum(self):
        cfg = self.cfgs
        try:
            list=[]
            cfgStr = []
            outputStr = []
            for i in range(2 , 4):
                list.append('d{0}'.format(i))
                cfgStr.append(cfg['hum_min'])
                outputStr.append('湿度{0}最小值'.format(i-1))
                list.append('e{0}'.format(i))
                cfgStr.append(cfg['hum_crmin'])
                outputStr.append('湿度{0}下临界值'.format(i-1))
                list.append('f{0}'.format(i))
                cfgStr.append(cfg['hum_crmax'])
                outputStr.append('湿度{0}上临界值'.format(i-1))
                list.append('g{0}'.format(i))
                cfgStr.append(cfg['hum_max'])
                outputStr.append('湿度{0}最大值'.format(i-1))
            self.checkAndSendTitleBar3(list , cfgStr , outputStr , 4)
        except:
            print('检查湿度值错误')
    
    def checkLoopCur(self):
        cfg = self.cfgs
        try:
            list=[]
            cfgStr = []
            outputStr = []
            for i in range(4 , 4+int(cfg['loops'])):
                list.append('d{0}'.format(i))
                cfgStr.append(cfg['loopcur_min'])
                outputStr.append('C{0}电流最小值'.format(i-3))
                list.append('e{0}'.format(i))
                cfgStr.append(cfg['loopcur_crmin'])
                outputStr.append('C{0}电流下临界值'.format(i-3))
                list.append('f{0}'.format(i))
                cfgStr.append(cfg['loopcur_crmax'])
                outputStr.append('C{0}电流上临界值'.format(i-3))
                list.append('g{0}'.format(i))
                cfgStr.append(cfg['loopcur_max'])
                outputStr.append('C{0}电流最大值'.format(i-3))
            self.checkAndSendTitleBar3(list , cfgStr , outputStr , 5)
        except:
            print('检查回路电流值错误')
    
    def checkLineCur(self):
        cfg = self.cfgs
        try:
            list=[]
            cfgStr = []
            outputStr = []
            for i in range(10 , 10+int(cfg['lines'])):
                list.append('d{0}'.format(i))
                cfgStr.append(cfg['cur_min'])
                outputStr.append('L{0}电流最小值'.format(i-9))
                list.append('e{0}'.format(i))
                cfgStr.append(cfg['cur_crmin'])
                outputStr.append('L{0}电流下临界值'.format(i-9))
                list.append('f{0}'.format(i))
                cfgStr.append(cfg['cur_crmax'])
                outputStr.append('L{0}电流上临界值'.format(i-9))
                list.append('g{0}'.format(i))
                cfgStr.append(cfg['cur_max'])
                outputStr.append('L{0}电流最大值'.format(i-9))
            self.checkAndSendTitleBar3(list , cfgStr , outputStr , 6)
        except:
            print('检查相电流值错误')
    
    def checkLineVol(self):
        cfg = self.cfgs
        try:
            list=[]
            cfgStr = []
            outputStr = []
            for i in range(13 , 13+int(cfg['lines'])):
                list.append('d{0}'.format(i))
                cfgStr.append(cfg['vol_min'])
                outputStr.append('L{0}电压最小值'.format(i-9))
                list.append('e{0}'.format(i))
                cfgStr.append(cfg['vol_crmin'])
                outputStr.append('L{0}电压下临界值'.format(i-9))
                list.append('f{0}'.format(i))
                cfgStr.append(cfg['vol_crmax'])
                outputStr.append('L{0}电压上临界值'.format(i-9))
                list.append('g{0}'.format(i))
                cfgStr.append(cfg['vol_max'])
                outputStr.append('L{0}电压最大值'.format(i-9))
            self.checkAndSendTitleBar3(list , cfgStr , outputStr , 7)
        except:
            print('检查相电压值错误')
    
    def checkSensorValue(self):
        cfg = self.cfgs
        try:
            self.driver.refresh()
            self.driver.find_elements_by_class_name('treeview')[1].click()
            time.sleep(1)
            self.driver.find_elements_by_class_name('menuItem')[6].click()
            time.sleep(1)
            self.driver.switch_to.frame('iframe2_d')
            self.checkLanguage()
            self.checkTem()
            self.checkHum()
            self.checkLoopCur()
            self.checkLineCur()
            self.checkLineVol()
        except:
            print('检查相阈值错误')
    
    def clearEnergy(self):
        cfg = self.cfgs
        try:
            self.driver.refresh()
            self.driver.find_elements_by_class_name('treeview')[1].click()
            time.sleep(1)
            self.driver.find_elements_by_class_name('menuItem')[7].click()
            time.sleep(1)
            self.driver.switch_to.frame('iframe2_e')
            if(int(cfg['series']) == 2 or int(cfg['series']) == 4):
                for i in range(0 , int(cfg['outputs'])):
                    self.driver.find_element_by_id('d{0}'.format(i)).click()
            elif(int(cfg['series']) == 1 or int(cfg['series']) == 3):
                for i in range(50 , 50+int(cfg['loops'])):
                    self.driver.find_element_by_id('d{0}'.format(i)).click()
            self.driver.find_element_by_id('d56').click()
            self.sendtoMainapp('清理电能操作;1') 
        except:
            print('清理电能失败')
    
    def checkEnergy(self):
        cfg = self.cfgs
        try:
            self.driver.refresh()
            self.driver.find_elements_by_class_name('treeview')[1].click()
            time.sleep(1)
            self.driver.find_elements_by_class_name('menuItem')[7].click()
            time.sleep(1)
            self.driver.switch_to.frame('iframe2_e')
            list=[]
            cfgStr = []
            outputStr = []
            if(int(cfg['series']) == 2 or int(cfg['series']) == 4):
                for i in range(0 , int(cfg['outputs'])):
                    list.append('c{0}'.format(i))
                    cfgStr.append('0.0')
                    outputStr.append('输出位{0}电能清零'.format(i+1))
            elif(int(cfg['series']) == 1 or int(cfg['series']) == 3):
                for i in range(50 , 50+int(cfg['loops'])):
                    list.append('c{0}'.format(i))
                    cfgStr.append('0.00')
                    outputStr.append('C{0}电能清零'.format(i-49))
            self.checkAndSendTitleBar3(list , cfgStr , outputStr , 8)
        except:
            print('检查电能失败')
            
    def openOrCloseOp(self , flag):
        cfg = self.cfgs
        try:
            self.driver.refresh()
            self.driver.find_elements_by_class_name('treeview')[1].click()
            time.sleep(1)
            self.driver.find_elements_by_class_name('menuItem')[11].click()
            time.sleep(1)
            self.driver.switch_to.frame('iframe2_i')
            if( flag == True ):
                self.driver.find_element_by_id('e50').click()
            else:
                self.driver.find_element_by_id('f50').click()
            time.sleep(int(cfg['outputs'])+8)
        except:
            pass
            
    def checkOp(self , flag):
        cfg = self.cfgs
        try:
            self.driver.refresh()
            self.driver.find_elements_by_class_name('treeview')[1].click()#设备设置
            time.sleep(1)
            self.driver.find_elements_by_class_name('menuItem')[11].click()#开关
            time.sleep(1)
            self.driver.switch_to.frame('iframe2_i')
            list=[]
            cfgStr = []
            outputStr = []
            if( flag == True ):
                for i in range(0 , int(cfg['outputs'])):
                    list.append('c{0}'.format(i))
                    outputStr.append('输出位{0}开关'.format(i+1))
                    if( int(cfg['language']) == 0 ):
                        cfgStr.append('开')
                    else:
                        cfgStr.append('ON')
                self.checkAndSendTitleBar3(list , cfgStr , outputStr , 10)
            else:
                for i in range(0 , int(cfg['outputs'])):
                    list.append('c{0}'.format(i))
                    outputStr.append('输出位{0}开关'.format(i+1))
                    if( int(cfg['language']) == 0 ):
                        cfgStr.append('关')
                    else:
                        cfgStr.append('OFF')
                self.checkAndSendTitleBar3(list , cfgStr , outputStr , 9)
        except:
            print('检查输出位开关失败')
    
    def checkTime(self):
        try:
            self.driver.refresh()
            self.driver.find_elements_by_class_name('treeview')[2].click()#网络安全
            time.sleep(1)
            self.driver.find_elements_by_class_name('menuItem')[15].click()#ntp
            time.sleep(1)
            self.driver.switch_to.frame('iframe3_d')
            devTime = self.driver.find_element_by_id('localtime').text.split()
            nowTime = str(datetime.datetime.now()).split()
            if( nowTime[0] == devTime[0]):
                h1 , m1 , s1 = nowTime[1].split(':')
                t1 = int(h1)*3600 + int(m1)*60
                h2 , m2 = devTime[1].split(':')
                t2 = int(h2)*3600 + int(m2)*60
                if( abs( t1-t2 ) >= 10*60 ):
                    self.sendtoMainapp("检查时间时分秒失败;0" )
                    self.sendtoMainapp("%d;1"%t1 )
                    self.sendtoMainapp("%d;1"%t2 )
                else:
                    #print(abs(t1-t2))
                    self.sendtoMainapp("检查时间成功;1" )
                    self.sendtoMainapp("%d;1"%t1 )
                    self.sendtoMainapp("%d;1"%t2 )
            else:
                self.sendtoMainapp("检查时间年月日失败;0" )
        except:
            print("检查时间异常")
            
    def resetfactory(self):
        try:
            self.driver.refresh()
            self.driver.find_elements_by_class_name('treeview')[6].click()#系统工具
            time.sleep(1)
            self.driver.find_elements_by_class_name('menuItem')[38].click()#系统命令
            time.sleep(1)
            self.driver.switch_to.frame('iframe7_b')
            self.setSelect('ee',1)
            self.alertClick('lang_7')
        except:
            print("恢复出厂设置异常")
            
    def checkAndSendTitleBar3(self , list , cfgStr , outputStr , case):
        cfg = self.cfgs
        zz = zip(list , cfgStr , outputStr)
        statusList = []
        messageList = []
        if( case == 1 ):
            for x,y,z in zz:
                status , message = self.check( x , y , z)
                statusList.append(status)
                messageList.append(message)
        elif( case == 2 or case == 3 or case == 4 or case == 5 or case == 6 or case == 7 ):
            for x,y,z in zz:
                status , message = self.checkStr( x , y , z)
                statusList.append(status)
                messageList.append(message)
        elif( case > 7 ):
            for x,y,z in zz:
                status , message = self.checkSWStr( x , y , z)
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
                self.sendtoMainapp("检查set后台各输出位阈值成功;1" )
            elif( case == 2):
                if(int(cfg['series']) == 3 or int(cfg['series']) == 4):
                    self.sendtoMainapp("输出位开关延时成功;1" )
                if(int(cfg['series']) == 2 or int(cfg['series']) == 4):
                    self.sendtoMainapp("输出位最小值成功;1" )
                    self.sendtoMainapp("输出位下临界值成功;1" )
                    self.sendtoMainapp("输出位上临界值成功;1" )
                    self.sendtoMainapp("输出位最大值成功;1" )
            elif( case == 3):
                self.sendtoMainapp("检查温度最小值成功;1" )
                self.sendtoMainapp("检查温度下临界值成功;1" )
                self.sendtoMainapp("检查温度上临界值成功;1" )
                self.sendtoMainapp("检查温度最大值成功;1" )
            elif( case == 4):
                self.sendtoMainapp("检查湿度最小值成功;1" )
                self.sendtoMainapp("检查湿度下临界值成功;1" )
                self.sendtoMainapp("检查湿度上临界值成功;1" )
                self.sendtoMainapp("检查湿度最大值成功;1" )
            elif( case == 5):
                self.sendtoMainapp("检查回路电流最小值成功;1" )
                self.sendtoMainapp("检查回路电流下临界值成功;1" )
                self.sendtoMainapp("检查回路电流上临界值成功;1" )
                self.sendtoMainapp("检查回路电流最大值成功;1" )
            elif( case == 6):
                self.sendtoMainapp("检查相电流最小值成功;1" )
                self.sendtoMainapp("检查相电流下临界值成功;1" )
                self.sendtoMainapp("检查相电流上临界值成功;1" )
                self.sendtoMainapp("检查相电流最大值成功;1" )
            elif( case == 7):
                self.sendtoMainapp("检查相电压最小值成功;1" )
                self.sendtoMainapp("检查相电压下临界值成功;1" )
                self.sendtoMainapp("检查相电压上临界值成功;1" )
                self.sendtoMainapp("检查相电压最大值成功;1" )
            elif( case == 8):
                self.sendtoMainapp("检查清理电能成功;1" )
            elif( case == 9):
                self.sendtoMainapp("检查输出位关成功;1" )
            elif( case == 10):
                self.sendtoMainapp("检查输出位开成功;1" )
        statusList.clear()
        messageList.clear()