#include "home_mpduparamwid.h"
#include "ui_home_mpduparamwid.h"

Home_MpduParamWid::Home_MpduParamWid(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Home_MpduParamWid)
{
    ui->setupUi(this);
    set_background_icon(this,":/image/back.jpg");
    QTimer::singleShot(15,this,SLOT(initFunSlot()));
}

Home_MpduParamWid::~Home_MpduParamWid()
{
    delete ui;
}

void Home_MpduParamWid::initFunSlot()
{
    mItem = Cfg::bulid()->item;
    mObj = Dev_Mpdu::bulid(this);
    mDev = mObj->getDev();
    initWid();
    initType();
}

void Home_MpduParamWid::initWid()
{
    int i = 0;
    mLoops[i++] = ui->lpSpin_1;
    mLoops[i++] = ui->lpSpin_2;
    mLoops[i++] = ui->lpSpin_3;
    mLoops[i++] = ui->lpSpin_4;
    mLoops[i++] = ui->lpSpin_5;
    mLoops[i++] = ui->lpSpin_6;

    i = 0;
    mBoards[i++] = ui->opSpin_1;
    mBoards[i++] = ui->opSpin_2;
    mBoards[i++] = ui->opSpin_3;
    mBoards[i++] = ui->opSpin_4;
    mBoards[i++] = ui->opSpin_5;
    mBoards[i++] = ui->opSpin_6;
}

void Home_MpduParamWid::initType()
{
    sDevType *dt = &(mDev->dt); //设备类型
    int v = dt->lines-1; if(v) v = 1;
    ui->lineBox->setCurrentIndex(v);
    v = dt->loops-1; if(v>4) v = 4;
    ui->loopBox->setCurrentIndex(v);

    ui->outputSpin->setValue(dt->outputs);
    ui->breakerBox->setCurrentIndex(dt->breaker);
    ui->standardBox->setCurrentIndex(dt->standar);
    ui->seriesBox->setCurrentIndex(dt->series-1);
    ui->envBox->setCurrentIndex(dt->envbox);
    ui->modbusBox->setCurrentIndex(dt->modbus);
    ui->languageBox->setCurrentIndex(dt->language);
    ui->verBox->setCurrentIndex(dt->mpdu_ver);
    ui->levelBox->setCurrentIndex(dt->level);
    ui->versionEdit->setText(dt->versions);
    ui->boardSpin->setValue(dt->boards);
    ui->safeRadio->setChecked(dt->security);

    on_verBox_currentIndexChanged(dt->mpdu_ver);
    emit indexHiddenSig(dt->mpdu_ver);
    for(int i=0; i<6; ++i) mLoops[i]->setValue(dt->loop[i]);
    for(int i=0; i<dt->boards; ++i) mBoards[i]->setValue(dt->board[i]);
    bool en = true;
    for(int i=dt->boards; i<6; ++i){
      mBoards[i]->setValue(0);
      mBoards[i]->setHidden(en);
    }
}


void Home_MpduParamWid::updateType()
{
    sDevType *dt = &(mDev->dt); //设备类型
    int v = ui->lineBox->currentIndex();
    if(v) v = 3; else v = 1; dt->lines = v;

    v = ui->loopBox->currentIndex()+1;
    if(v > 4) v = 6; dt->loops = v;

    dt->outputs = ui->outputSpin->value();
    dt->breaker = ui->breakerBox->currentIndex();
    dt->standar = ui->standardBox->currentIndex();
    dt->series = ui->seriesBox->currentIndex()+1;

    dt->envbox = ui->envBox->currentIndex();
    dt->modbus = ui->modbusBox->currentIndex();
    dt->language = ui->languageBox->currentIndex();
    dt->mpdu_ver = ui->verBox->currentIndex();
    dt->level = ui->levelBox->currentIndex();
    dt->versions = ui->versionEdit->text();
    dt->boards = ui->boardSpin->value();
    dt->security = ui->safeRadio->isChecked()?1:0;

    for(int i=0; i<6; ++i) dt->loop[i] = mLoops[i]->value();
    for(int i=0; i<6; ++i) dt->board[i] = mBoards[i]->value();

    if( dt->mpdu_ver == 2 && !dt->versions.contains(".") )
        emit sendVerSig(dt->versions.toInt());
    else
        emit sendVerSig(30);

    mItem->sn = ui->snEdit->text();
}

void Home_MpduParamWid::setItHidden(bool hidden)
{
    ui->lineBox->setHidden(hidden);
    ui->outputSpin->setHidden(hidden);
    ui->loopBox->setHidden(hidden);
    ui->breakerBox->setHidden(hidden);
    ui->modbusBox->setHidden(hidden);
    ui->standardBox->setHidden(hidden);

    ui->label_3->setHidden(hidden);
    ui->label_4->setHidden(hidden);
    ui->label_5->setHidden(hidden);
    ui->label_6->setHidden(hidden);
    ui->label_8->setHidden(hidden);
    ui->label_10->setHidden(hidden);

    ui->label->setHidden(!hidden);
    ui->snEdit->setHidden(!hidden);
}

void Home_MpduParamWid::setItHiddenOpCtrl(bool hidden)
{
    ui->lineBox->setHidden(hidden);
    ui->outputSpin->setHidden(hidden);
    ui->loopBox->setHidden(hidden);
    ui->breakerBox->setHidden(hidden);
    ui->modbusBox->setHidden(hidden);
    ui->standardBox->setHidden(hidden);
    ui->languageBox->setHidden(hidden);
    ui->seriesBox->setHidden(hidden);

    ui->label_3->setHidden(hidden);
    ui->label_4->setHidden(hidden);
    ui->label_5->setHidden(hidden);
    ui->label_6->setHidden(hidden);
    ui->label_7->setHidden(hidden);
    ui->label_8->setHidden(hidden);
    ui->label_9->setHidden(hidden);
    ui->label_10->setHidden(hidden);
}

void Home_MpduParamWid::setItShow(bool hidden)
{
    ui->label_7->setHidden(hidden);
    ui->label_9->setHidden(hidden);
    ui->languageBox->setHidden(hidden);
    ui->seriesBox->setHidden(hidden);
}

void Home_MpduParamWid::on_verBox_currentIndexChanged(int index)
{
    bool hidden = true;
    if(index) hidden = false; setItHidden(hidden);
    if(1 == index) hidden = true;
    ui->groupBox_2->setHidden(hidden);
    if(1 == index) setItHiddenOpCtrl(true);
    else setItShow(false);
    emit indexHiddenSig(index);
}

void Home_MpduParamWid::on_boardSpin_valueChanged(int arg1)
{
    bool en = true;
    if(arg1 == 0) arg1 = 1;
    int v = ui->outputSpin->value() / arg1;
    for(int i=0; i<6; ++i) {
        if(i < arg1) {
            en = false;
            mBoards[i]->setValue(v);
        } else {
            en = true;
            mBoards[i]->setValue(0);
        }
        mBoards[i]->setHidden(en);
    }
}

void Home_MpduParamWid::on_loopBox_currentIndexChanged(int index)
{
    bool en = true;
    if(index >= 4) index++;
    int v = ui->outputSpin->value() / (index+1);
    for(int i=0; i<6; ++i) {
        if(i > index) {
            en = true;
            mLoops[i]->setValue(0);
        } else {
            en = false;
            mLoops[i]->setValue(v);
        }
        mLoops[i]->setHidden(en);
    }
}

bool Home_MpduParamWid::outputCheck()
{
    int res = 0;
    bool ret = true;
    int v = ui->outputSpin->value();
    for(int i=0; i<6; ++i) {
        res += mBoards[i]->value();
    }
    if(v != res) ret = false;
    return ret;
}

bool Home_MpduParamWid::loopCheck()
{
    int res = 0;
    bool ret = true;
    int v = ui->outputSpin->value();
    for(int i=0; i<6; ++i) {
        res += mLoops[i]->value();
    }
    if(v != res) ret = false;
    return ret;
}

void Home_MpduParamWid::on_outputSpin_valueChanged(int)
{
    int v = ui->boardSpin->value();
    on_boardSpin_valueChanged(v);

    v = ui->loopBox->currentIndex();
    on_loopBox_currentIndexChanged(v);
}

void Home_MpduParamWid::setItemEnable(int id, int en)
{
    QModelIndex index = ui->loopBox->model()->index(id, 0);
    ui->loopBox->model()->setData(index, QVariant(en), Qt::UserRole - 1);
}

void Home_MpduParamWid::on_lineBox_currentIndexChanged(int index)
{
    for(int i=0; i<5; ++i) setItemEnable(i, 1|32);
    if(index) {
        setItemEnable(0, 0);
        setItemEnable(1, 0);
        setItemEnable(3, 0);
        ui->loopBox->setCurrentIndex(2);
    } else {
        setItemEnable(2, 0);
        setItemEnable(4, 0);
        ui->loopBox->setCurrentIndex(0);
    }
}
