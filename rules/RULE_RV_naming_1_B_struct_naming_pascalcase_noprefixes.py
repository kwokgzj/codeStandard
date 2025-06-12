"""
检查结构体命名是否符合大驼峰命名法（PascalCase）且不包含前缀。

== 违规 ==

    class myClass { }; <== 违规。类名应以大写字母开头。
    class c_Example { }; <== 违规。类名不应包含下划线。

== 正确 ==

    class MyClass { }; <== 正确。使用大驼峰命名法。
    class Calculator { }; <== 正确。使用大驼峰命名法。
"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *
import re
import util.review_util as rv

def RunRule(lexer, currentType, fullName, decl, contextStack, typeContext):
    if not decl and currentType == "STRUCT" and typeContext is not None:
        t = lexer.GetCurToken()
        if not rv.is_pascal_case(fullName):
            nsiqcppstyle_reporter.Error(
                t,
                __name__,
                f"结构体 '{fullName}' 不符合大驼峰命名规范",
            )

ruleManager.AddTypeNameRule(RunRule)
