/*
 * 测试变量命名规范
 * - 局部变量：小驼峰
 * - 类成员变量：m_前缀 + 小驼峰
 * - 全局变量：g_前缀 + 小驼峰
 */

// 测试1：全局变量
int g_userCount = 0;        // 正确
float g_maxValue = 100.0f;  // 正确
bool userFlag;              // 错误：缺少g_前缀
int g_MAX_VALUE;           // 错误：不是小驼峰

// 测试2：类定义
class TestClass {
    int m_memberCount;      // 正确
    float m_totalValue;     // 正确
    bool isValid;           // 错误：缺少m_前缀
    int m_CACHE_SIZE;      // 错误：不是小驼峰
};

// 测试3：函数中的局部变量
void testFunction() {
    if(true) {
        int localCounter = 0;}
    int localCounter;       // 正确
    float tempValue;        // 正确
    bool m_isValid;        // 错误：局部变量不应使用m_前缀
    int g_count;           // 错误：局部变量不应使用g_前缀
    int User_Name;         // 错误：不是小驼峰
}

// 测试4：复杂场景
class ComplexClass {
private:
    int m_itemCount;       // 正确
    float m_averageValue;  // 正确

    void calculate(int AAA) {
        int tempResult;    // 正确
        bool g_flag;       // 错误：局部变量不应使用g_前缀
        int m_temp;        // 错误：局部变量不应使用m_前缀
       }
    };

// 测试5：带数字的变量名
int g_value2D;             // 正确
float m_data3d;
int temp2Value;