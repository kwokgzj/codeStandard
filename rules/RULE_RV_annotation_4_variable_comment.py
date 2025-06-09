"""
变量注释要求：
1. 类成员变量必须有doxygen格式注释
2. 全局变量必须有doxygen格式注释
3. 局部变量不要求注释

== 违规示例 ==
    int g_count;            // 违规：全局变量缺少注释
    int m_value;           // 违规：成员变量缺少注释

== 正确示例 ==
    /** 总用户数 */
    int g_totalUsers;      // 正确：全局变量有注释

    /** 成员计数器 */
    int m_counter;         // 正确：成员变量有注释
"""
import nsiqcppstyle_reporter
from nsiqcppstyle_rulemanager import *

def _is_type_token(token):
    return token.type in ["INT", "CHAR", "FLOAT", "DOUBLE", "BOOL", "VOID", "LONG", "SHORT", "AUTO"]

def _is_var_declaration(t1, t2):
    return (_is_type_token(t1) and t2.type in ["SEMI", "EQUALS"])

def _check_comment(lexer, t):
    lexer.PushTokenIndex()
    t2 = lexer.GetPrevTokenInType("COMMENT")
    lexer.PopTokenIndex()
    lexer.PushTokenIndex()
    t3 = lexer.GetPrevTokenInTypeList(["SEMI", "PREPROCESSOR", "LBRACE"], False, True)
    lexer.PopTokenIndex()

    if t2 is not None and (t3 is None or t2.lexpos > t3.lexpos):
        if t2.additional in ["DOXYGEN_JAVADOC", "DOXYGEN_QT", "DOXYGEN_CPP"]:
            return True
    return False

def RunRule(lexer, contextStack):
    t = lexer.GetCurToken()
    if t.type != "ID":
        return

    prevToken = lexer.PeekPrevTokenSkipWhiteSpaceAndCommentAndPreprocess()
    nextToken = lexer.PeekNextTokenSkipWhiteSpaceAndCommentAndPreprocess()

    if not prevToken or not nextToken or not _is_var_declaration(prevToken, nextToken):
        return

    name = t.value
    curContext = contextStack.SigPeek()

    # 全局变量注释检查
    if curContext is None or curContext.type in ["NAMESPACE_BLOCK"]:
        if name.startswith("g_") and not _check_comment(lexer, t):
            nsiqcppstyle_reporter.Error(t, __name__,
                f"全局变量 '{name}' 必须有注释")

    # 类成员变量注释检查
    elif curContext is None or curContext.type in ["CLASS_BLOCK"]:
        if name.startswith("m_") and not _check_comment(lexer, t):
            nsiqcppstyle_reporter.Error(t, __name__,
                f"类成员变量 '{name}' 必须有注释")

ruleManager.AddRule(RunRule)