/*
 * 文件名：naming_1_C_enum_naming_test.cpp
 * 功能：测试枚举命名规则
 * 规则：RULE_RV_naming_1_C_enum_naming_pascalcase_noprefixes
 * 正确命名数量：1
 * 违反命名数量：5
 */

// 1. 枚举命名符合大驼峰命名法（PascalCase）
enum MyEnum {
    VALUE1,
    VALUE2
};

// 2. 枚举命名包含下划线
enum e_MyEnum {
    VALUE1,
    VALUE2
};

// 3. 枚举命名以小写字母开头
enum myenum {
    VALUE1,
    VALUE2
};

// 4. 枚举命名包含数字
enum MyEnum1 {
    VALUE1,
    VALUE2
};

// 5. 枚举命名包含特殊字符
enum MyEnum$ {
    VALUE1,
    VALUE2
};

// 6. 枚举命名包含中文字符
enum 我的枚举 {
    VALUE1,
    VALUE2
};

int main() {
    return 0;
}
