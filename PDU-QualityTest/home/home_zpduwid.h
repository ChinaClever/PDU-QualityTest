#ifndef HOME_ZPDUWID_H
#define HOME_ZPDUWID_H

#include <QWidget>
#include "home_mpduwid.h"
#include "devices/dev_zpdu.h"
#include "home_zpdualarmwid.h"
#include "home_zpdudebugwid.h"
#include "home_zpdusetwid.h"

namespace Ui {
class Home_ZpduWid;
}

class Home_ZpduWid : public QWidget
{
    Q_OBJECT

public:
    explicit Home_ZpduWid(QWidget *parent = nullptr);
    ~Home_ZpduWid();
signals:
    void errSig();
    void sendMpduVerSig(int);

protected:
    void initWid();
    bool inputCheck();
    bool dataSave();

public slots:
    void initFunSlot();
    void enabledSlot(bool en);
    void savePopupSlot(bool en);
    //void indexHiddenSlot(int index);

private:
    Ui::Home_ZpduWid *ui;
    sCfgItem *mItem;
    Dev_Object *mObj;
    sDevData *mDev;
    Home_ZpduAlarmWid* mZpduAlarmWid;
    Home_ZpduDebugWid* mZpduDebugWid;
    Home_ZpduSetWid* mZpduSetWid;
};

#endif // HOME_ZPDUWID_H
