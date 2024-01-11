/*
 *
 *  Created on: 2021年1月1日
 *      Author: Lzy
 */
#include "test_corethread.h"

Test_CoreThread::Test_CoreThread(QObject *parent) : Test_Object(parent)
{

}

void Test_CoreThread::initFunSlot()
{
    mLogs = Test_Logs::bulid(this);
    mRead = Test_NetWork::bulid(this);
    mSn = Sn_SerialNum::bulid(this);
    mProcess = new QProcess(this);
    connect(mRead , SIGNAL(sendVersionSig(QString)) , this , SLOT(getVersionSlot(QString)));
    connect(mRead , SIGNAL(sendMACSig(QString)) , this , SLOT(getMacSlot(QString)));
}
void Test_CoreThread::getVersionSlot(QString str)
{
    if( str.size() != 0 ){ 
        if(mItem->modeId == 1){//zpdu
            QString str1;
            str1 = str.right(str.size()-(str.lastIndexOf(":")+1));
            int index = str1.indexOf("."); // 查找目标字符的索引
            if (index != -1){
                this->mVersion = str1.mid(0, index).trimmed(); // 截取从开头到目标字符之间的子字符串（包括目标字符）
                    mPro->softwareVersion = this->mVersion;
            }
        }
        if(mItem->modeId == 0){//mpdu
            this->mVersion = str.right(str.size()-(str.lastIndexOf(":")+1));
            mPro->softwareVersion = this->mVersion;
        }
    }
}
void Test_CoreThread::getMacSlot(QString str)
{
    if( str.size() >= 17 ){
        this->mMacStr = str.right(17);
        mPro->macAddress = this->mMacStr;
        qDebug()<<"mPro->macAddress     "<<mPro->macAddress;
    }
}
bool Test_CoreThread::checkNet()
{
    QString str = tr("检测设备网络");
    bool ret = cm_pingNet("192.168.1.163");
    if(ret) str += tr("正常");
    else{
        str += tr("错误");
        mPro->result = Test_Fail;
    }

    return mLogs->updatePro(str, ret);
}



bool Test_CoreThread::startProcess()
{
    QString exe = "pyweb_quality_";
    switch (mItem->modeId) {
    case MPDU:  exe += "mpdu"; break;
    case ZPDU:  exe += "zpdu"; break;
    }

    exe += ".exe";
    bool ret = checkNet();
    if(ret){
        mProcess->close();
        mProcess->start(exe);
        ret = mProcess->waitForFinished(420*1000); //mProcess->execute(exe);
        mLogs->updatePro(tr("网页检查功能退出"), ret , 1);
    }

    return ret;
}


void Test_CoreThread::workResult(bool res)
{
    QString str = tr("最终结果");
    if(mPro->result != Test_Fail) {
        res = true;
        str += tr("通过");
        mPro->uploadPassResult = 1;
    } else {
        res = false;
        str += tr("失败");
        mPro->uploadPassResult = 0;
    }

    mLogs->updatePro(str, res);
    mLogs->saveLogs();
    sleep(2);
    Json_Pack::bulid()->http_post("testdata/add","192.168.1.12");//全流程才发送记录(http)
    mPro->step = Test_Over;
}



void Test_CoreThread::workDown()
{
    bool ret = true;
    mItem->sn.clear();
    mLogs->updatePro(tr("质检已启动"));
    if(mItem->sn.isEmpty() &&mItem->enSn) ret = mSn->snEnter();
    if(ret) ret = startProcess();

    workResult(ret);
}

void Test_CoreThread::run()
{
    if(isRun) return;
    isRun = true;

    updateDev();
    workDown();
    isRun = false;
}
