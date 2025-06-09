"""
Do not write more than 200 lines for a function.
It's really hard to detect comment line with keeping enough speed.
So it only counts non blank line.

== Violation ==

    void f() {
    -- more than 200 non blank lines <== Violated
    }

== Good ==

    void f() {
    -- more than 50 non blank lines <== OK
    }

"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *


def RunRule(lexer, fullName, decl, contextStack, context):
    if not decl and context is not None:
        startline = context.startToken.lineno
        endline = context.endToken.lineno
        count = 0
        for eachLine in lexer.lines[startline - 1 : endline - 1]:
            if not Match(r"^\s*$", eachLine):
                count += 1
        if count > 50:
            nsiqcppstyle_reporter.Error(
                context.startToken,
                __name__,
                f"函数 {fullName} 的非空行数超过50行 (实际: {count} 行)",
            )


ruleManager.AddFunctionNameRule(RunRule)