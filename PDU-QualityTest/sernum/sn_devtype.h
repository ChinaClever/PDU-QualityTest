#ifndef DEV_DEFTYPE_H
#define DEV_DEFTYPE_H
#include "sn_object.h"

class Sn_DevType
{
    Sn_DevType();
public:
    static Sn_DevType *bulid();
    bool analysDevType(uint id);

protected:
    QString getDevStr(uint id);
    QString getMpdu(uint id);

};

#endif // DEV_DEFTYPE_H
