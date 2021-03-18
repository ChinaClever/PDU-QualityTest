#ifndef HOME_MPDUTHRESHOLDWID_H
#define HOME_MPDUTHRESHOLDWID_H

#include "home_setopdlg.h"

namespace Ui {
class Home_MpduAlarmWid;
}

class Home_MpduAlarmWid : public QWidget
{
    Q_OBJECT

public:
    explicit Home_MpduAlarmWid(QWidget *parent = nullptr);
    ~Home_MpduAlarmWid();

    void updateData();
protected:
    void initData();

protected slots:
    void initFunSlot();

private:
    Ui::Home_MpduAlarmWid *ui;
    sCfgItem *mItem;
    Dev_Object *mObj;
    sDevData *mDev;
};

#endif // HOME_MPDUTHRESHOLDWID_H
