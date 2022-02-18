#include "home_zpdudebugwid.h"
#include "ui_home_zpdudebugwid.h"

Home_ZpduDebugWid::Home_ZpduDebugWid(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Home_ZpduDebugWid)
{
    ui->setupUi(this);
    set_background_icon(this,":/image/back.jpg");
    QTimer::singleShot(15,this,SLOT(initFunSlot()));
}

Home_ZpduDebugWid::~Home_ZpduDebugWid()
{
    delete ui;
}

void Home_ZpduDebugWid::initFunSlot()
{
    mItem = Cfg::bulid()->item;
    mObj = Dev_Zpdu::bulid(this);
    mDev = mObj->getDev();
    initData();
}

void Home_ZpduDebugWid::initData()
{
    sDevType *obj = &(mDev->dt);
    ui->levelBox->setCurrentIndex(obj->level);
    ui->devZpduTypeBox->setCurrentIndex(obj->devZpduType-1);
    ui->standarBox->setCurrentIndex(obj->standar);
    ui->languageBox->setCurrentIndex(obj->language);
    ui->C1OpEdit->setText(QString::number(obj->loop_op[0]));
    ui->C2OpEdit->setText(QString::number(obj->loop_op[1]));
    ui->C3OpEdit->setText(QString::number(obj->loop_op[2]));
    ui->C4OpEdit->setText(QString::number(obj->loop_op[3]));
    ui->C5OpEdit->setText(QString::number(obj->loop_op[4]));
    ui->C6OpEdit->setText(QString::number(obj->loop_op[5]));

    ui->C1LoopEdit->setText(QString::number(obj->loop_smallloop[0]));
    ui->C2LoopEdit->setText(QString::number(obj->loop_smallloop[1]));
    ui->C3LoopEdit->setText(QString::number(obj->loop_smallloop[2]));
    ui->C4LoopEdit->setText(QString::number(obj->loop_smallloop[3]));
    ui->C5LoopEdit->setText(QString::number(obj->loop_smallloop[4]));
    ui->C6LoopEdit->setText(QString::number(obj->loop_smallloop[5]));

    ui->L1OpEdit->setText(QString::number(obj->line_op[0]));
    ui->L2OpEdit->setText(QString::number(obj->line_op[1]));
    ui->L3OpEdit->setText(QString::number(obj->line_op[2]));
    ui->OpEdit->setText(QString::number(obj->outputs));
}

void Home_ZpduDebugWid::updateData()
{
    sDevType *obj = &(mDev->dt);
    obj->level = ui->levelBox->currentIndex();
    obj->devZpduType = ui->devZpduTypeBox->currentIndex()+1;
    obj->standar = ui->standarBox->currentIndex();
    obj->language = ui->languageBox->currentIndex();
    obj->loop_op[0] = ui->C1OpEdit->text().toInt();
    obj->loop_op[1] = ui->C2OpEdit->text().toInt();
    obj->loop_op[2] = ui->C3OpEdit->text().toInt();
    obj->loop_op[3] = ui->C4OpEdit->text().toInt();
    obj->loop_op[4] = ui->C5OpEdit->text().toInt();
    obj->loop_op[5] = ui->C6OpEdit->text().toInt();

    obj->loop_smallloop[0] = ui->C1LoopEdit->text().toInt();
    obj->loop_smallloop[1] = ui->C2LoopEdit->text().toInt();
    obj->loop_smallloop[2] = ui->C3LoopEdit->text().toInt();
    obj->loop_smallloop[3] = ui->C4LoopEdit->text().toInt();
    obj->loop_smallloop[4] = ui->C5LoopEdit->text().toInt();
    obj->loop_smallloop[5] = ui->C6LoopEdit->text().toInt();

    obj->line_op[0] = ui->L1OpEdit->text().toInt();
    obj->line_op[1] = ui->L2OpEdit->text().toInt();
    obj->line_op[2] = ui->L3OpEdit->text().toInt();
    obj->outputs = ui->OpEdit->text().toInt();
}

bool Home_ZpduDebugWid::loopCheck()
{
    int res = 0;
    bool ret = true;
    int v = ui->OpEdit->text().toInt();
    res += ui->C1OpEdit->text().toInt();
    res += ui->C2OpEdit->text().toInt();
    res += ui->C3OpEdit->text().toInt();
    res += ui->C4OpEdit->text().toInt();
    res += ui->C5OpEdit->text().toInt();
    res += ui->C6OpEdit->text().toInt();
    if(v != res) ret = false;
    return ret;
}

bool Home_ZpduDebugWid::lineCheck()
{
    int res = 0;
    bool ret = true;
    int v = ui->OpEdit->text().toInt();
    res += ui->L1OpEdit->text().toInt();
    res += ui->L2OpEdit->text().toInt();
    res += ui->L3OpEdit->text().toInt();
    if(v != res) ret = false;
    return ret;
}
