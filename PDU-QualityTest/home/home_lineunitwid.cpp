/*
 *
 *  Created on: 2021年1月1日
 *      Author: Lzy
 */
#include "home_lineunitwid.h"
#include "ui_home_lineunitwid.h"

Home_LineUnitWid::Home_LineUnitWid(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Home_LineUnitWid)
{
    ui->setupUi(this);
    QGridLayout *gridLayout = new QGridLayout(parent);
    gridLayout->setContentsMargins(0, 0, 0, 0);
    gridLayout->addWidget(this);
}

Home_LineUnitWid::~Home_LineUnitWid()
{
    delete ui;
}

void Home_LineUnitWid::init(sDevData *dev)
{
    mDev = dev;
    sObjCfg *obj = &(dev->cfg);

    ui->curMinSpin->setValue(obj->cur.min);
    ui->curMaxSpin->setValue(obj->cur.max);
    ui->volMinSpin->setValue(obj->vol.min);
    ui->volMaxSpin->setValue(obj->vol.max);

    ui->temMinSpin->setValue(obj->tem.min);
    ui->temMaxSpin->setValue(obj->tem.max);
    ui->humMinSpin->setValue(obj->hum.min);
    ui->humMaxSpin->setValue(obj->hum.max);
}

void Home_LineUnitWid::updateData()
{
    sObjCfg *obj = &(mDev->cfg);
    obj->cur.min = ui->curMinSpin->value();
    obj->cur.max = ui->curMaxSpin->value();
    obj->vol.min = ui->volMinSpin->value();
    obj->vol.max = ui->volMaxSpin->value();

    obj->tem.min = ui->temMinSpin->value();
    obj->tem.max = ui->temMaxSpin->value();
    obj->hum.min = ui->humMinSpin->value();
    obj->hum.max = ui->humMaxSpin->value();
}
