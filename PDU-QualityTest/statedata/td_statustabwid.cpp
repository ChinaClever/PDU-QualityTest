/*
 *
 *  Created on: 2021年1月1日
 *      Author: Lzy
 */
#include "td_statustabwid.h"

Td_StatusTabWid::Td_StatusTabWid(QWidget *parent) : ComTableWid(parent)
{
    initWid();
    mPro = sDataPacket::bulid()->getPro();
//    t = 0;
}


void Td_StatusTabWid::initWid()
{
    QStringList header;
    QString title = tr("质检数据列表");
    header << tr("时间") << tr("结果") << tr("质检项");
    initTableWid(header, 0, title);

    setColumnWidth(0, 160);
    setColumnWidth(1, 100);
    QGridLayout *gridLayout = new QGridLayout(this->parentWidget());
    gridLayout->setContentsMargins(0, 0, 0, 0);
    gridLayout->addWidget(this);
}


void Td_StatusTabWid::appendItem()
{
    QStringList listStr;
    listStr << mPro->time;
    bool pass = mPro->itPass.first();
    if(pass){
        listStr << "√";
    } else {
        listStr << "×";
    }

    listStr << mPro->item.first();
    insertRow(0, listStr);
    setAlignLeft(0, 2);

    if(!pass) setAlarmBackgroundColor(0);
    mPro->item.removeFirst();
    mPro->itPass.removeFirst();
}

void Td_StatusTabWid::timeoutDone()
{
//    if( t < 50 )
//    {
//        mPro->time = QTime::currentTime().toString("hh:mm:ss");
//        mPro->itPass<<"√";
//        mPro->item << "ttttttttt";
//        t++;
//    }
    while(mPro->item.size())
        appendItem();
}

void Td_StatusTabWid::startSlot()
{
    delTable();
}
