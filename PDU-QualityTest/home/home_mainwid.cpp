/*
 *
 *  Created on: 2021年1月1日
 *      Author: Lzy
 */
#include "home_mainwid.h"
#include "ui_home_mainwid.h"

Home_MainWid::Home_MainWid(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Home_MainWid)
{
    ui->setupUi(this);
    groupBox_background_icon(this);
    initWid();
}

Home_MainWid::~Home_MainWid()
{
    delete ui;
}


void Home_MainWid::initWid()
{
    ui->tabWidget->tabBar()->hide();
    mWorkWid = new Home_WorkWid(ui->workWid);
    connect(mWorkWid, SIGNAL(typeSig(int)), ui->tabWidget, SLOT(setCurrentIndex(int)));
    connect(mWorkWid, SIGNAL(startSig()), this, SIGNAL(startSig()));

    mMpduWid = new Home_MpduWid(ui->tabWidget);
    ui->tabWidget->addTab(mMpduWid, tr("MPDU参数设置"));
    connect(mMpduWid, SIGNAL(errSig()), mWorkWid, SLOT(errSlot()));
    connect(mWorkWid, SIGNAL(enabledSig(bool)), mMpduWid, SLOT(enabledSlot(bool)));
    connect(mWorkWid, SIGNAL(savePopupSig(bool)), mMpduWid, SLOT(savePopupSlot(bool)));
    connect(mMpduWid, SIGNAL(sendMpduVerSig(int)), mWorkWid, SLOT(recvVerSlot(int)));
}
