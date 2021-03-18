#ifndef DEV_MPDU_H
#define DEV_MPDU_H

#include "dev_object.h"

class Dev_Mpdu : public Dev_Object
{
    Q_OBJECT
    explicit Dev_Mpdu(QObject *parent = nullptr);
public:
    static Dev_Mpdu *bulid(QObject *parent = nullptr);

    void save();

protected:
    QString cfgGroup(){return "mCfg";}

    void initType();
    void initData();
    void initCfg();

    void writeType();
    void writeData();
};

#endif // DEV_MPDU_H
