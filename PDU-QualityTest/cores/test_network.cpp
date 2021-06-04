/*
 *
 *  Created on: 2021年1月1日
 *      Author: Lzy
 */
#include "test_network.h"

Test_NetWork::Test_NetWork(QObject *parent) : Test_Object(parent)
{

}

Test_NetWork *Test_NetWork::bulid(QObject *parent)
{
    static Test_NetWork* sington = nullptr;
    if(sington == nullptr)
        sington = new Test_NetWork(parent);
    return sington;
}

void Test_NetWork::initFunSlot()
{    
    mLogs = Test_Logs::bulid(this);
    mUdp = new UdpRecvSocket(this);
    mUdp->initSocket(10086);
    this->start();
}

void Test_NetWork::workDown()
{
    QReadLocker locker(mUdp->getLock());
    UdpBaseData *res = mUdp->getData();
    if(res) {
        QStringList list = QString(res->datagram).split(";");
        if(list.size() == 2) {
            QString str = list.first();
            bool pass = list.last().toInt();
            mLogs->updatePro(str, pass, 0);
        } else {
            qDebug() <<"Test_NetWork workDown err" << list.size();
        }
        delete res;
    } else {
        msleep(1);
    }
}

void Test_NetWork::run()
{
    isRun = true;
    while (isRun) {
        workDown();
    }
}
