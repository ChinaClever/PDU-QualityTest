/*
 *
 *  Created on: 2021年1月1日
 *      Author: Lzy
 */
#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    QTimer::singleShot(5,this,SLOT(initFunSlot())); //延时初始化
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::initFunSlot()
{
    initWid();
}

void MainWindow::initWid()
{
    mNavBarWid = new NavBarWid(ui->barWid);
    connect(mNavBarWid, SIGNAL(navBarSig(int)), this, SLOT(navBarSlot(int)));

    mHomeWid = new Home_MainWid(ui->stackedWid);
    ui->stackedWid->addWidget(mHomeWid);

    mTdWid = new Td_MainWid(ui->stackedWid);
    ui->stackedWid->addWidget(mTdWid);
    connect(mHomeWid, SIGNAL(startSig()), mTdWid, SIGNAL(startSig()));

    mSetupWid = new Setup_MainWid(ui->stackedWid);
    ui->stackedWid->addWidget(mSetupWid);

    mLog = new LogMainWid(ui->stackedWid);
    ui->stackedWid->addWidget(mLog);
}

void MainWindow::navBarSlot(int id)
{
    ui->stackedWid->setCurrentIndex(id);
}
