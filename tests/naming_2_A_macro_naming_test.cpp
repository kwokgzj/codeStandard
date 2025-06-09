/*
 * 文件名：naming_2_C_macro_naming_test.cpp
 * 功能：测试宏定义命名规则
 * 规则：RULE_RV_naming_2_C_macro_naming_allcaps_underscores
 * 正确命名数量：1
 * 违反命名数量：5
 */

// 1. 宏定义命名符合全大写+下划线命名法
#define MY_MACRO 1

// 2. 宏定义命名包含小写字母
#define my_macro 2

// 3. 宏定义命名包含数字
#define MY_MACRO1 3

// 4. 宏定义命名包含特殊字符
#define MY_MACRO$ 4

int main() {
    return 0;
}
