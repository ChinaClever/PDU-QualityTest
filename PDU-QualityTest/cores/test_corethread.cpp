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
        ret = mProcess->waitForFinished(120*1000);
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
    } else {
        res = false;
        str += tr("失败");
    }

    mLogs->updatePro(str, res);
    mLogs->saveLogs();
    mPro->step = Test_Over;
}



void Test_CoreThread::workDown()
{
    bool ret = true;
    mItem->sn.clear();
    mLogs->updatePro(tr("质检已启动"));
    if(mItem->enSn) ret = mSn->snEnter();
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
