"""
Braces for class, struct, enum, function and namespace should be located in a new line.

== Violation ==

    class MyClass { <== ERROR
        int x;
    };

    struct MyStruct { <== ERROR
        int y;
    };

    enum Color { <== ERROR
        RED,
        GREEN
    };

    void MyFunction() { <== ERROR
        int z;
    }

    namespace MyNamespace { <== ERROR
        int k;
    }

== Good ==

    class MyClass
    { <== OK
        int x;
    };

    struct MyStruct
    { <== OK
        int y;
    };

    enum Color
    { <== OK
        RED,
        GREEN
    };

    void MyFunction()
    { <== OK
        int z;
    }

    namespace MyNamespace
    { <== OK
        int k;
    }
"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *

"""
函数起始花括号{ 需要单独一行
"""
def functionRunRule(lexer, fullName, decl, contextStack, typeContext):
    if not decl and typeContext is not None:
        t = lexer.GetNextTokenInType("LBRACE", False, True)
        if t is not None:
            t2 = typeContext.endToken
            if t2 is not None and t.lineno != t2.lineno:
                prevToken = lexer.GetPrevTokenSkipWhiteSpaceAndCommentAndPreprocess()
                # print contextStack.Peek()
                if prevToken is not None and prevToken.lineno == t.lineno:
                    nsiqcppstyle_reporter.Error(
                        t,
                        __name__,
                        f"函数 '{fullName}' 的左花括号需要单独一行",
                    )


ruleManager.AddFunctionNameRule(functionRunRule)

"""
类，结构体，枚举类型，命名空间的起始花括号{ 需要单独一行
"""
def typeRunRule(lexer, currentType, fullName, decl, contextStack, typeContext):
    if not decl and currentType != "NAMESPACE" and typeContext is not None:
        t = lexer.GetNextTokenInType("LBRACE", False, True)
        if t is not None:
            t2 = typeContext.endToken
            if t2 is not None and t.lineno != t2.lineno:
                prevToken = lexer.GetPrevTokenSkipWhiteSpaceAndCommentAndPreprocess()
                # print contextStack.Peek()
                if prevToken is not None and prevToken.lineno == t.lineno:
                    nsiqcppstyle_reporter.Error(
                        t,
                        __name__,
                        f"'{fullName}' 的左花括号需要单独一行",
                    )
                # if t2.lineno != t.lineno and GetRealColumn(t2) != GetRealColumn(t):
                #     nsiqcppstyle_reporter.Error(
                #         t2,
                #         __name__,
                #         "The brace for type definition should be located in same column",
                #     )


ruleManager.AddTypeNameRule(typeRunRule)

"""
条件和循环语句（switch，try等）与左花括号同一行
"""
def controlRunRule(lexer, contextStack):
    t = lexer.GetCurToken()
    contextStack.SigPeek()

    # 识别控制语句关键字
    if t.type in ["IF", "ELSE", "FOR", "WHILE", "SWITCH", "TRY", "DO"]:
        next_token = lexer.GetNextTokenInType("LBRACE", False, True)
        if t is not None:
            if next_token.lineno != t.lineno:
                nsiqcppstyle_reporter.Error(
                    t,
                    __name__,
                    f"左花括号要与 '{t.value}' 在同一行",
                )

ruleManager.AddFunctionScopeRule(controlRunRule)

"""
右花括号单独一行
"""
def RightBraceRule(lexer, contextStack):
    t = lexer.GetCurToken()

    # 检查是否为右花括号
    if t.type == "RBRACE":
        # 获取同一行前面的非注释token
        prev_token = lexer.GetPrevTokenSkipWhiteSpaceAndCommentAndPreprocess()

        # 如果前面有token且在同一行(排除左花括号和注释的情况)
        if prev_token and prev_token.lineno == t.lineno and prev_token.type != "LBRACE":
            nsiqcppstyle_reporter.Error(
                t,
                __name__,
                "右花括号必须单独一行"
            )


# ruleManager.AddFunctionScopeRule(RightBraceRule)
ruleManager.AddRule(RightBraceRule)

