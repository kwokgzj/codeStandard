/*
 * 文件名：naming_1_B_struct_naming_test.cpp
 * 功能：测试结构体命名规则
 * 规则：RULE_RV_naming_1_B_struct_naming_pascalcase_noprefixes
 * 正确命名数量：1
 * 违反命名数量：5
 */

// 1. 结构体命名符合大驼峰命名法（PascalCase）
struct MyStruct {
    int x;
    int y;
};

// 2. 结构体命名包含下划线
struct s_MyStruct {
    int x;
    int y;
};

// 3. 结构体命名以小写字母开头
struct mystruct {
    int x;
    int y;
};

// 4. 结构体命名包含数字
struct MyStruct1 {
    int x;
    int y;
};

// 5. 结构体命名包含特殊字符
struct MyStruct$ {
    int x;
    int y;
};

// 6. 结构体命名包含中文字符
struct 我的结构体 {
    int x;
    int y;
};

int main() {
    return 0;
}
