/**
 * @file MainWindow.cpp
 * @author xiexingfeng (79415969@qq.com)
 * @brief
 * @version 0.1
 * @date 2025-02-13
 *
 * @copyright Copyright (c) 2014-2025 Revopoint 3D Technologies Inc. All rights reserved
 *
 */
#include "MainWindow.h"
#include "3drender/RenderUtil.h"
#include "log/RvDebug.h"

#include "../../rvscan/include/rvscan/ScanEvent.h"
#include "../document/RvPointCloudDocument.h"
#include "../renderer/RvMeshRenderer.h"
#include "../renderer/RvPointCloudRenderer.h"
#include "../renderer/RvRenderWidget.h"
#include "rvcore/IRvRenderer.h"
#include "rvcore/language/LanguageMgr.h"

#include "../camera/CameraViewPanel.h"
#include "../fileExplorer/FileTopPanel.h"
#include "../modelList/ModelListPanel.h"
#include "3drender/VisualManager.h"
#include "src/renderer/RvRenderContainer.h"

#include "../projects/RvProjectGroup.h"
#include "language.h"

#include "rvcore/CoreEvent.h"

#include <qboxlayout.h>
#include <qicon.h>
#include <qlogging.h>
#include <qnamespace.h>
#include <qsizegrip.h>
#include <qsizepolicy.h>
#include <qstackedwidget.h>
#include <qwidget.h>
#include <QApplication>
#include <QDockWidget>
#include <QFrame>
#include <QLayout>
#include <QMoveEvent>
#include <QPushButton>
#include <QStackedWidget>
#include <QStatusBar>
#include <QTabBar>
#include <QToolBar>
#include <QWidget>
#include <cstddef>

#include <service/event/ctkEventConstants.h>

#include "../search/SearchManager.h"
#define LAN_GEOMETRIC_RICHNESS_TIP		QObject::tr("拼接宽容度指的是扫描时对扫描对象几何特征复杂性的要求程度，拼接宽容度越低，对扫描对象的几何特征要求越严格，适用于扫描几何特征复杂的物体，比如雕塑，高端折纸等；拼接宽容度越高，对扫描对象的几何特征要求越宽容，适用于几何扫描特征简单的对象，比如马克杯，手等。")
/*
 * 测试函数命名规则
 * - 必须使用小驼峰命名法
 * - 构造函数、析构函数和运算符重载函数除外
 */
static const QMap<ScanObject, int> g_objectPriorityMap = { { ScanObject::SCAN_OBJECT_GENERAL, 0 }, { ScanObject::SCAN_OBJECT_DARK, 1 },
                                                           { ScanObject::SCAN_OBJECT_FACE, 2 },    { ScanObject::SCAN_OBJECT_HEAD, 3 },
                                                           { ScanObject::SCAN_OBJECT_BODY, 4 },    { ScanObject::SCAN_OBJECT_BODY_LARGE, 5 },
                                                           { ScanObject::SCAN_OBJECT_LARGE, 6 } };

void sayHello();

#include <iostream>
using namespace std;

const //dfdf
 aa::int GLOBAL_CONST = 100;
namespace rv
{
class MyClass {
public:
    const int CLASS_CONST; // 类成员常量
    MyClass( int val) : CLASS_CONST(val) {} // 构造函数初始化类成员常量
};

int main() { // 3. 局部作用域常量
const int LOCAL_CONST = 50;

MyClass obj(200);

int a = 10;
int b = 20;

const int* ptr1 = &a;       // 指向常量的指针（指针可以改变，指向的内容不能改）
int* const ptr2 = &b;       // 常量指针（指针不能改变，指向的内容可以改）
    const int*
    const ptr3 = &a; // 指向常量的常量指针（指针和内容都不能改）

return 0;
}

enum EnumGroupInfoRoles
{
    DefaultConfigRole = Qt::UserRole + 1,
};


class XAPIAN_VISIBILITY_DEFAULT RSet {
    explicit GroupInfoModel(const QList<GroupInfo>& itemList, QObject *parent = nullptr);
}

// 测试1：正确的函数命名
void sayHello() {              // 正确：小驼峰
    setStyleSheet(R"(
            background-color: #474747;
            border-radius: 8px;
            padding: 12px;
        )");
    if(true)
        int temp = 0;
}

void calculateSum() {          // 正确：小驼峰
}

int getValue() {              // 正确：小驼峰
}

// 测试2：错误的函数命名
void HelloWorld() {           // 错误：首字母大写
}

void Do_Something() {         // 错误：包含下划线
}

void CALCULATE() {
            // 错误：全大写


}

void Pascal_Case_Wrong() {    // 错误：Pascal命名法



}

void ProjectInfoIconDelegate::drawProjectSizeAndTime(QPainter *painter, const QStyleOptionViewItem &option, const QModelIndex &index) const
{
    QRect sizeRect = getRect(option, rvcore::PROJECT_SIZE);

    // 设置字体；
    QFont font;
    font.setPixelSize(14);
    painter->setFont(font);
    painter->setPen(QColor("#FFFFFF"));

    QString sizeStr = "--";
    auto size = index.data(Qt::UserRole).value<rvcore::ProjectModelInfo>().byteSize;
    if (size >= 0) {
        sizeStr = bytesToString(size);
    }
    // 绘制size;
    painter->drawText(sizeRect, Qt::AlignLeft | Qt::AlignVCenter, sizeStr);

    // 绘制split
    QFontMetrics fontMetrics = painter->fontMetrics();
    const int txtWidth = fontMetrics.boundingRect(sizeStr).width();
    const int splitHeight = fontMetrics.boundingRect(sizeStr).height() - 8;
    QRect splitRect = QRect(sizeRect.x() + txtWidth + 8, sizeRect.y() + (sizeRect.height() - splitHeight) / 2 + 1, 1, splitHeight);
    painter->fillRect(splitRect, QColor("#FFFFFF"));

    QDateTime dateTime = QDateTime::fromSecsSinceEpoch(index.data(Qt::UserRole).value<rvcore::ProjectModelInfo>().modifyTime);
    // 绘制time
    QRect timeRect = QRect(splitRect.x() + splitRect.width() + 8, sizeRect.y(), 1, sizeRect.height());
    timeRect.setWidth(sizeRect.x() + (sizeRect.width() - timeRect.x()));
    painter->drawText(timeRect, Qt::AlignLeft | Qt::AlignVCenter, QLocale().toString(dateTime, QLocale::ShortFormat));
}

class QWidget *MainWindow::setContainer(class QWidget *widget)
{
    QWidget *currentWidget = m_centralWidget->currentWidget();
    if (widget != nullptr) {
        m_centralWidget->addWidget(widget);
        m_centralWidget->setCurrentWidget(widget);
    }
    return currentWidget;
}

// 测试3：类成员函数
class TestClass {
public:
    // 特殊函数（例外情况）
    TestClass() {}                    // 正确：构造函数
    ~TestClass() {}                   // 正确：析构函数
    operator+() {}                    // 正确：运算符重载
    operator-() {}                    // 正确：运算符重载

    // 普通成员函数
    void getData() {}                 // 正确：小驼峰
    void SetValue() {}               // 错误：首字母大写
    void PROCESS_DATA() {}           // 错误：全大写
    void handle_event() {}           // 错误：下划线
private:
    void init() {}                    // 正确：小驼峰
    void Init() {}                    // 错误：首字母大写
};

// 测试4：模板函数
template<typename T>
void processData() {                  // 正确：小驼峰
}

template<typename T>
void Process_Template(int anddj, int AAA) {            // 错误：下划线和大写
}

void PointCloudDisplay::resetPointColor(const std::vector<int> &pointIndices)
{
    setPointColor(pointIndices, 1);
}

// 测试5：命名空间中的函数
namespace MyNamespace {
    void initSystem() {              // 正确：小驼峰
}

    void Init_System() {             // 错误：下划线和大写
    }
}

// 测试6：静态函数
static void loadConfig() {           // 正确：小驼峰
}

static void Load_Config(int S, int JDKS, int jfk_fjdk) {          // 错误：下划线和大写
}

// 测试7：内联函数
inline void updateCache() {          // 正确：小驼峰
}

inline void Update_Cache() {         // 错误：下划线和大写
    if(true)
    {
        int temp = 0;}
}

// 测试8：友元函数
class Friend {
    friend void showFriend();        // 正确：小驼峰
    friend void Show_Friend();       // 错误：下划线和大写
};

// 测试9：虚函数
class Virtual {
    virtual void render() {}         // 正确：小驼峰
    virtual void Render() {}         // 错误：首字母大写

private:
    int m_value;              // 正确：类成员变量使用m_前缀 + 小驼峰
    /*
     * 类成员变量使用m_前缀 + 大驼峰
     */
    int m_value1;
    /**
     * @brief 是否激活;
     */
    bool m_isActive;
    /**
     * @brief 用户年龄
     */
    int m_age;
    /*
      这是一个多行注释
      用于描述成员变量
    */
    bool m_isEnabled;      /*这是一个多行注释用于描述成员变量*/
    bool m_isEnabled1;
};

// 测试10：纯虚函数
class Pure {
    virtual void draw() = 0;         // 正确：小驼峰
    virtual void Draw() = 0;         };
}