#include "home_zpdusetwid.h"
#include "ui_home_zpdusetwid.h"

Home_ZpduSetWid::Home_ZpduSetWid(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Home_ZpduSetWid)
{
    ui->setupUi(this);
    set_background_icon(this,":/image/back.jpg");
    QTimer::singleShot(15,this,SLOT(initFunSlot()));
}

Home_ZpduSetWid::~Home_ZpduSetWid()
{
    delete ui;
}

void Home_ZpduSetWid::initFunSlot()
{
    mItem = Cfg::bulid()->item;
    mObj = Dev_Zpdu::bulid(this);
    mDev = mObj->getDev();
    initWid();
    initData();
}

void Home_ZpduSetWid::initWid()
{
    mListWid.push_back(ui->op1Box);
    mListWid.push_back(ui->op2Box);
    mListWid.push_back(ui->op3Box);
    mListWid.push_back(ui->op4Box);
    mListWid.push_back(ui->op5Box);
    mListWid.push_back(ui->op6Box);
    mListWid.push_back(ui->op7Box);
    mListWid.push_back(ui->op8Box);
    mListWid.push_back(ui->op9Box);
    mListWid.push_back(ui->op10Box);

    mListWid.push_back(ui->op11Box);
    mListWid.push_back(ui->op12Box);
    mListWid.push_back(ui->op13Box);
    mListWid.push_back(ui->op14Box);
    mListWid.push_back(ui->op15Box);
    mListWid.push_back(ui->op16Box);
    mListWid.push_back(ui->op17Box);
    mListWid.push_back(ui->op18Box);
    mListWid.push_back(ui->op19Box);
    mListWid.push_back(ui->op20Box);

    mListWid.push_back(ui->op21Box);
    mListWid.push_back(ui->op22Box);
    mListWid.push_back(ui->op23Box);
    mListWid.push_back(ui->op24Box);
    mListWid.push_back(ui->op25Box);
    mListWid.push_back(ui->op26Box);
    mListWid.push_back(ui->op27Box);
    mListWid.push_back(ui->op28Box);
    mListWid.push_back(ui->op29Box);
    mListWid.push_back(ui->op30Box);

    mListWid.push_back(ui->op31Box);
    mListWid.push_back(ui->op32Box);
    mListWid.push_back(ui->op33Box);
    mListWid.push_back(ui->op34Box);
    mListWid.push_back(ui->op35Box);
    mListWid.push_back(ui->op36Box);
    mListWid.push_back(ui->op37Box);
    mListWid.push_back(ui->op38Box);
    mListWid.push_back(ui->op39Box);
    mListWid.push_back(ui->op40Box);

    mListWid.push_back(ui->op41Box);
    mListWid.push_back(ui->op42Box);
    mListWid.push_back(ui->op43Box);
    mListWid.push_back(ui->op44Box);
    mListWid.push_back(ui->op45Box);
    mListWid.push_back(ui->op46Box);
    mListWid.push_back(ui->op47Box);
    mListWid.push_back(ui->op48Box);
}

void Home_ZpduSetWid::initData()
{
    sDevType *obj = &(mDev->dt);
    ui->typeEdit->setText(obj->type);
    ui->hardVersionEdit->setText(obj->hw_version);
    ui->protocolVersionEdit->setText(obj->protocol_version);
    ui->ratedVolBox->setCurrentIndex(obj->rated_voltage);
    ui->ratedCurBox->setCurrentIndex(obj->rated_current);
    ui->ratedFreqEdit->setText(obj->rated_frequency);
    ui->lineBox->setCurrentIndex(obj->lines-1);
    ui->breakerBox->setCurrentIndex(obj->breaker);

    for(int i = 0 ; i < ZpduOpSize ; i++)
    {
        mListWid[i]->setCurrentIndex(mDev->cfg.zpduopCur[i].max == 10 ? 0 : 1);
    }
}


void Home_ZpduSetWid::updateData()
{
    sDevType *obj = &(mDev->dt);
    obj->type = ui->typeEdit->text();
    obj->hw_version = ui->hardVersionEdit->text();
    obj->protocol_version = ui->protocolVersionEdit->text();
    obj->rated_voltage = ui->ratedVolBox->currentIndex();
    obj->rated_current = ui->ratedCurBox->currentIndex();
    obj->rated_frequency = ui->ratedFreqEdit->text();
    obj->lines = ui->lineBox->currentIndex()+1;
    obj->breaker = ui->breakerBox->currentIndex();

    for(int i = 0 ; i < ZpduOpSize ; i++)
    {
        mDev->cfg.zpduopCur[i].max = mListWid[i]->currentIndex() == 0 ? 10 : 16;
        mDev->cfg.zpduopCur[i].crMax = mListWid[i]->currentIndex() == 0 ? 10 : 16;
    }
}
