/*
 *
 *  Created on: 2021年1月1日
 *      Author: Lzy
 */
#include "home_mpduwid.h"
#include "ui_home_mpduwid.h"

Home_MpduWid::Home_MpduWid(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Home_MpduWid)
{
    ui->setupUi(this);
    set_background_icon(this,":/image/back.jpg");
    QTimer::singleShot(15,this,SLOT(initFunSlot()));
}

Home_MpduWid::~Home_MpduWid()
{
    delete ui;
}

void Home_MpduWid::initFunSlot()
{
    this->setEnabled(false);
    mItem = Cfg::bulid()->item;
    mObj = Dev_Mpdu::bulid(this);
    mDev = mObj->getDev();
    initWid();
}

void Home_MpduWid::initWid()
{
    QString str = tr("MPDU后台参数");
    mParamWid = new Home_MpduParamWid(ui->tabWidget);
    ui->tabWidget->addTab(mParamWid, str);
    connect(mParamWid, SIGNAL(indexHiddenSig(int)), this, SLOT(indexHiddenSlot(int)));
    connect(mParamWid, SIGNAL(sendVerSig(int)), this, SIGNAL(sendMpduVerSig(int)));

    str = tr("MPDU报警参数");
    mAlarmWid = new Home_MpduAlarmWid(ui->tabWidget);
    ui->tabWidget->addTab(mAlarmWid, str);
}

bool Home_MpduWid::inputCheck()
{
    QString str;
    bool ret = mParamWid->loopCheck();
    if(!ret) str += tr("每个回路输出位数量出错！\n");
    ret = mParamWid->outputCheck();
    if(!ret) str += tr("每块板输出位数量出错！\n");
    if(!str.isEmpty()) {
        MsgBox::critical(this, str);
        ret = false;
    }

    return ret;
}

bool Home_MpduWid::dataSave()
{
    bool ret = inputCheck();
    if(ret) {
        mParamWid->updateType();
        mAlarmWid->updateData();
    }

    return ret;
}

void Home_MpduWid::enabledSlot(bool en)
{
    if(mItem->modeId != MPDU) return;

    this->setEnabled(en);
    if(!en) {
        en = dataSave();
        if(en) {
            mObj->save();
        } else {
            emit errSig();
        }
    }
}

void Home_MpduWid::indexHiddenSlot(int index)
{
    if(1 == index)
        ui->tabWidget->removeTab(1);
    else
        ui->tabWidget->addTab( mAlarmWid ,tr("MPDU报警参数"));
}

void Home_MpduWid::savePopupSlot(bool en)
{
    if(mItem->modeId != MPDU) return;
    mObj->savePopup(en);
}
