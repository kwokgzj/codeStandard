"""
变量命名规范：
1. 局部变量必须使用小驼峰命名法
2. 类成员变量必须使用m_前缀 + 小驼峰命名法
3. 全局变量必须使用g_前缀 + 小驼峰命名法

== 违规示例 ==
    int MyVariable;          // 违规：首字母大写
    int memberVar;           // 违规：类成员变量缺少m_前缀
    int g_MAX_COUNT;        // 违规：全局变量使用了大写

== 正确示例 ==
    int myVariable;          // 正确：局部变量
    int m_memberCount;       // 正确：类成员变量
    int g_totalUsers;       // 正确：全局变量
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
    # 类成员变量检查
    elif curContext is None or curContext.type in ["CLASS_BLOCK"]:
        if not rv.is_member_var_name(name):
            nsiqcppstyle_reporter.Error(t, __name__,
                f"类成员变量 '{name}' 必须以'm_'为前缀并使用小驼峰命名法")
    # 局部变量检查
    else:
        if name.startswith("m_") or name.startswith("g_"):
            nsiqcppstyle_reporter.Error(t, __name__,
                f"局部变量 '{name}' 不能使用'm_'或'g_'前缀")
        elif not rv.is_camel_case(name):
            nsiqcppstyle_reporter.Error(t, __name__,
                f"局部变量 '{name}' 必须使用小驼峰命名法")

ruleManager.AddRule(RunRule)
