#ifndef HOME_OUTPUTWID_H
#define HOME_OUTPUTWID_H

#include "home_opunitwid.h"

namespace Ui {
class Home_OutputWid;
}

class Home_OutputWid : public QWidget
{
    Q_OBJECT

public:
    explicit Home_OutputWid(QWidget *parent = nullptr);
    ~Home_OutputWid();

    void updateData();
    void init(sObjCfg *dev);
    void setUnit(sUnitCfg &unit);

protected:
    void initWid();

private:
    Ui::Home_OutputWid *ui;
    Home_OpUnitWid *mBoxWid[OpSize];
    int mId;
};

#endif // HOME_OUTPUTWID_H
