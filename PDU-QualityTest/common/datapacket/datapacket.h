#ifndef DATAPACKET_H
#define DATAPACKET_H
#include <QtCore>
#include <QColor>

#define LINE_NUM  3
#define PACK_ARRAY_SIZE LINE_NUM
#define OpSize  6
#define ZpduOpSize 48


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
    sUnitCfg loopcur; // 回路电流
    sUnitCfg opCur[OpSize]; // 输出位电流
    sUnitCfg zpduopCur[ZpduOpSize]; // 输出位电流

    sUnitCfg tem; // 温度
    sUnitCfg hum; // 湿度
    float ratedVol;// 额定电压
};

struct sDevType
{
    sDevType(){ac=1;}
    uchar devType; // 1 ZPDU执行板类型  2 MPDU执行板类型   3 RPDU执行板类型
    // 4 SI-PDU  5 IP-PDU  6 BM-PDU

    uchar ac;
    uchar series; // 1 A系列  2 B系列  3 C系列  4 D系列1

    uchar loops;

    uchar modbus;

    uchar log_en;
    uchar envbox;
    uchar boards;
    uchar ip_lcd;
    uchar mpdu_ver;
    uchar zpdu_ver;
    uchar board[6];
    uchar loop[6];
    uchar security;
    uchar popup;
    QString versions;

    uchar outputs;
    uchar version;
    uchar language;
    uchar lines;// 1 单相     2 单相两路/双火线  3 三相
    uchar breaker;//0 16A, 1 20A
    uchar level;//垂直、水平
    uchar standar;//标准、中性
    uchar line_op[3];
    uchar loop_op[6];
    uchar loop_smallloop[6];
    uchar devZpduType;//1-20

    uchar rated_voltage;//0:220 , 1:380
    uchar rated_current;//0:16 , 1:32 , 2:63
    QString rated_frequency;//50
    QString type;//型号:ZZIF-130-2004
    QString hw_version;//A
    QString protocol_version;//196608
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
    Test_Manual,
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
    sDevData *getZpdu() {return zpdu;}
    sProgress *getPro() {return pro;}

    bool updatePro(const QString &str, bool pass=true, int sec=1);
    bool delay(int s=1);
private:
    sDevData *mpdu;
    sDevData *zpdu;
    sProgress *pro;
};



#endif // DATAPACKET_H
