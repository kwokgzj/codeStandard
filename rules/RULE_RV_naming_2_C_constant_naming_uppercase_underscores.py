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
    if t.type == "CONST" or t.type == "CONSTEXPR":
        t2 = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
        if t2 is None:
            return

        # 查找标识符（常量名）
        while t2 is not None and t2.type != "ID":
            t2 = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
            if t2 is None:
                return

        if t2 and not is_macro_name(t2.value):
            nsiqcppstyle_reporter.Error(t2, __name__,
                                        f"常量 {t2.value} 必须全大写，并使用下划线分割单词")


ruleManager.AddRule(RunRule)