"""
检查全局函数必须有文档注释。
该规则要求每个全局函数定义前必须有 doxygen 风格的注释。

== 违规 ==

    void GlobalFunction() { } // 违规：没有注释的全局函数

== 正确 ==

    /**
     * 这是一个全局函数的说明
     */
    void GlobalFunction() { } // 正确
"""
import nsiqcppstyle_reporter
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *


def RunRule(lexer, fullName, decl, contextStack, context):
    if decl:
        return

    # 只检查全局函数
    if contextStack.SigPeek() is not None:
        return

    t = lexer.GetCurToken()
    if IsOperator(t.value):
        return

    lexer.PushTokenIndex()
    t2 = lexer.GetPrevTokenInType("COMMENT")
    t3 = lexer.GetPrevTokenInTypeList(["LBRACE", "SEMI", "PREPROCESSOR"], False, True)
    lexer.PopTokenIndex()

    if t2 is None or (t3 is not None and t2.lexpos < t3.lexpos):
        nsiqcppstyle_reporter.Error(t, __name__,
                                    f"全局函数 '{fullName}' 缺少注释")
        return

    if t2.additional not in ["DOXYGEN_JAVADOC", "DOXYGEN_QT", "DOXYGEN_CPP"]:
        nsiqcppstyle_reporter.Error(t, __name__,
                                    f"全局函数 '{fullName}' 的注释必须是doxygen格式")


ruleManager.AddFunctionNameRule(RunRule)