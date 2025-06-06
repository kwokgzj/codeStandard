/*
 * 文件名：naming_1_A_class_naming_test.cpp
 * 功能：测试类命名规则
 * 规则：RULE_RV_naming_1_A_class_naming_pascalcase_noprefixes
 * 正确命名数量：1
 * 违反命名数量：5
 */

// 1. 类命名符合大驼峰命名法（PascalCase）
class MyClass {
};

// 2. 类命名包含下划线
class TMy_Class {
};

// 3. 类命名以小写字母开头
class myclass {
};

// 4. 类命名包含数字
class MyClass1 {
};

// 5. 类命名包含特殊字符
class MyClass$ {
};

// 6. 类命名包含中文字符
class 我的类 {
};
