#ifndef HOME_OPUNITWID_H
#define HOME_OPUNITWID_H

#include "home_lineunitwid.h"

namespace Ui {
class Home_OpUnitWid;
}

class Home_OpUnitWid : public QWidget
{
    Q_OBJECT

public:
    explicit Home_OpUnitWid(QWidget *parent = nullptr);
    ~Home_OpUnitWid();

    void updateData();
    void init(sUnitCfg *opCur);
    void setUnit(sUnitCfg &unit);

private:
    Ui::Home_OpUnitWid *ui;
    sUnitCfg *mOpCur;
};

#endif // HOME_OPUNITWID_H
