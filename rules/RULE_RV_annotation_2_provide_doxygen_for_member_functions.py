"""
检查公共成员函数必须有文档注释。
该规则要求每个类的公共成员函数定义前必须有 doxygen 风格的注释。

== 违规 ==

    class A {
    public:
        void PublicMethod() { } // 违规：没有注释的公共方法
    };

== 正确 ==

    class A {
    public:
        /**
         * 这是一个公共方法的说明
         */
        void PublicMethod() { } // 正确
    };
"""
import nsiqcppstyle_reporter
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *


def RunRule(lexer, fullName, decl, contextStack, context):
    if not decl:
        return

    if contextStack.SigPeek() is None:
        return

    t = lexer.GetCurToken()
    if IsConstructor(t.value, fullName, contextStack.SigPeek()) or IsOperator(t.value):
        return

    upperBlock = contextStack.SigPeek()
    if upperBlock.additional == "PUBLIC":
        lexer.PushTokenIndex()
        t2 = lexer.GetPrevTokenInType("COMMENT")
        t3 = lexer.GetPrevTokenInTypeList(["LBRACE", "SEMI", "PREPROCESSOR"], False, True)
        lexer.PopTokenIndex()

        if t2 is None or (t3 is not None and t2.lexpos < t3.lexpos):
            nsiqcppstyle_reporter.Error(t, __name__,
                                        f"公共成员函数 '{fullName}' 缺少注释")
            return

        if t2.additional not in ["DOXYGEN_JAVADOC", "DOXYGEN_QT", "DOXYGEN_CPP"]:
            nsiqcppstyle_reporter.Error(t, __name__,
                                        f"公共成员函数 '{fullName}' 的注释必须是doxygen格式")


def RunTypeScopeRule(lexer, contextStack):
    t = lexer.GetCurToken()
    if t.type in ["PUBLIC", "PRIVATE", "PROTECTED"]:
        curContext = contextStack.SigPeek()
        if curContext.type in ["CLASS_BLOCK", "STRUCT_BLOCK"]:
            curContext.additional = t.type


ruleManager.AddFunctionNameRule(RunRule)
ruleManager.AddTypeScopeRule(RunTypeScopeRule)