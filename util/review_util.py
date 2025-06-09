#
# 定义代码规范检查中要用到的公共函数
#

import re

def is_pascal_case(string):
    """
    验证给定字符串是否符合大驼峰命名规则（Pascal Case）
    
    大驼峰命名规则要求：
    1. 字符串由字母和数字组成
    2. 首字母必须大写
    3. 不包含空格、下划线等特殊字符
    4. 每个单词的首字母大写
    
    Args:
        string (str): 需要验证的字符串
    
    Returns:
        bool: 如果符合大驼峰命名规则返回True，否则返回False
    """
    # 检查是否为空字符串
    if not string:
        return False
    
    # 检查首字母是否大写
    if not string[0].isupper():
        return False
    
    # 检查是否只包含字母和数字
    if not string.isalnum():
        return False
    
    # 更严格的检查：确保符合大驼峰命名模式
    # 大驼峰模式应该是以大写字母开头，后面跟着任意数量的字母或数字，
    # 然后可能有多个以大写字母开头的单词
    pattern = r'^[A-Z][a-zA-Z0-9]*([A-Z][a-zA-Z0-9]*)*$'
    return bool(re.match(pattern, string))

def is_camel_case(string):
    """
    验证给定字符串是否符合小驼峰命名规则（Camel Case）
    
    小驼峰命名规则要求：
    1. 字符串由字母和数字组成
    2. 首字母必须小写
    3. 不包含空格、下划线等特殊字符
    4. 除第一个单词外，其他单词的首字母大写
    
    Args:
        string (str): 需要验证的字符串
    
    Returns:
        bool: 如果符合小驼峰命名规则返回True，否则返回False
    """
    # 检查是否为空字符串
    if not string:
        return False
    
    # 检查首字母是否小写
    if not string[0].islower():
        return False
    
    # 检查是否只包含字母和数字
    if not string.isalnum():
        return False
    
    # 更严格的检查：确保符合小驼峰命名模式
    # 小驼峰模式应该是以小写字母开头，后面跟着任意数量的字母或数字，
    # 然后可能有多个以大写字母开头的单词
    pattern = r'^[a-z][a-zA-Z0-9]*([A-Z][a-zA-Z0-9]*)*$'
    return bool(re.match(pattern, string))


def is_macro_name(string):
    """
    验证给定字符串是否符合全大写下划线命名规范

    命名规范要求：
    1. 所有字母都是大写
    2. 单词和数字之间用下划线分隔
    3. 可以包含数字
    4. 不能以数字开头
    5. 不能包含除下划线外的其他特殊字符

    Args:
        string (str): 需要验证的字符串

    Returns:
        bool: 如果符合命名规范返回True，否则返回False
    """
    # 检查是否为空字符串
    if not string:
        return False

    # 检查是否以字母开头（不能以数字或下划线开头）
    if not string[0].isalpha():
        return False

    # 检查是否只包含大写字母、数字和下划线
    if not all(c.isupper() or c.isdigit() or c == '_' for c in string):
        return False

    # 检查是否有连续的下划线
    if '__' in string:
        return False

    # 检查是否以下划线结尾
    if string.endswith('_'):
        return False

    # 使用更宽松的正则表达式进行检查
    # 允许数字前后都可以有下划线
    pattern = r'^[A-Z][A-Z0-9]*(_[A-Z0-9]+)*$'
    return bool(re.match(pattern, string))