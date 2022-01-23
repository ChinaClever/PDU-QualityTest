#include "home_zpduwid.h"
#include "ui_home_zpduwid.h"

Home_ZpduWid::Home_ZpduWid(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Home_ZpduWid)
{
    ui->setupUi(this);
    set_background_icon(this,":/image/back.jpg");
    QTimer::singleShot(15,this,SLOT(initFunSlot()));
}

Home_ZpduWid::~Home_ZpduWid()
{
    delete ui;
}

void Home_ZpduWid::initFunSlot()
{
    this->setEnabled(false);
    mItem = Cfg::bulid()->item;
    mObj = Dev_Zpdu::bulid(this);
    mDev = mObj->getDev();
    initWid();
}

void Home_ZpduWid::initWid()
{

    //    connect(mZpduAlarmWid, SIGNAL(indexHiddenSig(int)), this, SLOT(indexHiddenSlot(int)));
    //    connect(mZpduAlarmWid, SIGNAL(sendVerSig(int)), this, SIGNAL(sendMpduVerSig(int)));

    QString str = tr("ZPDU Debug参数");
    mZpduDebugWid = new Home_ZpduDebugWid(ui->tabWidget);
    ui->tabWidget->addTab(mZpduDebugWid, str);

    str = tr("ZPDU报警参数");
    mZpduAlarmWid = new Home_ZpduAlarmWid(ui->tabWidget);
    ui->tabWidget->addTab(mZpduAlarmWid, str);

    str = tr("ZPDU Set参数");
    mZpduSetWid = new Home_ZpduSetWid(ui->tabWidget);
    ui->tabWidget->addTab(mZpduSetWid, str);
}

bool Home_ZpduWid::inputCheck()
{
    QString str;
    bool ret = mZpduDebugWid->lineCheck();
    if(!ret) str += tr("每个相位输出位数量出错！\n");
    ret = mZpduDebugWid->loopCheck();
    if(!ret) str += tr("每个回路输出位数量出错！\n");
    if(!str.isEmpty()) {
        MsgBox::critical(this, str);
        ret = false;
    }
    return ret;
}

bool Home_ZpduWid::dataSave()
{
    bool ret = inputCheck();
    if(ret) {
        mZpduSetWid->updateData();
        mZpduAlarmWid->updateData();
        mZpduDebugWid->updateData();
    }

    return ret;
}

void Home_ZpduWid::enabledSlot(bool en)
{
    if(mItem->modeId != ZPDU) return;

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

void Home_ZpduWid::savePopupSlot(bool en)
{
    if(mItem->modeId != ZPDU) return;
    mObj->savePopup(en);
}
