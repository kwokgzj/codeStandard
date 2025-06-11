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

def _check_next_comment(lexer, t):
    lexer.PushTokenIndex()
    next_comment = lexer.GetNextTokenInType("COMMENT")
    lexer.PopTokenIndex()
    if next_comment is not None and next_comment.lineno == t.lineno:
        return True

def _check_prev_comment(lexer, t):
    lexer.PushTokenIndex()
    prev_comment = lexer.GetPrevTokenInType("COMMENT")
    lexer.PopTokenIndex()
    lexer.PushTokenIndex()
    prev_semi = lexer.GetPrevTokenInType("SEMI")
    lexer.PopTokenIndex()
    if prev_comment is not None:
        if prev_semi is not None:
            if prev_semi.lineno < prev_comment.lineno:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

def _check_comment_divide(lexer, t):
    line_text = ""
    while True:
        next_token = lexer.GetNextToken(False, False, False)
        if next_token is None or next_token.lineno != t.lineno:
            break
        if next_token.value != ";":
            line_text += next_token.value
    if line_text.lstrip().startswith("//"):
        return True

def RunRule(lexer, contextStack):
    lexer.PushTokenIndex()
    t = lexer.GetCurToken()
    lexer.PopTokenIndex()
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
        if name.startswith("g_") and not _check_prev_comment(lexer, t) and not _check_comment_divide(lexer, t) and not _check_next_comment(lexer, t):
            nsiqcppstyle_reporter.Error(t, __name__,
                f"全局变量 '{name}' 必须有注释")

    # 类成员变量注释检查
    elif curContext is None or curContext.type in ["CLASS_BLOCK"]:
        if name.startswith("m_") and not _check_prev_comment(lexer, t) and not _check_comment_divide(lexer, t) and not _check_next_comment(lexer, t):
            nsiqcppstyle_reporter.Error(t, __name__,
                f"类成员变量 '{name}' 必须有注释")

ruleManager.AddRule(RunRule)