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


def functionRunRule(lexer, contextStack):
    t = lexer.GetCurToken()
    if t.type == "LBRACE":
        prevToken = lexer.GetPrevTokenSkipWhiteSpaceAndCommentAndPreprocess()
        if prevToken is not None and prevToken.lineno == t.lineno and contextStack.Peek().type == "BRACEBLOCK":
            nsiqcppstyle_reporter.Error(
                t,
                __name__,
                f"函数的左花括号需要单独一行",
            )

ruleManager.AddFunctionScopeRule(functionRunRule)

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
                        f"{fullName} 声明的左花括号需要单独一行",
                    )
                # if t2.lineno != t.lineno and GetRealColumn(t2) != GetRealColumn(t):
                #     nsiqcppstyle_reporter.Error(
                #         t2,
                #         __name__,
                #         "The brace for type definition should be located in same column",
                #     )


ruleManager.AddTypeNameRule(typeRunRule)

# def namespaceRunRule(lexer, currentType, fullName, decl, contextStack, typeContext):
#     if not decl and currentType == "NAMESPACE" and typeContext is not None:
#         t = lexer.GetNextTokenInType("LBRACE", False, True)
#         if t is not None:
#             t2 = typeContext.endToken
#             if t2 is not None and t.lineno != t2.lineno:
#                 prevToken = lexer.GetPrevTokenSkipWhiteSpaceAndCommentAndPreprocess()
#                 # print contextStack.Peek()
#                 if prevToken is not None and prevToken.lineno == t.lineno:
#                     nsiqcppstyle_reporter.Error(
#                         t,
#                         __name__,
#                         "The brace for type definition should be located in start of line",
#                     )
#                 # if t2.lineno != t.lineno and GetRealColumn(t2) != GetRealColumn(t):
#                 #     nsiqcppstyle_reporter.Error(
#                 #         t2,
#                 #         __name__,
#                 #         "The brace for type definition should be located in same column",
#                 #     )
#
#
# ruleManager.AddTypeNameRule(namespaceRunRule)
