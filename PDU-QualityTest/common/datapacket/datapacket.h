#ifndef DATAPACKET_H
#define DATAPACKET_H
#include <QtCore>
#include <QColor>

#define LINE_NUM  3
#define PACK_ARRAY_SIZE LINE_NUM
#define OpSize  6


/**
 * 数据单元：包括当前值，阈值，临界值，告警状态等
 */
struct sDataUnit
{
    sDataUnit() {size=0;}

    ushort size;
    ushort value[PACK_ARRAY_SIZE]; // 值
    ushort min[PACK_ARRAY_SIZE]; // 最小值
    ushort max[PACK_ARRAY_SIZE]; // 最大值
    uchar alarm[PACK_ARRAY_SIZE]; // 报警值 0表示未报警  1表示已报警 2表示已记录
    uchar status[PACK_ARRAY_SIZE];
};



/**
 * 数据对象：包括电流，电压，功率，电能，开关状态，插接位名称
 */
struct sObjData
{
    sObjData() {size=0;}
    int size;
    sDataUnit vol; // 电压
    sDataUnit cur; // 电流
    sDataUnit tem; // 温度
    sDataUnit hum; // 湿度

    ushort pow[PACK_ARRAY_SIZE]; // 功率
    uint ele[PACK_ARRAY_SIZE]; // 电能

    uchar pf[PACK_ARRAY_SIZE]; // 功率因数
    uchar sw[PACK_ARRAY_SIZE]; // 开关状态 0 表示未启用
    ushort aPow[PACK_ARRAY_SIZE]; // 视在功率值

    uchar hz; // 电压频率
    ushort br;  // 00	表示波特率9600(00默认9600，01为4800，02为9600，03为19200，04为38400)
};

/**
 * 数据单元：包括当前值，阈值，临界值，告警状态等
 */
struct sUnitCfg
{
    uchar en;
    uchar id;
    float min; // 最小值
    float max; // 最大值

    float crMin; // 最小值
    float crMax; // 最大值
};



/**
 * 数据对象：包括电流，电压，功率，电能，开关状态，插接位名称
 */
struct sObjCfg
{
    sUnitCfg vol; // 电压
    sUnitCfg cur; // 电流
    sUnitCfg output; // 电流
    sUnitCfg opCur[OpSize]; // 输出位电流

    sUnitCfg tem; // 温度
    sUnitCfg hum; // 湿度
};

struct sDevType
{
    sDevType(){ac=1;}
    uchar devType; // 1 ZPDU执行板类型  2 MPDU执行板类型   3 RPDU执行板类型
    // 4 SI-PDU  5 IP-PDU  6 BM-PDU

    uchar ac;
    uchar series; // 1 A系列  2 B系列  3 C系列  4 D系列1
    uchar lines;
    uchar loops;
    uchar outputs;
    uchar breaker;
    uchar language;
    uchar modbus;
    uchar standar;
    uchar version;
    uchar log_en;
    uchar envbox;
    uchar boards;
    uchar level;
    uchar mpdu_ver;
    uchar board[3];
    uchar loop[6];
    uchar ip_lcd;
    uchar security;

    QString versions;
};



/**
 * 设备数据结构体：
 */
struct sDevData
{
    sDevType dt; //设备类型
    sObjCfg cfg; // MPDU配置数据
    sObjData data;
};


enum {
    Test_Fun, // 功能
    Test_Start, // 开始
    Test_vert, // 验证
    Test_Over, // 终止
    Test_End, // 完成

    Test_Info=0,
    Test_Pass=1,
    Test_Fail=2,
};

struct sProgress
{
    sProgress() {step=0;}

    uchar step; // 步骤
    QString time;
    QList<bool> pass, itPass;
    QStringList status, item;

    uchar result;    // 最终结果
    QTime startTime;
};


/**
 * 数据包
 */
class sDataPacket
{
    sDataPacket();
public:
    static sDataPacket *bulid();

    void init();
    sDevData *getMpdu() {return mpdu;}
    sProgress *getPro() {return pro;}

    bool updatePro(const QString &str, bool pass=true, int sec=1);
    bool delay(int s=1);
private:
    sDevData *mpdu;
    sProgress *pro;
};



#endif // DATAPACKET_H
