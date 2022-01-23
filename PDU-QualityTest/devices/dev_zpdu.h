#ifndef DEV_ZPDU_H
#define DEV_ZPDU_H
#include "dev_object.h"

class Dev_Zpdu : public Dev_Object
{
    explicit Dev_Zpdu(QObject *parent = nullptr);
public:
    static Dev_Zpdu *bulid(QObject *parent = nullptr);

    void save();
    void savePopup(bool en);

protected:
    QString cfgGroup(){return "zCfg";}

    void initSetHtml();
    void initDebugHtml();
    void initData();
    void initCfg();

    void writeSetHtml();
    void writeDebugHtml();
    void writeData();
    void initUnitV(const QString& prefix, sUnitCfg &unit);
    void initUnitC(const QString& prefix, sUnitCfg &unit);
    void initUnitT(const QString& prefix, sUnitCfg &unit);
    void initUnitH(const QString& prefix, sUnitCfg &unit);
};

#endif // DEV_ZPDU_H
