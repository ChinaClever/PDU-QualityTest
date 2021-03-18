/*
 *
 *  Created on: 2021年1月1日
 *      Author: Lzy
 */
#include "home_opunitwid.h"
#include "ui_home_opunitwid.h"

Home_OpUnitWid::Home_OpUnitWid(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Home_OpUnitWid)
{
    ui->setupUi(this);
    QGridLayout *gridLayout = new QGridLayout(parent);
    gridLayout->setContentsMargins(0, 0, 0, 0);
    gridLayout->addWidget(this);
}

Home_OpUnitWid::~Home_OpUnitWid()
{
    delete ui;
}

void Home_OpUnitWid::init(sUnitCfg *opCur)
{
    mOpCur = opCur;

    ui->idSpin->setValue(mOpCur->id);
    ui->enComboBox->setCurrentIndex(mOpCur->en);

    ui->curMinSpin->setValue(mOpCur->min);
    ui->curMaxSpin->setValue(mOpCur->max);

    ui->curCrMinSpin->setValue(mOpCur->crMin);
    ui->curCrMaxSpin->setValue(mOpCur->crMax);
}

void Home_OpUnitWid::updateData()
{
    mOpCur->id = ui->idSpin->value();
    mOpCur->en = ui->enComboBox->currentIndex();

    mOpCur->min = ui->curMinSpin->value();
    mOpCur->max = ui->curMaxSpin->value();
    mOpCur->crMin = ui->curCrMinSpin->value();
    mOpCur->crMax = ui->curCrMaxSpin->value();

}

void Home_OpUnitWid::setUnit(sUnitCfg &unit)
{
    ui->enComboBox->setCurrentIndex(unit.en);

    ui->curMinSpin->setValue(unit.min);
    ui->curMaxSpin->setValue(unit.max);

    ui->curCrMinSpin->setValue(unit.crMin);
    ui->curCrMaxSpin->setValue(unit.crMax);
}
