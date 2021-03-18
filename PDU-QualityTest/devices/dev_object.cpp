/*
 *
 *  Created on: 2021年1月1日
 *      Author: Lzy
 */
#include "dev_object.h"

Dev_Object::Dev_Object(QObject *parent) : QThread(parent)
{
    QTimer::singleShot(150,this,SLOT(initFunSlot()));
    mPacket = sDataPacket::bulid();
    mItem = Cfg::bulid()->item;
    mPro = mPacket->getPro();

    mDev = nullptr;
    mDt = nullptr;
}

void Dev_Object::initFunSlot()
{
    mModbus = Rtu_Modbus::bulid(this)->get();
    if(!mModbus) QTimer::singleShot(150,this,SLOT(initFunSlot()));
}

void Dev_Object::initUnit(const QString& prefix, sUnitCfg &unit, int f)
{
    unit.min = read(prefix+"_min", 0).toFloat();
    unit.max = read(prefix+"_max", 10).toFloat();

    switch (f) {
    case 2:
        unit.en = read(prefix+"_en", 0).toInt();
        unit.id = read(prefix+"_id", 0).toInt();
    case 1:
        unit.crMin = read(prefix+"_crmin", 0).toFloat();
        unit.crMax = read(prefix+"_crmax", 10).toFloat();
        break;
    }
}

void Dev_Object::writeUnit(const QString& prefix, sUnitCfg &unit, int f)
{
    write(prefix+"_min", QString::number(unit.min));
    write(prefix+"_max", QString::number(unit.max));

    switch (f) {
    case 2:
        write(prefix+"_en", unit.en);
        write(prefix+"_id", unit.id);
    case 1:
        write(prefix+"_crmin", QString::number(unit.crMin));
        write(prefix+"_crmax", QString::number(unit.crMax));
        break;
    }
}


void Dev_Object::write(const QString &key, const QVariant& v)
{
    Cfg::bulid()->write(key, v, cfgGroup());
}

QVariant Dev_Object::read(const QString &key, const QVariant &v)
{
    return Cfg::bulid()->read(key, v, cfgGroup());
}


uchar *Dev_Object::toInt(uchar *ptr, int line, uint *value)
{
    for(int i=0; i<line; ++i) {
        value[i] =  (*ptr) * 256 + *(ptr+1);  ptr += 2; // 读取电能高8位
        value[i] <<= 16; // 左移8位
        value[i] +=  (*ptr) * 256 + *(ptr+1);  ptr += 2; // 读取电能底8位
    }

    return ptr;
}

uchar *Dev_Object::toOutputEle(uchar *ptr, int line, uint *value)
{
    for(int i=0; i<line; ++i) {
        value[i] = (*ptr++) << 16;
        value[i] += (*ptr++) << 8;
        value[i] += *ptr++;
    }

    return ptr;
}

uchar *Dev_Object::toShort(uchar *ptr, int line, ushort *value)
{
    for(int i=0; i<line; ++i) {
        value[i] =  (*ptr) * 256 + *(ptr+1);  ptr += 2;
    }

    return ptr;
}

uchar *Dev_Object::toChar(uchar *ptr, int line, uchar *value)
{
    for(int i=0; i<line; ++i) {
        value[i] = *(ptr++); // 读取电压
    }

    return ptr;
}

uchar *Dev_Object::toThreshold(uchar *ptr, int line, sDataUnit &unit)
{
    for(int i=0; i<line; ++i) {
        ptr = toShort(ptr, 1, &unit.min[i]);
        ptr = toShort(ptr, 1, &unit.max[i]);
    }

    return ptr;
}

uchar *Dev_Object::toEnvTh(uchar *ptr, sDataUnit &unit)
{
    unit.max[0] = *ptr++;
    unit.min[0] = *ptr++;
    return ptr;
}

ushort Dev_Object::getShort(uchar *ptr)
{
    return  (*ptr) * 256 + *(ptr+1);
}

uchar *Dev_Object::getShort(uchar *ptr, int line, uchar *value)
{
    for(int i=0; i<line; ++i) {
        value[i] = getShort(ptr); ptr += 2;
    }

    return  ptr;
}
