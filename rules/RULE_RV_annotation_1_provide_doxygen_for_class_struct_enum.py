"""
Provide the class doxygen comment.
It checks if there is doxygen sytle comment in front of each class definition.

== Violation ==

    class A { <== Violation. No doxygen comment.
    };

    /*        <== Violation. It's not a doxygen comment
     *
     */
    class B {
    };

== Good ==

    /**
     * blar blar
     */
    class A { <== OK
    };

    class B; <== Don't care. It's forward decl.
"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *

"""
类必须注释
"""
def classRunRule(lexer, currentType, fullName, decl, contextStack, typeContext):
    if not decl and currentType == "CLASS" and typeContext is not None:
        t = lexer.GetCurToken()
        lexer.PushTokenIndex()
        t2 = lexer.GetPrevTokenInType("COMMENT")
        lexer.PopTokenIndex()
        lexer.PushTokenIndex()
        t3 = lexer.GetPrevTokenInTypeList(["LBRACE", "SEMI", "PREPROCESSOR"], False, True)
        lexer.PopTokenIndex()
        if t2 is not None and (t3 is None or t2.lexpos > t3.lexpos):
            if t2.additional in ["DOXYGEN_JAVADOC", "DOXYGEN_QT", "DOXYGEN_CPP"]:
                return
        nsiqcppstyle_reporter.Error(
            t,
            __name__,
            f"类({fullName})必须有注释.",
        )


ruleManager.AddTypeNameRule(classRunRule)

"""
结构体必须注释
"""
def structRunRule(lexer, currentType, fullName, decl, contextStack, context):
    if not decl and currentType in ("STRUCT", "UNION") and context is not None:
        t = lexer.GetCurToken()
        lexer.PushTokenIndex()
        t2 = lexer.GetPrevTokenInType("COMMENT")
        lexer.PopTokenIndex()
        lexer.PushTokenIndex()
        t3 = lexer.GetPrevTokenInTypeList(["SEMI", "PREPROCESSOR", "LBRACE"], False, True)
        lexer.PopTokenIndex()
        if t2 is not None and (t3 is None or t2.lexpos > t3.lexpos):
            if t2.additional in ["DOXYGEN_JAVADOC", "DOXYGEN_QT", "DOXYGEN_CPP"]:
                return
        nsiqcppstyle_reporter.Error(
            t,
            __name__,
            f"结构体({fullName})必须有注释.",
        )


ruleManager.AddTypeNameRule(structRunRule)

"""
枚举类型必须注释
"""
def classRunRule(lexer, currentType, fullName, decl, contextStack, typeContext):
    if not decl and currentType == "ENUM" and typeContext is not None:
        t = lexer.GetCurToken()
        lexer.PushTokenIndex()
        t2 = lexer.GetPrevTokenInType("COMMENT")
        lexer.PopTokenIndex()
        lexer.PushTokenIndex()
        t3 = lexer.GetPrevTokenInTypeList(["LBRACE", "SEMI", "PREPROCESSOR"], False, True)
        lexer.PopTokenIndex()
        if t2 is not None and (t3 is None or t2.lexpos > t3.lexpos):
            if t2.additional in ["DOXYGEN_JAVADOC", "DOXYGEN_QT", "DOXYGEN_CPP"]:
                return
        nsiqcppstyle_reporter.Error(
            t,
            __name__,
            f"枚举类型({fullName})必须有注释.",
        )


ruleManager.AddTypeNameRule(classRunRule)

