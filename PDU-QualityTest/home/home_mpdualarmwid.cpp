#include "home_mpdualarmwid.h"
#include "ui_home_mpdualarmwid.h"

Home_MpduAlarmWid::Home_MpduAlarmWid(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Home_MpduAlarmWid)
{
    ui->setupUi(this);
    set_background_icon(this,":/image/back.jpg");
    QTimer::singleShot(15,this,SLOT(initFunSlot()));
}

Home_MpduAlarmWid::~Home_MpduAlarmWid()
{
    delete ui;
}


void Home_MpduAlarmWid::initFunSlot()
{
    mItem = Cfg::bulid()->item;
    mObj = Dev_Mpdu::bulid(this);
    mDev = mObj->getDev();
    initData();
}

void Home_MpduAlarmWid::initData()
{
    sObjCfg *obj = &(mDev->cfg);
    ui->outputMinSpin->setValue(obj->output.min);
    ui->outputMaxSpin->setValue(obj->output.max);
    ui->outputCrMinSpin->setValue(obj->output.crMin);
    ui->outputCrMaxSpin->setValue(obj->output.crMax);

    ui->curMinSpin->setValue(obj->cur.min);
    ui->curMaxSpin->setValue(obj->cur.max);
    ui->curCrMinSpin->setValue(obj->cur.crMin);
    ui->curCrMaxSpin->setValue(obj->cur.crMax);

    ui->volMinSpin->setValue(obj->vol.min);
    ui->volMaxSpin->setValue(obj->vol.max);

    ui->temMinSpin->setValue(obj->tem.min);
    ui->temMaxSpin->setValue(obj->tem.max);

    ui->humMinSpin->setValue(obj->hum.min);
    ui->humMaxSpin->setValue(obj->hum.max);
}


void Home_MpduAlarmWid::updateData()
{
    sObjCfg *obj = &(mDev->cfg);
    obj->output.min = ui->outputMinSpin->value();
    obj->output.max = ui->outputMaxSpin->value();
    obj->output.crMin = ui->outputCrMinSpin->value();
    obj->output.crMax = ui->outputCrMaxSpin->value();

    obj->cur.min = ui->curMinSpin->value();
    obj->cur.max = ui->curMaxSpin->value();
    obj->cur.crMin = ui->curCrMinSpin->value();
    obj->cur.crMax = ui->curCrMaxSpin->value();

    obj->vol.min = ui->volMinSpin->value();
    obj->vol.max = ui->volMaxSpin->value();

    obj->tem.min = ui->temMinSpin->value();
    obj->tem.max = ui->temMaxSpin->value();
    obj->hum.min = ui->humMinSpin->value();
    obj->hum.max = ui->humMaxSpin->value();
}
