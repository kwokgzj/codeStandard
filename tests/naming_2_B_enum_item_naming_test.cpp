/*
 * 测试枚举值命名规范
 * - 必须全部大写
 * - 使用下划线分隔单词
 */

// 测试1：正确的枚举值命名
enum Color {
    RED,              // 正确：单个单词全大写
    DARK_BLUE,       // 正确：下划线分隔，全大写
    LIGHT_GREEN      // 正确：下划线分隔，全大写
};

// 测试2：错误的枚举值命名
enum Status {
    Ready,           // 错误：首字母大写，不是全大写
    NOT_ready,       // 错误：部分小写
    PROCESSING123,   // 错误：数字之前缺少下划线
    done            // 错误：全部小写
};

// 测试3：带赋值的枚举定义
enum ErrorCode {
    SUCCESS_CODE = 0,        // 正确：全大写+下划线
    error_not_found = 404,   // 错误：全部小写
    ERROR_SERVER500         // 错误：数字前缺少下划线
};

// 测试4：typedef 枚举定义
typedef enum {
    FIRST_ITEM,            // 正确
    secondItem,            // 错误：驼峰式，不是全大写
    THIRD_ITEM_123        // 正确：数字前有下划线
} TestEnum;

// 测试5：单行定义的枚举
enum Direction { LEFT, RIGHT, UP, DOWN };  // 正确：单个单词全大写

// 测试6：带前缀的枚举值（错误示例）
enum Prefix {
    kConstant,            // 错误：带k前缀，不是全大写
    mValue,              // 错误：带m前缀，不是全大写
    PREFIX_VALUE         // 正确
};

// 测试7：复杂命名场景
enum ComplexEnum {
    HTTP_GET_REQUEST,     // 正确
    HTTP_404_NOT_FOUND,   // 正确
    DB_ERROR_2_RETRY,    // 正确
    myError,             // 错误：不是全大写
    NOUNDERSCORE         // 错误：应该分词
};