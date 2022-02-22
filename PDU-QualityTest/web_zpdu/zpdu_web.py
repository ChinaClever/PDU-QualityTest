from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import WebDriverException
import configparser
import time
import os

class ZpduWeb:

    def __init__(self):
        self.ip_prefix = "https://"
        self.initCfg()
        self.initDriver()

    def initDriver(self):
        try:
            self.driver = webdriver.Firefox(executable_path="geckodriver.exe")
        except ValueError:
            self.driver = webdriver.Chrome(executable_path="chromedriver.exe")

    @staticmethod
    def getCfg():
        cf = configparser.ConfigParser()
        fn = os.path.expanduser('~') + "/.PDU-QualityTest/cfg.ini"
        cf.read(fn, 'utf-8-sig')  # 读取配置文件，如果写文件的绝对路径，就可以不用os模块
        return cf

    def initCfg(self):
        
        self.cfgs = {'ip_prefix':'https://','versions':'','user': 'admin', 'password': 'admin123','ip_addr': '192.168.1.163', 'debug_web':  'correct.html','lines':1,'loops':1,'outputs':24,'standar':0,'series':4,'language':0,'breaker':1,'modbus':1,'vol_min':80,'vol_max':276,'cur_min':0,'cur_crmin':0,'cur_crmax':32,'cur_max':32,'tem_min':0,'tem_max':40,'hum_min':0,'hum_max':99,'output_min':0,'output_crmin':0,'output_crmax':16,'output_max':16,'op_1_min':0,'op_1_max':10,'op_1_en':0,'op_1_id':0,'op_1_crmin':0,'op_1_crmax':10,'op_2_min':0,'op_2_max':10,'op_2_en':0,'op_2_id':0,'op_2_crmin':0,'op_2_crmax':10,'op_3_min':0,'op_3_max':10,'op_3_en':0,'op_3_id':0,'op_3_crmin':0,'op_3_crmax':10,'op_4_min':0,'op_4_max':10,'op_4_en':0,'op_4_id':0,'op_4_crmin':0,'op_4_crmax':10,'op_5_min':0,'op_5_max':10,'op_5_en':0,'op_5_id':0,'op_5_crmin':0,'op_5_crmax':10,'op_6_min':0,'op_6_max':10,'op_6_en':0,'op_6_id':0,'op_6_crmin':0,'op_6_crmax':10,'mpdu_ver':0,'boards':3,'level':0,'envbox':0,'loop_1':8,'loop_2':8,'loop_3':8,'loop_4':8,'loop_5':8,'loop_6':8, 'security':0,'popup':1,'ratedVol':230}
        items = ZpduWeb.getCfg().items("zCfg")  # 获取section名为Mysql-Database所对应的全部键值对
        #self.cfgs['mac'] = MpduWeb.getCfg().get("Mac", "mac")
        for it in items:
            self.cfgs[it[0]] = it[1]

    def login1(self):
        ip =  self.cfgs['ip_prefix'] +self.cfgs['ip_addr']
        try:
            self.driver.get(ip)
        except WebDriverException:
            return 0,'输入IP错误;0'
        
        self.login(self.cfgs['user'] , 'admin')
        win = self.driver.switch_to_alert()
        print(win.text)
        if( '错误' in win.text or 'error' in win.text):
            win.accept()
            return 1,'账号和密码错误;1'
        time.sleep(3)
        win.send_keys(self.cfgs['password'])
        win.accept()
        time.sleep(3)
        win = self.driver.switch_to_alert()
        win.send_keys(self.cfgs['password'])
        win.accept()
        self.driver.refresh()
        time.sleep(3)
        return 1,'输入IP正确;1'
        
    def login2(self):
        ip =  self.cfgs['ip_prefix'] +self.cfgs['ip_addr']
        try:
            self.driver.get(ip)
        except WebDriverException:
            return 0,'输入IP错误;0'
        self.login(self.cfgs['user'] , self.cfgs['password'])
        try:
            win = self.driver.switch_to_alert()
            print(win.text)
            if( '错误' in win.text or 'error' in win.text ):
                time.sleep(1)
                win.accept()
                return 0,'再次输入账号和密码错误;0'
        except:
            time.sleep(2)
            return 1,'输入IP正确;1'
    
    def login(self , user , password ):    
        self.setItById('name', user , '账号')
        self.setItById('psd', password  , '密码')
        self.execJs('login()')
        
        
    def setEle(self):
        self.divClick(3)
        jsSheet = " claerset = createXmlRequest();claerset.onreadystatechange = clearrec;ajaxget(claerset, \"/energyzero?a=\" + {0}+\"&\");"        
        for num in range(0, 4):
            self.execJs(jsSheet.format(num))

    def setSelect(self, id, v):
        it = self.driver.find_element_by_id(id)
        Select(it).select_by_index(v)
        time.sleep(0.5)

    def setItById(self, id, v, parameter):
        try:
            time.sleep(0.1)
            it = self.driver.find_element_by_id(id)
        except NoSuchElementException:
            msg = '网页上找不到{0}'.format(id)
            #self.sendtoMainapp(msg, 0)
            return False
        else:
            if it.is_displayed():
                it.clear()
                it.send_keys(str(v))
                msg = '检查{0} {1}：{2};{3}'.format(parameter, id, v , 1)
                if('输出位开关延时' not in msg):
                    self.sendtoMainapp(msg)
            return True

    def btnClick(self, id):
        self.driver.find_element_by_id(id).click()
        time.sleep(0.5)

    def alertClick(self, id):
        self.btnClick(id)
        self.driver.switch_to.alert.accept()
        time.sleep(0.35)

    def divClick(self, id):
        self.driver.switch_to.default_content()
        self.execJs("clk({0})".format(id))
        self.driver.switch_to.frame('rightMain')

    def execJs(self, js):
        self.driver.execute_script(js)
        time.sleep(0.5)

    def execJsAlert(self, js):
        self.execJs(js)
        self.driver.switch_to.alert.accept()
        time.sleep(0.5)
    
    def setSelect(self, id, v):
        it = self.driver.find_element_by_id(id)
        if it.is_displayed():
            Select(it).select_by_index(v)
            time.sleep(1)
    
    def resetFactory(self):
        jsSheet = "var xmlset = createXmlRequest();xmlset.onreadystatechange = setdata;ajaxget(xmlset, \"/setsys?a=\" + 1 + \"&\");"
        if( int(self.cfgs['mpdu_ver']) == 2 and int(self.cfgs['versions']) == 16 ):
                jsSheet = 'var setUrl = Encryption(\"/setsys\");var xmlset = createXmlRequest();xmlset.onreadystatechange = setdata;ajaxget(xmlset, setUrl +\"?a=\" + 1 + \"&\");'
        self.divClick(7)
        if( int(self.cfgs['mpdu_ver']) == 2 and int(self.cfgs['security']) == 1 ):
            time.sleep(2)
        time.sleep(1.35)
        self.driver.find_element_by_id('biao1').click()
        time.sleep(3.35)
        if( int(self.cfgs['mpdu_ver']) == 2 and int(self.cfgs['security']) == 1 ):
            time.sleep(2)
        self.setSelect('order',1);time.sleep(3)
        self.execJs(jsSheet); time.sleep(3)
        self.sendtoMainapp('设备Web出厂设置成功;1')
        
    def check(self, ssid , value , parameter):
        try:
            message =''
            self.driver.find_element_by_id(ssid)
        except NoSuchElementException:
            message =  '网页上找不到{0}ID;'.format(parameter)+str(2)
            #sock.sendto(message.encode('utf-8-sig') , (dest_ip , dest_port))
            return 2,message
        v = self.driver.find_element_by_id(ssid).get_attribute('value')
        ret = 1
        if( value != self.driver.find_element_by_id(ssid).get_attribute('value') ):
            message = '检查{0}失败，实际值{1}，期待值{2};'.format(parameter,v,value)+str(0)
            ret = 0
        else:
            message ='检查{0}成功{1};'.format(parameter,value)+str(1)
        #sock.sendto(message.encode('utf-8-sig') , (dest_ip , dest_port))
        return ret,message
            
    def checkStr(self, ssid , value , parameter):
        try:
            message =''
            self.driver.find_element_by_id(ssid)
        except NoSuchElementException:
            message =  '网页上找不到{0}ID;'.format(parameter)+str(2)
            #sock.sendto(message.encode('utf-8-sig') , (dest_ip , dest_port))
            return 2,message
        v = self.driver.find_element_by_id(ssid).get_attribute('value')
        if ( isinstance(v,int)):
            v = str(v)
        ret = 1
        if('.' in v):
            v , v1= v.split('.')
        
        if( value == v ):
            message ='检查{0}成功{1};'.format(parameter,value)+str(1)
        else:
            message = '检查{0}失败，实际值{1}，期待值{2};'.format(parameter,v,value)+str(0)
            ret = 0
        #sock.sendto(message.encode('utf-8-sig') , (dest_ip , dest_port))
        return ret,message
        
    def checkSWStr(self, ssid , value , parameter):
        try:
            message =''
            self.driver.find_element_by_id(ssid)
        except NoSuchElementException:
            message =  '网页上找不到{0}ID;'.format(parameter)+str(2)
            #sock.sendto(message.encode('utf-8-sig') , (dest_ip , dest_port))
            return 2,message
        v = self.driver.find_element_by_id(ssid).text
        if ( isinstance(v,int)):
            v = str(v)
        ret = 1
        if( value == v ):
            message ='检查{0}成功{1};'.format(parameter,value)+str(1)
        else:
            message = '检查{0}失败，实际值{1}，期待值{2};'.format(parameter,v,value)+str(0)
            ret = 0
        #sock.sendto(message.encode('utf-8-sig') , (dest_ip , dest_port))
        return ret,message    
    
    def checkStr2(self, ssid , value , parameter):
        cfg = self.cfgs
        line = int(cfg['lines'])
        loop = int(cfg['loops'])
        try:
            message =''
            self.driver.find_element_by_id(ssid)
        except NoSuchElementException:
            message =  '网页上找不到{0}ID;'.format(parameter)+str(2)
            #sock.sendto(message.encode('utf-8-sig') , (dest_ip , dest_port))
            return 2,message
        webValueStr = self.driver.find_element_by_id(ssid).get_attribute('value')
        webValue = int(webValueStr)
        ret = 1
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
        if(  fileValue == webValue ):
            message ='检查{0}成功{1};'.format(parameter,fileValue)+str(1)
        else:
            message = '检查{0}失败，实际值{1}，期待值{2};'.format(parameter,webValue,fileValue)+str(0)
            ret = 0
        #sock.sendto(message.encode('utf-8-sig') , (dest_ip , dest_port))
        return ret,message
        
    def checkTemAndHum(self, ssid , parameter):
        
        try:
            message =''
            self.driver.find_element_by_id(ssid)
        except NoSuchElementException:
            message =  '网页上找不到{0}ID;'.format(parameter)+str(2)
            
            return 2,message
        webValueStr = self.driver.find_element_by_id(ssid).text
        #print(webValueStr)
        ret=1
        if(  webValueStr == 'NA' or webValueStr == '0'):
            message ='{0}当前值{1}不正确;'.format(parameter,webValueStr)+str(0)
            ret = 0
        else:
            message = '{0}当前值{1}正确;'.format(parameter,webValueStr)+str(1)
        return ret,message
        
    def sendtoMainapp(self, parameter):
        sock = self.sock
        dest_ip = self.ip
        dest_port = self.port
        message = parameter
        sock.sendto(message.encode('utf-8-sig') , (dest_ip , dest_port))
        
    def checkVersion(self):
        cfg = self.cfgs
        try:
            try:
                self.divClick(1)
                message = '登陆成功;1'
                self.sendtoMainapp(message)
                jsSheet = 'if(confirm("确认网页Logo是否正确")){alert("Logo正确");}else{alert("Logo错误");}'
                self.execJs(jsSheet)
                time.sleep(1)
                while( True ):
                    alert = self.driver.switch_to_alert().text
                    if( alert == '确认网页Logo是否正确' ):
                        time.sleep(1)
                    elif( alert == 'Logo正确' ):
                        self.sendtoMainapp('Logo正确;1')
                        break
                    elif( alert == 'Logo错误' ):
                        self.sendtoMainapp('Logo错误;0')
                        break
                self.driver.switch_to.alert.accept()
            except :
                print('exception')
            finally:
                time.sleep(5)
                tt = self.driver.find_element_by_xpath('//table[2]/tbody/tr[2]/td[2]')#1.5.7//table[2]/tbody/tr[2]/td[2]
                #1.5.8//table[2]/tbody/tr[1]/td[2]
                if( cfg['versions'] == '1.5.8' ):
                    tt = self.driver.find_element_by_xpath('//table[2]/tbody/tr[1]/td[2]')
                #print(tt.text)
                if( cfg['versions'] == ''):
                    return 2,'软件版本空;2'
                    
                if( cfg['versions'] in tt.text and len(str(cfg['versions'])) >= 2 ):
                    if( '.' in cfg['versions']):
                        cfg['versions'] = '55'
                    return 1,'软件版本正确;1'
                else:
                    return 0,'软件版本错误;0'
        except UnexpectedAlertPresentException:
            message = '登陆失败，账号密码错误;0'
            return 0,message
            
    def macAddrCheck(self , ssid  , parameter):
        cfg = self.cfgs
        try:
            message =''
            self.driver.find_element_by_id(ssid)
        except NoSuchElementException:
            message =  '网页上找不到{0}ID;'.format(parameter)+str(2)
            #sock.sendto(message.encode('utf-8-sig') , (dest_ip , dest_port))
            return 2,message
        v = self.driver.find_element_by_id(ssid).get_attribute('value')
        ret = 1
        if( '2C:26:5F:' in v ):
            message ='检查{0}成功{1};'.format(parameter,v)+str(1)
        else:
            message = '检查{0}失败，实际值{1};'.format(parameter,v)+str(1)
        #sock.sendto(message.encode('utf-8-sig') , (dest_ip , dest_port))
        return ret,message

    def setAlarmTcur(self):
        time.sleep(4)
       
        self.setItById('Tcmin1' , '1' ,'总电流最小值')
        self.setItById('Txcmin1' , '1' ,'总电流下限值')
        time.sleep(2)
        self.driver.find_element_by_id("save4").click()
        time.sleep(15)
        if( int(self.cfgs['popup']) == 1):
            try:
                #jsSheet = 'if(confirm("请检查ALM指示灯是否亮起、蜂鸣器是否蜂鸣、声光告警器是否亮起")){alert("是");}else{alert("否");}'
                #self.execJs(jsSheet)
                #print(alert)
                time.sleep(3)
                #while( True ):
                    #alert = self.driver.switch_to_alert().text
                #    if( alert == '请检查ALM指示灯是否亮起、蜂鸣器是否蜂鸣、声光告警器是否亮起' ):
                #        time.sleep(2)
                #    elif( alert == '是' ):
                #        self.sendtoMainapp('ALM指示灯已亮起、蜂鸣器已蜂鸣、声光告警器已亮起;1')
                #        break
                #    elif( alert == '否' ):
                #        self.sendtoMainapp('ALM指示灯未亮起、蜂鸣器未蜂鸣、声光告警器未亮起;0')
                #        break
                #    time.sleep(1)
                
                #self.driver.switch_to.alert.accept()
            except :
                print("exception")
            
        
    def setNormalTcur(self):
        time.sleep(4)
        
        self.setItById('Tcmin1' , '0' ,'总电流最小值')
        self.setItById('Txcmin1' , '0' ,'总电流下限值')
        time.sleep(2)
        self.driver.find_element_by_id("save4").click()
        time.sleep(2)
        if( int(self.cfgs['popup']) == 1):
            try:
                #jsSheet = 'if(confirm("请检查ALM指示灯是否灭、蜂鸣器是否蜂鸣停止、声光告警器是否灭")){alert("是");}else{alert("否");}'
                #self.execJs(jsSheet)
                time.sleep(3)
                #while( True ):
                #    alert = self.driver.switch_to_alert().text
                #    if( alert == '请检查ALM指示灯是否灭、蜂鸣器是否蜂鸣停止、声光告警器是否灭' ):
                #        time.sleep(2)
                #    elif( alert == '是' ):
                #        self.sendtoMainapp('ALM指示灯已灭、蜂鸣器已蜂鸣停止、声光告警器已灭;1')
                #        break
                #    elif( alert == '否' ):
                #        self.sendtoMainapp('ALM指示灯未灭、蜂鸣器未蜂鸣停止、声光告警器未灭;0')
                #        break
                #    time.sleep(1)
                
                #self.driver.switch_to.alert.accept()
            except :
                print("exception")

    def checkCalibrationLog(self):
        cfg = self.cfgs
        self.divClick(6)
        time.sleep(1)
        if( int(self.cfgs['security']) == 1 ):
            time.sleep(3)
        self.driver.find_element_by_id('biao2').click()
        time.sleep(3)
        tt = self.driver.find_element_by_id('evenlognum').text
        ss , page = tt.split(':')
        table = self.driver.find_element_by_id('tbalarmlog')
        trs = table.find_elements_by_tag_name('tr')
        v = int(cfg['mpdu_ver'])
        for tr in trs:
            tds = tr.find_elements_by_tag_name('td')
            for td in tds:
                if( v == 0 ):
                    if( '校准' in td.text or 'calibration' in td.text ):
                        message = '日志中存在自动校准记录;0'
                        self.sendtoMainapp(message)
                else:
                    if( '校准' in td.text or 'Local Time Correct' in td.text ):
                        message = '日志中存在自动校准记录;0'
                        self.sendtoMainapp(message)

