#ifndef TEST_CORETHREAD_H
#define TEST_CORETHREAD_H

#include "test_network.h"

class Test_CoreThread : public Test_Object
{
    Q_OBJECT
public:
    explicit Test_CoreThread(QObject *parent = nullptr);

protected:
    void run();
    void workDown();
    bool checkNet();
    bool startProcess();
    void workResult(bool res);
    void openAllSwitch();

protected slots:
    void initFunSlot();
    void getVersionSlot(QString str);
    void getMacSlot(QString str);
private:
    Test_Logs *mLogs;
    Sn_SerialNum *mSn;
    Test_NetWork *mRead;
    QProcess *mProcess;
    QString mVersion;
    QString mMacStr;
};

#endif // TEST_CORETHREAD_H
