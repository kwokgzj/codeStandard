"""
枚举值必须全大写，使用下划线分割单词。

== 违规示例 ==

    enum Color {
        Red,        // 违规：不是全大写
        darkBlue,   // 违规：不是全大写且没有下划线
        LIGHTGREEN  // 违规：没有用下划线分割单词
    }

== 正确示例 ==

    enum Color {
        RED,            // 正确
        DARK_BLUE,     // 正确
        LIGHT_GREEN    // 正确
    }
"""

from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *
import util.review_util as rv

g_last_lineno = None

def RunRule(lexer, typeName, typeFullName, decl, contextStack, typeContext):
    global g_last_lineno
    if not decl and typeName == "ENUM" and typeContext is not None:
        lexer._MoveToToken(typeContext.startToken)
        t2 = typeContext.endToken

        while True:
            t = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
            if t is None or t == t2:
                break

            # 检查是否是枚举值（标识符）
            if t.type == "ID" and t.lineno != g_last_lineno:
                fullName = t.value
                # 检查是否符合命名规范：全大写+下划线
                if not rv.is_macro_name(fullName):
                    nsiqcppstyle_reporter.Error(
                        t,
                        __name__,
                        f"枚举值 '{fullName}' 不符合全大写、下划线命名规范",
                    )
            g_last_lineno = t.lineno


ruleManager.AddTypeNameRule(RunRule)