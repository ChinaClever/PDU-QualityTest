#include "sn_object.h"

Sn_Object::Sn_Object(QObject *parent) : QThread(parent)
{
    QTimer::singleShot(850,this,SLOT(initFunSlot()));
    mPacket = sDataPacket::bulid();
    mItem = Cfg::bulid()->item;
    mPro = mPacket->getPro();

    mDev = mPacket->getMpdu();
    mDt =  &(mDev->dt);
}

void Sn_Object::initFunSlot()
{
    mModbus = Rtu_Modbus::bulid(this)->get();
    if(!mModbus) QTimer::singleShot(150,this,SLOT(initFunSlot()));
}

void Sn_Object::initDev()
{
    switch (mItem->modeId) {
    case MPDU: mDev = mPacket->getMpdu(); break;
    case ZPDU: mDev = mPacket->getZpdu(); break;
    }

    if(mDev) mDt = &(mDev->dt);
}
