"""
检查枚举命名是否符合大驼峰命名法（PascalCase）且不包含前缀。

== 违规 ==

    enum myEnum { }; &lt;== 违规。枚举名应以大写字母开头。
    enum e_Example { }; &lt;== 违规。枚举名不应包含下划线。

== 正确 ==

    enum MyEnum { }; &lt;== 正确。使用大驼峰命名法。
    enum Example { }; &lt;== 正确。使用大驼峰命名法。
"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *
import re
import util.review_util as rv

def RunRule(lexer, currentType, fullName, decl, contextStack, typeContext):
    if not decl and currentType == "ENUM" and typeContext is not None:
        t = lexer.GetCurToken()
        if not rv.is_pascal_case(fullName):
            nsiqcppstyle_reporter.Error(
                t,
                __name__,
                f"枚举 '{fullName}' 不符合大驼峰命名规范",
            )

ruleManager.AddTypeNameRule(RunRule)
