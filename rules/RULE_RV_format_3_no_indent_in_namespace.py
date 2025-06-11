"""
命名空间内的代码不需要缩进。

== 违规示例 ==

    namespace MyNamespace {
        class MyClass {  // 违规：命名空间内缩进
        };
        void foo() {     // 违规：命名空间内缩进
        }
    }

== 正确示例 ==

    namespace MyNamespace {
    class MyClass {     // 正确：无缩进
    };
    void foo() {       // 正确：无缩进
    }
    }
"""

from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *

# 用于存储已经报告过错误的命名空间
reported_namespaces = set()

def RunRule(lexer, contextStack):
    token = lexer.GetCurToken()
    if token is None:
        return

    if token.type != "ID":
        return

    curContext = contextStack.SigPeek()

    # 检查是否在命名空间内
    if curContext is not None and curContext.type == "NAMESPACE_BLOCK":
        # 检查此命名空间是否已经报告过错误
        if curContext not in reported_namespaces:
            # 获取当前行的缩进
            line = lexer.GetCurTokenLine()
            if line.startswith((" ", "\t")):
                nsiqcppstyle_reporter.Error(token, __name__,
                                          "命名空间内的代码不应该缩进")
                # 标记该命名空间已报告错误
                reported_namespaces.add(curContext)

ruleManager.AddRule(RunRule)