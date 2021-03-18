/*
 *
 *  Created on: 2021年1月1日
 *      Author: Lzy
 */
#include "home_setopdlg.h"
#include "ui_home_setopdlg.h"

Home_SetOpDlg::Home_SetOpDlg(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Home_SetOpDlg)
{
    ui->setupUi(this);
    groupBox_background_icon(this);
    mOutputWid = new Home_OutputWid(ui->groupBox);
}

Home_SetOpDlg::~Home_SetOpDlg()
{
    delete ui;
}

void Home_SetOpDlg::on_okBtn_clicked()
{
    sUnitCfg unit;

    unit.en = ui->enComboBox->currentIndex();
    unit.min = ui->curMinSpin->value();
    unit.max = ui->curMaxSpin->value();
    unit.crMin = ui->curCrMinSpin->value();
    unit.crMax = ui->curCrMaxSpin->value();
    mOutputWid->setUnit(unit);
}


void Home_SetOpDlg::updateIndex(int id)
{
    mDev = Dev_Mpdu::bulid(this);
    switch (id) {
    case MPDU: break;
    case ZPDU: break;
    }

    sObjCfg *obj = &(mDev->getDev()->cfg);
    mOutputWid->init(obj);
}

void Home_SetOpDlg::on_saveBtn_clicked()
{
    this->accept();
    mOutputWid->updateData();
    mDev->save();
}
