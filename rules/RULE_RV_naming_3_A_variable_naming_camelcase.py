"""
变量命名规范和注释要求：
1. 局部变量必须使用小驼峰命名法
2. 类成员变量必须使用m_前缀 + 小驼峰命名法，并且必须有注释
3. 全局变量必须使用g_前缀 + 小驼峰命名法，并且必须有注释

== 违规示例 ==
    int g_count;            // 违规：全局变量缺少注释
    int m_value;           // 违规：成员变量缺少注释

== 正确示例 ==
    /** 总用户数 */
    int g_totalUsers;      // 正确：全局变量有注释

    /** 成员计数器 */
    int m_counter;         // 正确：成员变量有注释
"""

from nsiqcppstyle_rulemanager import *
from nsiqunittest.nsiqcppstyle_unittestbase import *
import util.review_util as rv

def _is_type_token(token):
    """检查是否是类型声明token"""
    return token.type in ["INT", "CHAR", "FLOAT", "DOUBLE", "BOOL", "VOID", "LONG", "SHORT", "AUTO"]

def _is_var_declaration(t1, t2):
    """检查是否是变量声明"""
    return (_is_type_token(t1) and t2.type in ["SEMI", "EQUALS"])

def _check_comment(lexer, t):
    """检查变量是否有doxygen注释"""
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

    # 全局变量检查
    if curContext is None or curContext.type in ["NAMESPACE_BLOCK"]:
        if not rv.is_global_var_name(name):
            nsiqcppstyle_reporter.Error(t, __name__,
                f"全局变量 '{name}' 必须以'g_'为前缀并使用小驼峰命名法")
        elif not _check_comment(lexer, t):
            nsiqcppstyle_reporter.Error(t, __name__,
                f"全局变量 '{name}' 必须有注释")

    # 类成员变量检查
    elif curContext is None or curContext.type in ["CLASS_BLOCK"]:
        if not rv.is_member_var_name(name):
            nsiqcppstyle_reporter.Error(t, __name__,
                f"类成员变量 '{name}' 必须以'm_'为前缀并使用小驼峰命名法")
        elif not _check_comment(lexer, t):
            nsiqcppstyle_reporter.Error(t, __name__,
                f"类成员变量 '{name}' 必须有注释")

    # 局部变量检查
    else:
        if name.startswith("m_") or name.startswith("g_"):
            nsiqcppstyle_reporter.Error(t, __name__,
                f"局部变量 '{name}' 不能使用'm_'或'g_'前缀")
        elif not rv.is_camel_case(name):
            nsiqcppstyle_reporter.Error(t, __name__,
                f"局部变量 '{name}' 必须使用小驼峰命名法")

ruleManager.AddRule(RunRule)