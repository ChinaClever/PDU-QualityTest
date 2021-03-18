#ifndef DEV_OBJECT_H
#define DEV_OBJECT_H

#include "rtu_modbus.h"

class Dev_Object : public QThread
{
    Q_OBJECT
public:
    explicit Dev_Object(QObject *parent = nullptr);
    sDevData *getDev() {return mDev;}

    virtual void save()=0;

protected:
    virtual QString cfgGroup()=0;
    void initUnit(const QString& prefix, sUnitCfg &unit, int f=0);
    void writeUnit(const QString& prefix, sUnitCfg &unit, int f=0);

    void write(const QString &key, const QVariant& v);
    QVariant read(const QString &key, const QVariant &v = QVariant());

    uchar *toInt(uchar *ptr, int line, uint *value);
    uchar *toChar(uchar *ptr, int line, uchar *value);
    uchar *toShort(uchar *ptr, int line, ushort *value);

    ushort getShort(uchar *ptr);
    uchar *getShort(uchar *ptr, int line, uchar *value);
    uchar *toOutputEle(uchar *ptr, int line, uint *value);
    uchar *toThreshold(uchar *ptr, int line, sDataUnit &unit);
    uchar *toEnvTh(uchar *ptr, sDataUnit &unit);

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

#endif // DEV_OBJECT_H
