#ifndef HOME_SETOPDLG_H
#define HOME_SETOPDLG_H

#include <QDialog>
#include "home_outputwid.h"

namespace Ui {
class Home_SetOpDlg;
}

class Home_SetOpDlg : public QDialog
{
    Q_OBJECT

public:
    explicit Home_SetOpDlg(QWidget *parent = nullptr);
    ~Home_SetOpDlg();

    void updateIndex(int id);

private slots:
    void on_okBtn_clicked();
    void on_saveBtn_clicked();

private:
    Ui::Home_SetOpDlg *ui;
    Dev_Object *mDev;
    Home_OutputWid *mOutputWid;
};

#endif // HOME_SETOPDLG_H
