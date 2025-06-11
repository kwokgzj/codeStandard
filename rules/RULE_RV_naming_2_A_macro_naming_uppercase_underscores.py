"""
检查枚举命名是否符合大驼峰命名法（PascalCase）且不包含前缀。

== 违规 ==

    enum myEnum { }; &lt;== 违规。枚举名应以大写字母开头。
    enum e_Example { }; &lt;== 违规。枚举名不应包含下划线。

== 正确 ==

    enum MyEnum { }; &lt;== 正确。使用大驼峰命名法。
    enum Example { }; &lt;== 正确。使用大驼峰命名法。
"""

from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *
import util.review_util as rv

def RunRule(lexer, contextStack):
    t = lexer.GetCurToken()
    if t.type == "PREPROCESSOR" and t.value.find("define") != -1:
        d = lexer.GetNextTokenSkipWhiteSpaceAndComment()
        k2 = lexer.GetNextTokenSkipWhiteSpaceAndComment()
        if d.type == "ID" and k2 is not None and k2.type in ["NUMBER", "STRING", "CHARACTOR"] and d.lineno == k2.lineno:
            fullName = d.value
            if not rv.is_macro_name(fullName):
                nsiqcppstyle_reporter.Error(
                    t,
                    __name__,
                    f"宏定义 '{fullName}' 不符合全大写、下划线命名规范.",
                )


ruleManager.AddPreprocessRule(RunRule)
