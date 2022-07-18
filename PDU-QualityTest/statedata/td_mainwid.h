#ifndef TD_MAINWID_H
#define TD_MAINWID_H

#include <QWidget>
#include "home_mainwid.h"
#include "td_statustabwid.h"

namespace Ui {
class Td_MainWid;
}

class Td_MainWid : public QWidget
{
    Q_OBJECT

public:
    explicit Td_MainWid(QWidget *parent = nullptr);
    ~Td_MainWid();
    void exportLog(QString str);

signals:
    void startSig();

private slots:
    void on_exportBtn_clicked();


private:
    Ui::Td_MainWid *ui;
    Td_StatusTabWid *mStatusTabWid;
    sCfgItem * mItem;
};

#endif // TD_MAINWID_H
