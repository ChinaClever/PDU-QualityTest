#include "home_zpdualarmwid.h"
#include "ui_home_zpdualarmwid.h"

Home_ZpduAlarmWid::Home_ZpduAlarmWid(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Home_ZpduAlarmWid)
{
    ui->setupUi(this);
    set_background_icon(this,":/image/back.jpg");
    QTimer::singleShot(15,this,SLOT(initFunSlot()));
}

Home_ZpduAlarmWid::~Home_ZpduAlarmWid()
{
    delete ui;
}


void Home_ZpduAlarmWid::initFunSlot()
{
    mItem = Cfg::bulid()->item;
    mObj = Dev_Zpdu::bulid(this);
    mDev = mObj->getDev();
    initData();
}

void Home_ZpduAlarmWid::initData()
{
    sObjCfg *obj = &(mDev->cfg);
    ui->loopMinSpin->setValue(obj->loopcur.min);
    ui->loopMaxSpin->setValue(obj->loopcur.max);
    ui->loopCrMinSpin->setValue(obj->loopcur.crMin);
    ui->loopCrMaxSpin->setValue(obj->loopcur.crMax);

    ui->curMinSpin->setValue(obj->cur.min);
    ui->curMaxSpin->setValue(obj->cur.max);
    ui->curCrMinSpin->setValue(obj->cur.crMin);
    ui->curCrMaxSpin->setValue(obj->cur.crMax);

    ui->volMinSpin->setValue(obj->vol.min);
    ui->volMaxSpin->setValue(obj->vol.max);
    ui->volCrMinSpin->setValue(obj->vol.crMin);
    ui->volCrMaxSpin->setValue(obj->vol.crMax);

    ui->temMinSpin->setValue(obj->tem.min);
    ui->temMaxSpin->setValue(obj->tem.max);
    ui->temCrMinSpin->setValue(obj->tem.crMin);
    ui->temCrMaxSpin->setValue(obj->tem.crMax);

    ui->humMinSpin->setValue(obj->hum.min);
    ui->humMaxSpin->setValue(obj->hum.max);
    ui->humCrMinSpin->setValue(obj->hum.crMin);
    ui->humCrMaxSpin->setValue(obj->hum.crMax);

}


void Home_ZpduAlarmWid::updateData()
{
    sObjCfg *obj = &(mDev->cfg);
    obj->loopcur.min = ui->loopMinSpin->value();
    obj->loopcur.max = ui->loopMaxSpin->value();
    obj->loopcur.crMin = ui->loopCrMinSpin->value();
    obj->loopcur.crMax = ui->loopCrMaxSpin->value();

    obj->cur.min = ui->curMinSpin->value();
    obj->cur.max = ui->curMaxSpin->value();
    obj->cur.crMin = ui->curCrMinSpin->value();
    obj->cur.crMax = ui->curCrMaxSpin->value();

    obj->vol.min = ui->volMinSpin->value();
    obj->vol.max = ui->volMaxSpin->value();
    obj->vol.crMin = ui->volCrMinSpin->value();
    obj->vol.crMax = ui->volCrMaxSpin->value();

    obj->tem.min = ui->temMinSpin->value();
    obj->tem.max = ui->temMaxSpin->value();
    obj->tem.crMin = ui->temCrMinSpin->value();
    obj->tem.crMax = ui->temCrMaxSpin->value();

    obj->hum.min = ui->humMinSpin->value();
    obj->hum.max = ui->humMaxSpin->value();
    obj->hum.crMin = ui->humCrMinSpin->value();
    obj->hum.crMax = ui->humCrMaxSpin->value();

}
