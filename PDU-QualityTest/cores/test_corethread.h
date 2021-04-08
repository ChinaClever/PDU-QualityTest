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
    bool manualConfirmBox(QString &str);

protected slots:
    void initFunSlot();
    bool manualConfirmSlot();

private:
    Test_Logs *mLogs;
    Sn_SerialNum *mSn;
    Test_NetWork *mRead;
    QProcess *mProcess;
};

#endif // TEST_CORETHREAD_H
