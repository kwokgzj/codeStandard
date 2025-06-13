"""
函数名必须使用小驼峰命名法。

== 违规示例 ==

    void HelloWorld() {      // 违规：首字母大写
        ...
    }

    void My_Function() {     // 违规：包含下划线
        ...
    }

    void DOSOMETHING() {     // 违规：全大写
        ...
    }

== 正确示例 ==

    void sayHello() {        // 正确：小驼峰命名
        ...
    }

    void calculateSum() {    // 正确：小驼峰命名
        ...
    }

    // 例外情况：构造函数、析构函数和运算符重载函数
    class MyClass {
        MyClass();           // 正确：构造函数可以使用大写
        ~MyClass();          // 正确：析构函数可以使用大写
        operator+();         // 正确：运算符重载
    };
"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *
import util.review_util as rv


def RunRule(lexer, fullName, decl, contextStack, context):
    if not decl:
        return
    t = lexer.GetCurToken()
    value = t.value

    # 跳过构造函数和析构函数
    if IsConstructor(value, fullName, contextStack.SigPeek()):
        return

    # 跳过运算符重载函数
    if IsOperator(value):
        return

    # 检查是否符合小驼峰命名规则
    if not rv.is_camel_case(value):
        nsiqcppstyle_reporter.Error(t, __name__,
                                    f"函数名 '{value}' 必须使用小驼峰命名法")


ruleManager.AddFunctionNameRule(RunRule)
