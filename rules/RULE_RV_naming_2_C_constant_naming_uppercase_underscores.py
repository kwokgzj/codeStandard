"""
常量必须全大写，使用下划线分割单词。

== 违规示例 ==
    const int MaxValue = 100;        // 违规：不是全大写
    const float Pi = 3.14;          // 违规：不是全大写
    static const int MAXSPEED = 200; // 违规：没有使用下划线分割

== 正确示例 ==
    const int MAX_VALUE = 100;
    const float PI = 3.14;
    static const int MAX_SPEED = 200;
"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *
from util.review_util import is_macro_name


def RunRule(lexer, contextStack):
    t = lexer.GetCurToken()
    # 检查 const 或 constexpr
    if t.type == "CONST" and contextStack.SigPeek().type in ["NAMESPACE_BLOCK"]:
        # 跳过类型、修饰符，找到变量名
        t2 = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
        while t2 is not None and t2.type not in ("ID", "SEMICOLON", "ASSIGN"):
            t2 = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
        # 检查变量名
        if t2 and t2.type == "ID" and not is_macro_name(t2.value):
            # 检查命名规范
            if not (t2.value.isupper() and "_" in t2.value):
                nsiqcppstyle_reporter.Error(
                    t2, __name__,
                    f"常量 '{t2.value}' 不符合全大写、下划线命名规范"
                )

ruleManager.AddRule(RunRule)