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

enum EnumGroupInfoRoles
{
    DefaultConfigRole = Qt::UserRole + 1,
};


class XAPIAN_VISIBILITY_DEFAULT RSet {
}

// 测试1：正确的函数命名
void sayHello() {              // 正确：小驼峰
    setStyleSheet(R"(
            background-color: #474747;
            border-radius: 8px;
            padding: 12px;
        )");
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
    if(true) {
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