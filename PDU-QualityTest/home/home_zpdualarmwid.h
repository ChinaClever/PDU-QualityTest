#ifndef HOME_ZPDUALARMWID_H
#define HOME_ZPDUALARMWID_H

#include <QWidget>
#include "common.h"
#include "devices/dev_object.h"
#include "devices/dev_zpdu.h"

namespace Ui {
class Home_ZpduAlarmWid;
}

class Home_ZpduAlarmWid : public QWidget
{
    Q_OBJECT

public:
    explicit Home_ZpduAlarmWid(QWidget *parent = nullptr);
    ~Home_ZpduAlarmWid();
    void updateData();

protected slots:
    void initFunSlot();

private:
    void initData();

private:
    Ui::Home_ZpduAlarmWid *ui;
    sCfgItem *mItem;
    Dev_Object *mObj;
    sDevData *mDev;
};

#endif // HOME_ZPDUALARMWID_H
