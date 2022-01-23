#ifndef SN_OBJECT_H
#define SN_OBJECT_H

#include "dev_mpdu.h"
#include "dev_zpdu.h"

class Sn_Object : public QThread
{
    Q_OBJECT
public:
    explicit Sn_Object(QObject *parent = nullptr);

    void initDev();

protected slots:
    virtual void initFunSlot();

protected:
    sDevType *mDt;
    sDevData *mDev;
    RtuRw *mModbus;
    sCfgItem *mItem;
    sProgress *mPro;
    sDataPacket *mPacket;
};

#endif // SN_OBJECT_H
