/*
 *
 *  Created on: 2021年1月1日
 *      Author: Lzy
 */
#include "td_mainwid.h"
#include "ui_td_mainwid.h"
#include <QFileDialog>
#include "common/cfgcom/config.h"

Td_MainWid::Td_MainWid(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Td_MainWid)
{
    ui->setupUi(this);
    groupBox_background_icon(this);
    mStatusTabWid = new Td_StatusTabWid(ui->groupBox);
    connect(this, SIGNAL(startSig()), mStatusTabWid, SLOT(startSlot()));
    mItem = Cfg::bulid()->item;
}

Td_MainWid::~Td_MainWid()
{
    delete ui;
}

void Td_MainWid::exportLog(QString str)
{
    QList<QStringList> list;
    mStatusTabWid->getList(list);
    QString path = "/logs/";
    QString fi = "/"+str+".csv";

    QDir dir;
    path = dir.currentPath()+"/logs";
    QDir pathdir(path);
    bool ok = false;
    if(!pathdir.exists()){
        ok = pathdir.mkdir(path);
    }
    QFile file(path+fi);
    if(!file.open(QIODevice::WriteOnly | QIODevice::Append | QIODevice::NewOnly)){
        qDebug()<<"no this file! ! !";
    }else{
        QTextStream csvOutput(&file);
        for(int i = 0 ; i < list.size() ; i++){
            for(int j = 0 ; j < list.at(i).size() ; j++){
                csvOutput<<list.at(i).at(j).toUtf8();
                if( j != list.at(i).size()-1 ) csvOutput<<",";
            }
            csvOutput<<"\n";
        }
        file.flush();
        file.close();
    }
}

void Td_MainWid::on_exportBtn_clicked()
{
    if(mItem->sn.isEmpty()){
        QString str = QDateTime::currentDateTime().toString("yyyy-MM-dd hh-mm-ss");
        exportLog(str);
    }else{
        exportLog(mItem->sn);
    }
}
