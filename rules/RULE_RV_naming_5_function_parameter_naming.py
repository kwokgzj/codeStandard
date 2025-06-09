"""
函数参数必须使用小驼峰命名法。

== 违规示例 ==

    void function1(int First_param);     // 违规：参数名不是小驼峰
    int calculate(int A, int B_value);   // 违规：参数名不是小驼峰
    void process(int m_value);           // 违规：参数名不能使用m_前缀

== 正确示例 ==

    void function1(int firstParam);      // 正确：使用小驼峰
    int calculate(int valueA, int tempValue); // 正确：使用小驼峰
    void process(int inputValue);        // 正确：使用小驼峰

"""
import nsiqcppstyle_reporter
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
import util.review_util as rv


def RunRule(lexer, fullName, decl, contextStack, context):
    # 查找左括号
    lexer.GetNextTokenInType("LPAREN", False, True)

    # 保存当前位置
    lexer.PushTokenIndex()
    rparen = lexer.GetNextMatchingToken()
    lexer.PopTokenIndex()

    # 跳过左括号
    t = lexer.GetNextToken()

    while t != rparen:
        t = lexer.GetNextToken(True, True, True, True)

        # 检查参数名称
        if t.type == "ID":
            param_name = t.value

            # 检查是否符合小驼峰命名
            if not rv.is_camel_case(param_name):
                nsiqcppstyle_reporter.Error(t, __name__,
                                            f"函数 {fullName} 的参数 '{param_name}' 必须使用小驼峰命名法")


ruleManager.AddFunctionNameRule(RunRule)
