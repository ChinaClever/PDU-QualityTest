#ifndef HOME_THUNITWID_H
#define HOME_THUNITWID_H

#include <QWidget>
#include "common.h"
#include "dev_mpdu.h"

namespace Ui {
class Home_LineUnitWid;
}

class Home_LineUnitWid : public QWidget
{
    Q_OBJECT

public:
    explicit Home_LineUnitWid(QWidget *parent = nullptr);
    ~Home_LineUnitWid();

     void init(sDevData *dev);
     void updateData();

private:
    Ui::Home_LineUnitWid *ui;
    sDevData *mDev;
};

#endif // HOME_THUNITWID_H
