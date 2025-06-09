"""
Do not write more than 2000 lines for a file.
It only counts non blank lines.

== Violation ==

    file.cpp
    -- more than 2000 non blank lines <== Violated

== Good ==

    file.cpp
    -- less than 2000 non blank lines <== OK

"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *


def RunRule(lexer, filename, dirname):
    count = 0
    for line in lexer.lines:
        if not Match(r"^\s*$", line):
            count += 1

    if count > 2000:
        nsiqcppstyle_reporter.Error(
            DummyToken(lexer.filename, 1, 0, 0),
            __name__,
            f"{filename} 代码行数超过2000行.(实际行数：{count}行)",
        )


ruleManager.AddFileStartRule(RunRule)