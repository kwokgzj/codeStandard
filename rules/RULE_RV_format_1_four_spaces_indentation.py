"""
必须使用4个空格进行缩进。

== 违规示例 ==

    void Hello()
    {
    [TAB]Hello();     // 违规：使用了制表符
      Hello();        // 违规：只使用了2个空格
     Hello();         // 违规：使用了3个空格

== 正确示例 ==

    void Hello()
    {
        Hello();     // 正确：使用4个空格缩进
    }

"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqcppstyle_types import *
from nsiqunittest.nsiqcppstyle_unittestbase import *


def RunRule(lexer: Lexer, line: LineText, lineno: LineNumber) -> None:
    t = lexer.GetCurToken()

    # 跳过注释行
    if t.type in ["COMMENT", "CPPCOMMENT"]:
        next_token = lexer.GetNextTokenSkipWhiteSpaceAndComment()
        if next_token.lineno != t.lineno:
            return

    # 跳过空白行
    if Match(r"^\s*$", line):
        return

    # 检查是否使用了制表符
    if Search("^\t", line):
        nsiqcppstyle_reporter.Error(
            DummyToken(lexer.filename, line, lineno, 0),
            __name__,
            "禁止使用制表符(Tab)进行缩进，请使用4个空格",
        )
        return

    # 获取行首空格数量
    leading_spaces = len(line) - len(line.lstrip(' '))
    if leading_spaces > 0 and leading_spaces <= 20 and leading_spaces % 4 != 0:
        nsiqcppstyle_reporter.Error(
            DummyToken(lexer.filename, line, lineno, 0),
            __name__,
            "缩进必须是4的倍数个空格",
        )


ruleManager.AddLineRule(RunRule)