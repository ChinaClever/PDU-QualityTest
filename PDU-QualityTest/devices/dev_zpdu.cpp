#include "dev_zpdu.h"

Dev_Zpdu::Dev_Zpdu(QObject *parent) : Dev_Object(parent)
{
    mDev = mPacket->getZpdu();
    mDt = &(mDev->dt);
    initCfg();
}


Dev_Zpdu *Dev_Zpdu::bulid(QObject *parent)
{
    static Dev_Zpdu* sington = nullptr;
    if(sington == nullptr)
        sington = new Dev_Zpdu(parent);
    return sington;
}


void Dev_Zpdu::initSetHtml()
{
    sDevType *ptr = mDt;
    ptr->type = read("type", "ZZIF-130-2004").toString();
    ptr->hw_version = read("hw_version", "A").toString();
    ptr->protocol_version = read("protocol_version", "196608").toString();
    ptr->rated_voltage = read("rated_voltage", 0).toInt();
    ptr->rated_current = read("rated_current", 1).toInt();
    ptr->rated_frequency = read("rated_frequency", "50").toString();
    ptr->lines = read("lines", 3).toInt();
    ptr->breaker = read("breaker", 0).toInt();
}

void Dev_Zpdu::initDebugHtml()
{
    sDevType *ptr = mDt;ptr->standar = read("standar", 0).toInt();
    ptr->outputs = read("outputs", 24).toInt();
    ptr->language = read("language", 0).toInt();
    ptr->level = read("level", 0).toInt();
    ptr->zpdu_ver = read("zpdu_ver", 1).toInt();
    ptr->popup = read("popup" , 0).toInt();
    ptr->devZpduType = read("devzpdutype" , 16).toInt();

    for(int i=0; i<3; ++i) ptr->line_op[i] = read(QString("line_op%1").arg(i+1), 8).toInt();
    for(int i=0; i<6; ++i) ptr->loop_op[i] = read(QString("loop_op%1").arg(i+1), 4).toInt();
    for(int i=0; i<6; ++i) ptr->loop_smallloop[i] = read(QString("loop_smallloop%1").arg(i+1), 1).toInt();
}

void Dev_Zpdu::writeSetHtml()
{
    sDevType *ptr = mDt;
    write("type",ptr->type);
    write("hw_version",ptr->hw_version);
    write("protocol_version",ptr->protocol_version);
    write("rated_voltage",ptr->rated_voltage);
    write("rated_current",ptr->rated_current);
    write("rated_frequency",ptr->rated_frequency);
    write("lines", ptr->lines);
    write("breaker", ptr->breaker);
}

void Dev_Zpdu::writeDebugHtml()
{
    sDevType *ptr = mDt;
    write("standar", ptr->standar);
    write("outputs", ptr->outputs);
    write("language", ptr->language);
    write("level", ptr->level);
    write("zpdu_ver", ptr->zpdu_ver);
    write("devzpdutype", ptr->devZpduType);
    write("popup", ptr->popup);

    for(int i=0; i<3; ++i) write(QString("line_op%1").arg(i+1), ptr->line_op[i]);
    for(int i=0; i<6; ++i) write(QString("loop_op%1").arg(i+1), ptr->loop_op[i]);
    for(int i=0; i<6; ++i) write(QString("loop_smallloop%1").arg(i+1), ptr->loop_smallloop[i]);
}

void Dev_Zpdu::initUnitV(const QString& prefix, sUnitCfg &unit)
{
    unit.min = read(prefix+"_min", 50).toFloat();
    unit.max = read(prefix+"_max", 500).toFloat();
    unit.crMin = read(prefix+"_crmin", 50).toFloat();
    unit.crMax = read(prefix+"_crmax", 500).toFloat();
}

void Dev_Zpdu::initUnitC(const QString& prefix, sUnitCfg &unit ,int value)
{
    unit.min = read(prefix+"_min", 0).toFloat();
    unit.max = read(prefix+"_max", value).toFloat();
    unit.crMin = read(prefix+"_crmin", 0).toFloat();
    unit.crMax = read(prefix+"_crmax", value).toFloat();
}

void Dev_Zpdu::initUnitT(const QString& prefix, sUnitCfg &unit)
{
    unit.min = read(prefix+"_min", 0).toFloat();
    unit.max = read(prefix+"_max", 40).toFloat();
    unit.crMin = read(prefix+"_crmin", 0).toFloat();
    unit.crMax = read(prefix+"_crmax", 40).toFloat();
}

void Dev_Zpdu::initUnitH(const QString& prefix, sUnitCfg &unit)
{
    unit.min = read(prefix+"_min", 0).toFloat();
    unit.max = read(prefix+"_max", 100).toFloat();
    unit.crMin = read(prefix+"_crmin", 0).toFloat();
    unit.crMax = read(prefix+"_crmax", 100).toFloat();
}

void Dev_Zpdu::initData()
{
    sObjCfg *ptr = &(mDev->cfg);
    initUnitV("vol", ptr->vol);
    initUnitC("cur", ptr->cur , 32);
    initUnitC("loopcur", ptr->loopcur , 16);

    initUnitT("tem", ptr->tem);
    initUnitH("hum", ptr->hum);
    for(int i = 0 ; i < ZpduOpSize ; i++)
    {
        QString str = "zpduopcur_" + QString::number(i+1);
        initUnitC(str, ptr->zpduopCur[i] , 16);
    }
}

void Dev_Zpdu::writeData()
{
    sObjCfg *ptr = &(mDev->cfg);
    writeUnit("vol", ptr->vol, 1);
    writeUnit("cur", ptr->cur, 1);
    writeUnit("loopcur", ptr->loopcur, 1);

    writeUnit("tem", ptr->tem, 1);
    writeUnit("hum", ptr->hum, 1);

    for(int i=0; i<ZpduOpSize; ++i) {
        QString str = "zpduopcur_" + QString::number(i+1);
        writeUnit(str, ptr->zpduopCur[i], 1);
    }
}

void Dev_Zpdu::initCfg()
{
    initSetHtml();
    initDebugHtml();
    initData();
}

void Dev_Zpdu::save()
{
    writeSetHtml();
    writeDebugHtml();
    writeData();
}

void Dev_Zpdu::savePopup(bool en)
{
    sDevType *ptr = mDt;
    ptr->popup = en?1:0;
    write("popup", ptr->popup);
}
