"""
Do not write over 140 columns per a line.
This rule doesn't recognize tabs. It only think each character as 1 column.

== Violation ==

    int HEEEEEEEEEEEEEEEEEEELLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO = 1;
    <== Violation. Too long

== Good ==

    int K; <== OK. It's short.
"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *


def RunRule(lexer, line, lineno):
    if Match(r"^\s*$", line):  # 跳过空行
        return

    # 跳过纯注释行
    if Match(r"^\s*(//|/\*|^\s*\*)", line):
        return

    # 移除行尾注释再检查长度
    code_line = line
    comment_start = line.find("//")
    if comment_start != -1:
        code_line = line[:comment_start]
        
    # 去除前后空白
    code_line = code_line.strip()

    # 检查代码部分的长度
    if len(code_line) > 140:
        nsiqcppstyle_reporter.Error(
            DummyToken(lexer.filename, line, lineno, 0),
            __name__,
            "代码行长度不能超过140个字符",
        )


ruleManager.AddLineRule(RunRule)
