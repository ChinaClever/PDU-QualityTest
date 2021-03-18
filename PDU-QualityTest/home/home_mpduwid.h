#ifndef HOME_MPDUBWID_H
#define HOME_MPDUBWID_H

#include "home_mpduparamwid.h"

namespace Ui {
class Home_MpduWid;
}

class Home_MpduWid : public QWidget
{
    Q_OBJECT

public:
    explicit Home_MpduWid(QWidget *parent = nullptr);
    ~Home_MpduWid();

signals:
    void errSig();

protected:
    void initWid();
    bool inputCheck();
    bool dataSave();

public slots:
    void initFunSlot();
    void enabledSlot(bool en);
    void indexHiddenSlot(int index);

private:
    Ui::Home_MpduWid *ui;
    sCfgItem *mItem;
    Dev_Object *mObj;
    sDevData *mDev;

    Home_MpduParamWid *mParamWid;
    Home_MpduAlarmWid *mAlarmWid;
};

#endif // HOME_MPDUBWID_H
