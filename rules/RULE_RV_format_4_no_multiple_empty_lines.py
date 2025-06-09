"""
检查代码中的连续空行数量，不允许出现超过1行的连续空行。

== 违规 ==

    int foo() {
        int a = 1;


        return a;    // 违规：有2个连续空行
    }

== 正确 ==

    int foo() {
        int a = 1;

        return a;    // 正确：只有1个空行
    }
"""
import nsiqcppstyle_reporter
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *

# 全局变量存储上次非空行的信息
g_last_file = ""
g_last_line_no = 0


def RunRule(lexer, line, lineno):
    global g_last_file, g_last_line_no

    # 如果是新文件，重置上次行号
    if g_last_file != lexer.filename:
        g_last_file = lexer.filename
        g_last_line_no = 0
        return

    # 检查当前行是否为非空行
    if not Match(r"^\s*$", line):
        # 如果当前是非空行，且与上次非空行间隔超过2行，说明存在多个连续空行
        if g_last_line_no > 0 and (lineno - g_last_line_no) > 2:
            nsiqcppstyle_reporter.Error(
                DummyToken(lexer.filename, line, lineno, 0),
                __name__,
                f"第{g_last_line_no + 1}行到第{lineno - 1}行之间存在多个连续空行"
            )
        g_last_line_no = lineno


ruleManager.AddLineRule(RunRule)