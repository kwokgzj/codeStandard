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
    if not decl:
        return
    # 查找左括号
    lexer.GetNextTokenInType("LPAREN", False, True)

    # 保存当前位置
    lexer.PushTokenIndex()
    rparen = lexer.GetNextMatchingToken()
    lexer.PopTokenIndex()

    # 跳过左括号
    t = lexer.GetNextToken()

    while t != rparen:
        # 记录最后一个标识符
        last_id = None

        # 读取直到遇到逗号或右括号
        while t != rparen and t.type != "COMMA":
            if t.type == "ID":
                last_id = t
            t = lexer.GetNextToken(True, True, True, True)

        # 检查最后一个标识符（即参数名）
        if last_id and not rv.is_camel_case(last_id.value):
            nsiqcppstyle_reporter.Error(last_id, __name__,
                                        f"参数 '{last_id.value}' 必须使用小驼峰命名法")

        # 如果遇到逗号，继续处理下一个参数
        if t.type == "COMMA":
            t = lexer.GetNextToken(True, True, True, True)


ruleManager.AddFunctionNameRule(RunRule)
