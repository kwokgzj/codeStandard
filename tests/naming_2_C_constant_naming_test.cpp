/*
 * 测试常量命名规范
 * - 必须全部大写
 * - 使用下划线分隔单词
 */

// 测试1：基本常量定义
const int MAX_VALUE = 100;          // 正确
const float PI = 3.14;              // 正确
const char PATH_SEPARATOR = '/';     // 正确

// 测试2：错误的常量命名
const int maxValue = 200;           // 错误：小驼峰
const double Pi = 3.14159;          // 错误：首字母大写
const int MAXSPEED = 120;           // 错误：缺少下划线

// 测试3：static const 常量
static const int BUFFER_SIZE = 1024;        // 正确
static const char DEFAULT_NAME[] = "test";  // 正确
static const int MinValue = 0;              // 错误：非全大写

// 测试4：constexpr 常量
constexpr int ARRAY_LENGTH = 256;           // 正确
constexpr double GOLDEN_RATIO = 1.618;      // 正确
constexpr int invalidValue = -1;            // 错误：小写

// 测试5：带数字的常量命名
const int HTTP_PORT_80 = 80;                // 正确
const int MAX_RETRY_3_TIMES = 3;            // 正确
const int Error404 = 404;                   // 错误：数字没有用下划线分隔

// 测试6：类中的常量
class TestClass {
    static const int CLASS_VERSION = 1;      // 正确
    static const int kClassId = 100;        // 错误：使用k前缀
    const int defaultValue = 0;             // 错误：小写
};

// 测试7：命名空间中的常量
namespace test {
    const int CONFIG_VERSION = 2;           // 正确
    const char* DB_CONNECTION = "mysql";    // 正确
    const int MaxConnections = 10;          // 错误：非全大写
}