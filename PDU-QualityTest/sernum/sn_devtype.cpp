/*
 *
 *  Created on: 2021年1月1日
 *      Author: Lzy
 */
#include "sn_devtype.h"
#include "common/json/json_build.h"
#include "common/json/json_recv.h"

Sn_DevType::Sn_DevType()
{
    QJsonObject json;
    Json_Build::bulid()->getJson(json);
    Json_Recv::bulid()->recv("pdu_id");
}

Sn_DevType * Sn_DevType::bulid()
{
    static  Sn_DevType* sington = nullptr;
    if(sington == nullptr)
        sington = new  Sn_DevType();
    return sington;
}

QString Sn_DevType::getMpdu(uint id)
{
    QString str;
    if(2 == (id >> 12)) {
        str += "MPDU主控";
        if((id >> 11) & 1) str += "_二期"; else str += "_一期";
        if((id >> 10) & 1) str += "_三相"; else str += "_单相";
        str += QObject::tr("_%1回路").arg((id >> 6) & 0xF);
        str += QObject::tr("_%1输出位").arg(id & 0x3F);
    }
    return  str;
}


QString Sn_DevType::getDevStr(uint id)
{
    QString res = getMpdu(id);
    if(res.isEmpty()) {
        res = Json_Recv::bulid()->getDevTypeByID(id);
    }

    return res;
}


bool Sn_DevType::analysDevType(uint id)
{
    bool ret = true;
    QString str = getDevStr(id);
    if(str.size()) {
        Cfg::bulid()->item->dev_type = str;
    } else {
        ret = false;
    }

    return ret;
}

