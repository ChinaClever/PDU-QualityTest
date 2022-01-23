#ifndef HOME_ZPDUSETWID_H
#define HOME_ZPDUSETWID_H

#include <QWidget>
#include "common.h"
#include "home_zpdualarmwid.h"
#include <QComboBox>

namespace Ui {
class Home_ZpduSetWid;
}

class Home_ZpduSetWid : public QWidget
{
    Q_OBJECT

public:
    explicit Home_ZpduSetWid(QWidget *parent = nullptr);
    ~Home_ZpduSetWid();
    void updateData();

protected slots:
    void initFunSlot();

private:
    void initData();
    void initWid();

private:
    Ui::Home_ZpduSetWid *ui;
    sCfgItem *mItem;
    Dev_Object *mObj;
    sDevData *mDev;
    QList<QComboBox*> mListWid;
};

#endif // HOME_ZPDUSETWID_H
