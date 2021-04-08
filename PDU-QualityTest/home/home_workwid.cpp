/*
 *
 *  Created on: 2021年1月1日
 *      Author: Lzy
 */
#include "home_workwid.h"
#include "ui_home_workwid.h"

Home_WorkWid::Home_WorkWid(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Home_WorkWid)
{
    ui->setupUi(this);

    QTimer::singleShot(250,this,SLOT(initFunSlot()));
}

Home_WorkWid::~Home_WorkWid()
{
    delete ui;
}

void Home_WorkWid::initLayout()
{
    QPalette pl = ui->textEdit->palette();
    pl.setBrush(QPalette::Base,QBrush(QColor(255,0,0,0)));
    ui->textEdit->setPalette(pl);
    //ui->textEdit->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOn);
    //ui->textEdit->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);

    QGridLayout *gridLayout = new QGridLayout(this->parentWidget());
    gridLayout->setContentsMargins(0, 7, 0, 0);
    gridLayout->addWidget(this);
}

void Home_WorkWid::initFunSlot()
{
    mCnt = 0;
    mSetOpDlg = new Home_SetOpDlg(this);
    mCoreThread = new Test_CoreThread(this);

    mPacket = sDataPacket::bulid();
    mPro = mPacket->getPro();
    mItem = Cfg::bulid()->item;
    mPro->step = Test_End;
    ui->cntSpin->setValue(mItem->cnt.cnt);
    ui->userEdit->setText(mItem->user);

    initLayout();
    initTypeComboBox();
    timer = new QTimer(this);
    timer->start(500);
    connect(timer, SIGNAL(timeout()), this, SLOT(timeoutDone()));
}

void Home_WorkWid::setTextColor()
{
    QColor color("black");
    bool pass = mPro->pass.first();
    if(!pass) color = QColor("red");
    ui->textEdit->moveCursor(QTextCursor::Start);

    QTextCharFormat fmt;//文本字符格式
    fmt.setForeground(color);// 前景色(即字体色)设为color色
    QTextCursor cursor = ui->textEdit->textCursor();//获取文本光标
    cursor.mergeCharFormat(fmt);//光标后的文字就用该格式显示
    ui->textEdit->mergeCurrentCharFormat(fmt);//textEdit使用当前的字符格式
}

void Home_WorkWid::insertText()
{
    while(mPro->status.size()) {
        setTextColor();
        QString str = QString::number(mId++) + "、"+ mPro->status.first() + "\n";
        ui->textEdit->insertPlainText(str);
        mPro->status.removeFirst();
        mPro->pass.removeFirst();
    }
}

void Home_WorkWid::updateCnt()
{
    sCount *cnt = &(mItem->cnt);
    ui->okLcd->display(cnt->ok);
    ui->allLcd->display(cnt->all);
    ui->errLcd->display(cnt->err);

    QString str = "0";
    if(cnt->all) {
        double value = cnt->ok*100.0 / cnt->all;
        str = QString::number(value,'f',0) +"%";
    }
    ui->passLcd->display(str);
}

QString Home_WorkWid::getTime()
{
    QTime t(0,0,0,0);
    t = t.addSecs(mPro->startTime.secsTo(QTime::currentTime()));
    return  tr("%1").arg(t.toString("mm:ss"));
}

void Home_WorkWid::updateTime()
{
    QString str = getTime();
    QString style = "background-color:yellow; color:rgb(0, 0, 0);";
    style += "font:100 34pt \"微软雅黑\";";

    ui->timeLab->setText(str);
    ui->timeLab->setStyleSheet(style);
    ui->startBtn->setText(tr("终止设置"));
}

void Home_WorkWid::updateResult()
{
    QString style;
    QString str = tr("---");
    if (Test_Fail == mPro->result) {
        str = tr("失败");
        style = "background-color:red; color:rgb(255, 255, 255);";
    } else {
        str = tr("成功");
        style = "background-color:green; color:rgb(255, 255, 255);";
    }
    style += "font:100 34pt \"微软雅黑\";";

    mPro->step = Test_End;
    ui->timeLab->setText(str);
    ui->timeLab->setStyleSheet(style);
    ui->groupBox_4->setEnabled(true);
    ui->startBtn->setText(tr("开始设置"));
    ui->cntSpin->setValue(mItem->cnt.cnt);
    if(mItem->cnt.cnt < 1) {
        mItem->user.clear();
        ui->userEdit->setText(mItem->user);
    }
}

void Home_WorkWid::updateWid()
{
    QString str = mItem->sn;
    if(str.isEmpty()) str = "--- ---";
    ui->snLab->setText(str);

    str = mItem->dev_type;
    if(str.isEmpty()) str = "--- ---";
    ui->devLab->setText(str);

    if(mPro->step < Test_Over) {
        updateTime();
    } else if(mPro->step < Test_End){
        updateResult();
    }
}

void Home_WorkWid::timeoutDone()
{
    updateCnt();
    if(mPro->step < Test_End) {
        insertText();
        updateWid();
    }
}

bool Home_WorkWid::initSerial()
{
    bool ret = true;
    if(mItem->modeId <= MPDU) {
        ret = mItem->com->isOpened();
        mItem->dev_type.clear();
    } else {
        mItem->dev_type = ui->typeComboBox->currentText();
    }

    if(ret){
        mId = 1;
        mItem->sn.clear();
    } else {
        MsgBox::critical(this, tr("请先打开串口")); return ret;
    }

    return ret;
}

bool Home_WorkWid::initWid()
{
    bool ret = initSerial();
    if(ret) {
        if(mItem->user.isEmpty()) {
            MsgBox::critical(this, tr("请先填写客户名称！")); return false;
        }
        if(mItem->cnt.cnt < 1) {
            MsgBox::critical(this, tr("请先填写订单剩余数量！")); return false;
        }

        mPacket->init();
        emit startSig();
        ui->textEdit->clear();
        mPro->step = Test_Start;
        ui->groupBox_4->setEnabled(false);
    }

    return ret;
}

void Home_WorkWid::on_startBtn_clicked()
{
    bool ret = true;
    if(mPro->step == Test_End) {
        if(initWid())mCoreThread->start();
    } else {
        ret = MsgBox::question(this, tr("确定需要提前结束？"));
        if(ret) {
            mPro->result = Test_Fail;
            updateResult();
        }
    }
}

void Home_WorkWid::saveFunSlot()
{
    bool en = mCnt % 2;
    emit enabledSig(en);
    if(!en) Cfg::bulid()->writeCfgDev();
}

void Home_WorkWid::on_setBtn_clicked()
{
    QString str = tr("修改");
    bool en = ++mCnt % 2;
    if(en) str = tr("保存");

    ui->setBtn->setText(str);
    ui->cntSpin->setEnabled(en);
    ui->userEdit->setEnabled(en);
    ui->startBtn->setDisabled(en);
    ui->typeComboBox->setDisabled(en);
    mItem->cnt.cnt = ui->cntSpin->value();
    if(mItem->user != ui->userEdit->text()) {
        mItem->user = ui->userEdit->text();
        sCount *cnt = &(mItem->cnt);
        cnt->all = cnt->ok = cnt->err = 0;
        Cfg::bulid()->writeCnt();
    }

    QTimer::singleShot(50,this,SLOT(saveFunSlot()));
}

void Home_WorkWid::saveErrSlot()
{
    mCnt = 1;
    emit enabledSig(true);
    ui->setBtn->setText(tr("保存"));
}

void Home_WorkWid::on_outputBtn_clicked()
{
    mSetOpDlg->exec();
}

void Home_WorkWid::on_typeComboBox_currentIndexChanged(int index)
{
    mItem->modeId = index;
    initTypeComboBox();
    Cfg::bulid()->writeCfgDev();
}

void Home_WorkWid::initTypeComboBox()
{
    bool en = false;
    int index = mItem->modeId;
    mItem->enSn = ui->snCheckBox->isChecked();
    if(index > MPDU) {
        en = true;
        mItem->enSn = false;
        ui->outputBtn->setHidden(en);
    } else if(index == MPDU) {
        ui->outputBtn->setHidden(false);
    } else {
        ui->outputBtn->setHidden(true);
    }
    //ui->setBtn->setHidden(en);
    ui->snCheckBox->setHidden(en);

    mSetOpDlg->updateIndex(index);
    ui->typeComboBox->setCurrentIndex(index);
    emit typeSig(index);
}

void Home_WorkWid::on_snCheckBox_clicked(bool checked)
{
    mItem->enSn = checked;
    if(!checked) MsgBox::information(this, tr("注意：创建序列号有利于产品溯源。你已选择不创建序列号。"));
}
