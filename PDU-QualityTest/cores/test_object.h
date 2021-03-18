#ifndef TEST_OBJECT_H
#define TEST_OBJECT_H

#include "sn_serialnum.h"

class Test_Object : public QThread
{
    Q_OBJECT
public:
    explicit Test_Object(QObject *parent = nullptr);
    ~Test_Object();

protected:
    void updateDev();

protected slots:
    virtual void initFunSlot(){}

protected:
    bool isRun;
    sDevType *mDt;
    sDevData *mDev;
    sCfgItem *mItem;
    sProgress *mPro;
    Dev_Object *mObj;
    sDataPacket *mPacket;
};

#endif // TEST_OBJECT_H
