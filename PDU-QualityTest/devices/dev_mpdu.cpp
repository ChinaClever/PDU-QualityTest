/*
 *
 *  Created on: 2021年1月1日
 *      Author: Lzy
 */
#include "dev_mpdu.h"

Dev_Mpdu::Dev_Mpdu(QObject *parent) : Dev_Object(parent)
{
    mDev = mPacket->getMpdu();
    mDt = &(mDev->dt);
    initCfg();
}


Dev_Mpdu *Dev_Mpdu::bulid(QObject *parent)
{
    static Dev_Mpdu* sington = nullptr;
    if(sington == nullptr)
        sington = new Dev_Mpdu(parent);
    return sington;
}


void Dev_Mpdu::initType()
{
    sDevType *ptr = mDt;
    ptr->lines = read("lines", 1).toInt();
    ptr->loops = read("loops", 3).toInt();
    ptr->series = read("series", 4).toInt();
    ptr->breaker = read("breaker", 1).toInt();
    ptr->standar = read("standar", 0).toInt();
    ptr->outputs = read("outputs", 24).toInt();
    ptr->language = read("language", 1).toInt();
    ptr->versions = read("versions", "").toString();
    ptr->envbox = read("envbox", 0).toInt();
    ptr->modbus = read("modbus", 0).toInt();
    ptr->boards = read("boards", 3).toInt();
    ptr->level = read("level", 0).toInt();
    ptr->mpdu_ver = read("mpdu_ver", 2).toInt();
    ptr->security = read("security", 0).toInt();
    ptr->popup = read("popup" , 0).toInt();

    for(int i=0; i<6; ++i) ptr->loop[i] = read(QString("loop_%1").arg(i+1), 8).toInt();
    for(int i=0; i<3; ++i) ptr->board[i] = read(QString("board_%1").arg(i+1), 8).toInt();
}

void Dev_Mpdu::writeType()
{
    sDevType *ptr = mDt;
    write("lines", ptr->lines);
    write("loops", ptr->loops);
    write("series", ptr->series);
    write("breaker", ptr->breaker);
    write("standar", ptr->standar);
    write("outputs", ptr->outputs);
    write("language", ptr->language);
    write("versions", ptr->versions);
    write("envbox", ptr->envbox);
    write("modbus", ptr->modbus);
    write("boards", ptr->boards);
    write("level", ptr->level);
    write("mpdu_ver", ptr->mpdu_ver);
    write("security", ptr->security);
    write("popup", ptr->popup);

    for(int i=0; i<6; ++i) write(QString("loop_%1").arg(i+1), ptr->loop[i]);
    for(int i=0; i<3; ++i) write(QString("board_%1").arg(i+1), ptr->board[i]);
}

void Dev_Mpdu::initData()
{
    sObjCfg *ptr = &(mDev->cfg);
    initUnit("vol", ptr->vol);
    initUnit("cur", ptr->cur, 1);

    initUnit("tem", ptr->tem);
    initUnit("hum", ptr->hum);
    initUnit("output", ptr->output, 1);

    for(int i=0; i<OpSize; ++i) {
        QString str = "op_" + QString::number(i+1);
        initUnit(str, ptr->opCur[i], 2);
    }
}

void Dev_Mpdu::writeData()
{
    sObjCfg *ptr = &(mDev->cfg);
    writeUnit("vol", ptr->vol);
    writeUnit("cur", ptr->cur, 1);

    writeUnit("tem", ptr->tem);
    writeUnit("hum", ptr->hum);
    writeUnit("output", ptr->output, 1);

    for(int i=0; i<OpSize; ++i) {
        QString str = "op_" + QString::number(i+1);
        writeUnit(str, ptr->opCur[i], 2);
    }
}

void Dev_Mpdu::initCfg()
{
    initType();
    initData();
}

void Dev_Mpdu::save()
{
    writeType();
    writeData();
}

void Dev_Mpdu::savePopup(bool en)
{
    sDevType *ptr = mDt;
    ptr->popup = en?1:0;
    write("popup", ptr->popup);
}
