/*
 *
 *  Created on: 2021年1月1日
 *      Author: Lzy
 */
#include "test_object.h"

Test_Object::Test_Object(QObject *parent) : QThread(parent)
{
    isRun = false;
    mPacket = sDataPacket::bulid();
    mItem = Cfg::bulid()->item;
    mPro = mPacket->getPro();
    mObj = Dev_Mpdu::bulid(this);
    mDev = mObj->getDev();
    mDt = &(mDev->dt);
    QTimer::singleShot(500,this,SLOT(initFunSlot()));
}

Test_Object::~Test_Object()
{
    isRun = false;
    wait();
}

void Test_Object::updateDev()
{
    switch (mItem->modeId) {
    case MPDU: mObj = Dev_Mpdu::bulid(this); break;
    }

    if(mObj != NULL) {
        mDev = mObj->getDev();
        mDt = &(mDev->dt);
    }
}
