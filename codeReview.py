import chardet
import openai
import os
import json
import argparse
import requests
import threading
import time
import logging
from logging.handlers import RotatingFileHandler
import xml.etree.ElementTree as ET

openai.api_key = 'sk-qbmnGv4vorqPw241D9246c6b427e4e98A85f3f2d5b98De9a'
openai.api_base = 'http://192.168.2.21:9300/v1'
model_name = 'deepseek-r1'

dify_check_cpp_code_standard_api_key = 'app-9atmCq5yMxiOvY8Xvn8S0fjD'
dify_check_cpp_code_standard_api_key_optimize = 'app-C3s9fIt525WfY01aSTsxvXPM'
dify_check_cpp_code_standard_api_key_optimize_1 = 'app-XZMyvyCftSwPoOX6l3bmRYNH'
dify_check_cpp_code_standard_base_url = 'http://dify.i.ai.chishine3d.com:5080/v1/workflows/run'

def get_system_prompt():
    return '''### 你是一名高级软件工程师，精通多种编程语言、框架、设计模式和最佳实践。

====

### 工具使用

你可以使用一组工具，这些工具在用户批准后执行。你每次可以使用一个工具，并将在用户的响应中收到该工具使用的执行结果。你可以通过逐步使用工具来完成给定的任务，每一步的工具使用都基于前一步的结果。

### 工具使用格式

工具使用采用类似 XML 的标签格式。工具名称被包含在开始和结束标签中，每个参数也类似地被包含在其自己的标签对中。以下是其结构：

<toolName>value</toolName>

例如：
<readFile>src/main.js</readFile>

始终遵循这种格式以确保工具被正确解析和执行。

### 工具列表

#### readFile
- 描述：请求读取指定路径文件的内容。当你需要查看某个现有文件的内容时使用此工具，例如分析代码、查看文本文件或从配置文件中提取信息。对于其他类型的二进制文件可能不适用，因为它会以字符串形式返回原始内容。
- 参数：
  - path：（必填）要读取的文件路径（相对于当前工作目录）。
- 使用示例：
<readFile>File path here</readFile>

#### listFiles
- 描述：列出指定目录中的文件和目录。
- 参数：
  - path：（必填）要列出内容的目录路径（相对于当前工作目录）。
- 使用示例：
<listFiles>Directory path here</listFiles>

====

### 工具使用指南

1. 根据任务和工具描述，选择最合适的工具。评估是否需要更多信息来继续，并考虑哪种工具最适合当前步骤。例如，使用 `listFiles` 工具比 `readFile` 工具更能获得目录下清晰的代码结构。在选择工具时，必须仔细思考每个可用工具，并选择最适合当前任务步骤的工具。
2. 如果需要多个操作，请每次使用一个工具，逐步完成任务，每个工具的使用都应基于上一个工具的结果。不要假设任何工具的使用结果。每个步骤都必须根据前一步的结果进行。
3. 按照每个工具指定的 XML 格式编写工具使用请求。
4. 每次工具使用后，用户会响应工具使用的结果。此结果将为你提供继续任务或做出进一步决策所需的信息。此响应可能包括：
   - 工具是否成功或失败，以及失败的原因。
   - 与工具使用相关的任何其他相关信息或意外结果。
5. 始终等待用户确认每个工具使用的结果后再继续。不要假设工具使用成功，除非用户明确确认结果。

逐步进行至关重要，每次工具使用后都要等待用户的反馈再继续任务。这种方法可以让你：
1. 在继续之前确认每个步骤的成功。
2. 立即解决出现的任何问题或错误。
3. 根据新信息或意外结果调整你的方法。
4. 确保每个操作都正确地建立在前一个操作的基础上。

通过等待并仔细考虑用户对每个工具使用的响应，你可以做出相应的反应，并根据情况做出明智的决策。这种逐步的方法有助于确保你的工作整体成功和准确。

====

### 代码审查策略

1. 初步分析：
   - 读取目标文件。
   - 识别关键组件和依赖项。
   - 查找导入的模块或相关文件。

2. 深入研究：
   - 读取相关文件和依赖项。
   - 分析组件之间的关系。
   - 检查接口的一致性。
   - 验证错误处理模式。

3. 审查代码时：
   - 主动检查相关文件。
   - 跟踪依赖项和导入。
   - 查找共享的工具和通用模式。
   - 考虑更广泛的系统上下文。

4. 最终审查：
   - 提供全面的分析。
   - 对问题优先级进行排序（低、中、高）。
   - 对于具体问题，提供行号。
   - 在相关时引用相关文件。

====

### 代码检查内容
重点关注以下方面：
1. 变量和数据类型问题：
    - 是否正确地进行变量的初始化和赋值操作？-低优先级
    - 是否避免使用未经初始化的变量？-低优先级
2. 内存管理和指针使用：
    - 是否正确地分配和释放动态内存？-高优先级
    - 是否避免内存泄漏和空指针解引用？-高优先级
    - 是否正确地处理指针和引用的生命周期？-中优先级
3. 异常处理：
    - 是否考虑了边界条件和异常情况?-高优先级
    - 是否正确地捕获和处理异常？-中优先级
    - 是否避免在析构函数中抛出异常？-高优先级
    - 是否适当地使用异常规范？-低优先级
4. 安全性问题：
    - 是否对用户输入进行适当的验证和过滤，以防止潜在的安全漏洞（例如缓冲区溢出、代码注入等）？-高优先级
    - 是否避免使用不安全的函数和操作，如不受限制的字符串操作、弱加密算法等？-中优先级
    - 加锁后是否正确地进行了解锁?-高优先级
5. 性能问题：
    - 是否避免不必要的计算、内存分配和复制操作？-低优先级
    - 是否适当地使用引用、移动语义和常量引用参数？-中优先级
    - 是否适当地使用算法和数据结构，以提高性能和效率？-低优先级

====

### XML格式输出规则

1. 输出格式要求：
   - 仅输出正在审查的当前文件中发现的问题
   - 不要包含相关文件中发现的问题
   - 所有输出必须遵循XML格式
   - 每个issue必须包含以下属性：
     * type：问题类型（必填）
     * description：问题描述（必填）
     * suggestedFix：建议修复方案（必填）
     * priority：问题优先级（必填）
     * example：示例代码（选填）
     * path：文件路径（必填）
     * line：行号（必填）
   - 问题类型限于以下类型，每个问题应归类到最接近的类别中，绝对不能出现除以下6种类型之外的类型：
    VARIABLES_AND_DATA_TYPES         // 变量和数据类型
    MEMORY_AND_POINTER          // 内存管理和指针使用
    EXCEPTION_HANDLING    // 异常处理
    SECURITY          // 安全性问题
    PERFORMANCE         // 性能问题
    OTHERS         // 其它问题
   - 问题优先级限于以下级别，每个问题应归类到最接近的级别中，绝对不能出现除以下3种级别之外的级别：
    LOW         // 低优先级，默认级别，只有在问题对代码质量影响较小时才使用
    MEDIUM          // 中优先级，只有在问题对代码质量有一定影响时才使用
    HIGH         // 高优先级，只有在问题严重影响代码质量时才使用
    - 标准输出格式：
       <issue>
           <type><![CDATA[错误类型]]></type>
           <description><![CDATA[问题描述]]></description>
           <suggestedFix><![CDATA[修复建议]]></suggestedFix>
           <priority><![CDATA[问题优先级]]></priority>
           <example><![CDATA[示例代码]]></example>
           <path><![CDATA[文件路径]]></path>
           <line><![CDATA[行号]]></line>
       </issue>
    - 行号的格式只能是单个的行号、多个行号，或者是一个范围这三种，不能是多个范围，或者是行号和范围的组合，或者是其他格式。
       - 正确示例：
       <line><![CDATA[10]]></line>
       <line><![CDATA[10, 15, 20]]></line>
       <line><![CDATA[10-20]]></line>
       - 错误示例：
       <line><![CDATA[10-15, 20-25]]></line>
       <line><![CDATA[10, 15-20]]></line>
       <line><![CDATA[10-15, 20]]></line>
       <line><![CDATA[36,82,171等多处]]></line>
       <line><![CDATA[36,93,157,200...]]></line>

2. 输出结构示例：
   - 对于工具使用请求的响应：
     <toolName>readFile</toolName>
     <status>success</status>
     <content>File content here</content>
     
   - 对于代码审查结果：
     <issue>
         <type><![CDATA[VARIABLES_AND_DATA_TYPES]]></type>
         <description><![CDATA[声明的未使用变量]]></description>
         <suggestedFix><![CDATA[删除未使用的变量声明]]></suggestedFix>
         <priority><![CDATA[LOW]]></priority>
         <path><![CDATA[src/main.js]]></path>
         <line><![CDATA[10]]></line>
     </issue>

     <issue>
         <type><![CDATA[MEMORY_AND_POINTER]]></type>
         <description><![CDATA[潜在的内存泄漏]]></description>
         <suggestedFix><![CDATA[在组件卸载中添加事件侦听器清理]]></suggestedFix>
         <priority><![CDATA[HIGH]]></priority>
         <example><![CDATA[useEffect(() => {
       element.addEventListener('click', handler);
       return () => element.removeEventListener('click', handler);
       }, []);]]></example>
         <path><![CDATA[src/main.js]]></path>
         <line><![CDATA[15]]></line>
     </issue>

5. 最终输出：
   - 只输出当前审查文件中发现的问题
   - 如果需要参考其他文件来理解问题，可以在description中提及，但不要输出其他文件的问题
   - 最终输出必须汇总所有步骤的结果，并提供全面的分析

====

### 代码审查验证规则

1. 变量命名验证：
   - 不检查类、函数、变量的命名
   - 不检查API字段名称是否正确
   - 不对自定义规范名称、字段进行拼写检查

2. 类设计检查：
   - 必须先读取类的声明文件
   - 必须检查是否已存在相关声明
   - 仅在完整了解类设计后才能提出设计建议

3. 错误报告前提条件：
   - 必须检查完整的类层次结构
   - 必须确认问题在当前上下文确实存在

====

### 注意事项
1. 请按照给定的步骤执行任务，等待用户的反馈后再继续下一步。
2. 只检查当前审查文件中的问题，不要输出其他文件的问题。
3. 错误类型必须符合以下6种类型之一，不得超出：
    VARIABLES_AND_DATA_TYPES         // 变量和数据类型
    MEMORY_AND_POINTER          // 内存管理和指针使用
    EXCEPTION_HANDLING    // 异常处理
    SECURITY          // 安全性问题
    PERFORMANCE         // 性能问题
    OTHERS         // 其它问题
4. 优先级必须符合以下3种级别之一，不得超出：
    LOW         // 低优先级
    MEDIUM          // 中优先级
    HIGH         // 高优先级
5. 行号的格式必须符合规定的范围，不得超出。
6. 最终输出中只包含XML格式的问题，不要包含其他内容。
7. 问题描述和修复建议必须输出中文。
8. 不检查变量命名、API字段名称、自定义规范名称的拼写。
9. 不对注释做任何检查。

====

### 记住：不要只读取目标文件。积极探索相关文件，以了解完整的上下文。输出中文。只输出XML格式内容。结果只要用户提供的审查文件的结果。'''

def get_user_prompt():
    return '''当前审查文件为：
${filePath}

当前审查代码仓库路径为：
${sourcePath}

当前审查代码仓库的目录结构为：
${sourceList}

请帮我审查该文件的代码是否存在潜在bug，并且标出行号。'''

def readFile_without_number(file_path):
    """读取文件内容"""
    try:
        encoding = DetectEncoding(file_path=file_path)
        with open(file_path, 'r', encoding=encoding) as file:  # 指定编码为 utf-8
            return file.read()
    except UnicodeDecodeError:
        # 如果 utf-8 解码失败，尝试其他编码
        try:
            with open(file_path, 'r', encoding='gbk') as file:
                return file.read()
        except Exception as e:
            return f"Error reading file: {e}"
    except Exception as e:
        return f"Error reading file: {e}"

def readFile(file_path):
    """读取文件内容"""
    try:
        encoding = DetectEncoding(file_path=file_path)
        with open(file_path, 'r', encoding=encoding) as file:
            lines = file.readlines()
            numbered_lines = [f"{line.rstrip()}/*{i+1}*/\n" for i, line in enumerate(lines)]
            content = ''.join(numbered_lines)
            return f"<toolName>readFile</toolName>\n<status>success</status>\n<content>{content}</content>"
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='gbk') as file:
                lines = file.readlines()
                numbered_lines = [f"{line.rstrip()}/*{i+1}*/\n" for i, line in enumerate(lines)]
                content = ''.join(numbered_lines)
                return f"<toolName>readFile</toolName>\n<status>success</status>\n<content>{content}</content>"
        except Exception as e:
            return f"<toolName>readFile</toolName>\n<status>failed</status>\n<error>{e}</error>"
    except Exception as e:
        return f"<toolName>readFile</toolName>\n<status>failed</status>\n<error>{e}</error>"


def listFiles(base_path):
    try:
        result = []
        base_path = os.path.abspath(base_path)  # Convert to absolute path for consistency

        for root, _, files in os.walk(base_path):
            for file_name in files:
                full_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(full_path, base_path)
                result.append(relative_path)

        content = '\n'.join(result) if result else "No files found"
        return f"<toolName>listFiles</toolName>\n<status>success</status>\n<content>{content}</content>"
    except Exception as e:
        return f"<toolName>listFiles</toolName>\n<status>failed</status>\n<error>{e}</error>"


def handle_function_call(function_name, arguments):
    """处理大模型的函数调用"""
    if function_name == "readFile":
        file_path = arguments.get("path")  # 注意：根据模型返回的参数名调整
        if file_path:
            return readFile(os.path.join(sourcePath, file_path))
        else:
            return "Error: file_path is missing in arguments"
    if function_name == "listFiles":
        base_path = arguments.get("path")
        if base_path:
            return listFiles(os.path.join(sourcePath, base_path))
        else:
            return "Error: file_path is missing in arguments"
    else:
        return f"Error: Unsupported function {function_name}"


def list_subdirectories(base_path):
    folders = []
    dir_list = os.listdir(base_path)
    for folder in dir_list:
        full_path = os.path.join(base_path, folder)
        if os.path.isdir(full_path):  # 正确判断是否为目录
            folders.append(full_path)
    if folders:
        return '\n'.join(folders)  # 统一返回string类型
    else:
        return "No subdirectories found"


def chat_with_model(client, messages):
    """与大模型对话"""
    try:
        response = client.chat.completions.create(
            model=model_name,  # 确保 model_name 已定义
            messages=messages,
            temperature=0.2,
            presence_penalty=0.0,
            frequency_penalty=0.0,
            top_p=0.95,
            timeout=bugsTimeout  # 设置超时（单位：秒）
        )
        return response.choices[0].message  # 新版 API 返回的是对象，不是字典
    except openai.APITimeoutError:
        raise Exception("OpenAI API请求超时")
    except openai.APIError as e:
        raise Exception(f"OpenAI API错误: {str(e)}")
    except Exception as e:
        raise Exception(f"未知错误: {str(e)}")

def parse_tool_call(response_content):
    if "<readFile>" in response_content:
        path_start = response_content.find("<readFile>") + len("<readFile>")
        path_end = response_content.find("</readFile>")
        path_value = response_content[path_start:path_end].strip()
        arguments = {"path": path_value}
        return "readFile", arguments
    if "<listFiles>" in response_content:
        path_start = response_content.find("<listFiles>") + len("<listFiles>")
        path_end = response_content.find("</listFiles>")
        path_value = response_content[path_start:path_end].strip()
        arguments = {"path": path_value}
        return "listFiles", arguments
    return None, None

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def get_language_extensions():
    return {
        "cpp": (".cpp", ".cxx", ".cc", ".h", ".hpp", ".hxx"),
        "c++": (".cpp", ".cxx", ".cc", ".h", ".hpp", ".hxx"),
        "C++": (".cpp", ".cxx", ".cc", ".h", ".hpp", ".hxx"),
        "python": (".py",),
        "Python": (".py",),
        "java": (".java",),
        "Java": (".java",),
        "javascript": (".js", ".jsx", ".ts", ".tsx"),
        "csharp": (".cs",),
        "go": (".go",),
        "rust": (".rs",),
        "swift": (".swift",),
        "php": (".php",),
        "ruby": (".rb",)
    }

def get_standard_api():
    if language == "cpp" or language == "c++" or language == "C++":
        return dify_check_cpp_code_standard_api_key_optimize_1, dify_check_cpp_code_standard_base_url


def validate_xml_issues(input_text):
    invalid_issues = []  # 存储无效的issues及其原因

    def is_valid_cdata(content):
        """验证CDATA格式,忽略标签内的代码示例"""
        content = content.strip()
        if not content.startswith('<![CDATA['):
            return False, "缺少CDATA开始标记"
        if not content.endswith(']]>'):
            return False, "缺少CDATA结束标记"

        # 提取CDATA内容进行检查
        cdata_content = content[9:-3]

        # 检查是否有嵌套CDATA
        if '<![CDATA[' in cdata_content:
            return False, "CDATA中不能嵌套CDATA"

        # 不检查CDATA内的代码内容
        return True, ""

    def check_required_tags(issue):
        """检查必需标签的存在性和CDATA格式"""
        required_tags = {
            'type': False,
            'description': False,
            'suggestedFix': False,
            'path': False,
            'line': False
        }
        optional_tags = {'priority', 'example'}

        # 检查必需标签
        missing_tags = []
        invalid_cdata_tags = []
        for tag in required_tags:
            start_tag = f'<{tag}>'
            end_tag = f'</{tag}>'

            start_pos = issue.find(start_tag)
            if start_pos == -1:
                missing_tags.append(tag)
                continue

            end_pos = issue.find(end_tag, start_pos)
            if end_pos == -1:
                return False, f"标签 {tag} 未闭合"

            content = issue[start_pos + len(start_tag):end_pos].strip()
            is_valid, error = is_valid_cdata(content)
            if not is_valid:
                invalid_cdata_tags.append(f"{tag}({error})")

            required_tags[tag] = True

        if missing_tags:
            return False, f"缺少必需标签: {', '.join(missing_tags)}"
        if invalid_cdata_tags:
            return False, f"CDATA格式错误: {', '.join(invalid_cdata_tags)}"

        # 检查可选标签的CDATA格式
        for tag in optional_tags:
            start_tag = f'<{tag}>'
            end_tag = f'</{tag}>'

            start_pos = issue.find(start_tag)
            if start_pos != -1:
                end_pos = issue.find(end_tag, start_pos)
                if end_pos == -1:
                    return False, f"可选标签 {tag} 未闭合"

                content = issue[start_pos + len(start_tag):end_pos].strip()
                is_valid, error = is_valid_cdata(content)
                if not is_valid:
                    return False, f"可选标签 {tag} 的CDATA格式错误: {error}"

        return True, ""

    def check_xml_structure(issue):
        """检查XML结构的完整性"""
        stack = []
        i = 0
        issue_len = len(issue)

        while i < issue_len:
            # 找到标签开始位置
            if issue[i] == '<':
                # 检查是否有可疑的 CDATA 标记
                if i + 2 <= issue_len and issue[i:i + 2] == '<!' and 'CDATA[' in issue[i:i + 50]:
                    # 如果不是标准的 CDATA 标记，则认为是无效的
                    if i + 9 > issue_len or issue[i:i + 9] != '<![CDATA[':
                        return False, "发现可疑的 CDATA 标记"
                # 跳过CDATA内容
                if i + 9 <= issue_len and issue[i:i + 9] == '<![CDATA[':
                    end = issue.find(']]>', i)
                    if end == -1:
                        return False, "CDATA未闭合"
                    i = end + 3
                    continue

                # 找到标签结束位置
                end = issue.find('>', i)
                if end == -1:
                    return False, "标签未闭合"

                tag_content = issue[i + 1:end].strip()

                # 判断是否为结束标签
                is_end_tag = tag_content.startswith('/')
                if is_end_tag:
                    tag_name = tag_content[1:]  # 去掉开头的/
                else:
                    tag_name = tag_content

                # 去掉属性部分
                if ' ' in tag_name:
                    tag_name = tag_name.split()[0]

                # 检查是否为合法标签名
                if not is_valid_tag_name(tag_name):
                    i += 1
                    continue

                # 处理开闭标签
                if is_end_tag:
                    if not stack:
                        return False, f"多余的结束标签 /{tag_name}"
                    if stack[-1] != tag_name:
                        return False, f"标签配对错误: 期望 /{stack[-1]}, 实际为 /{tag_name}"
                    stack.pop()
                else:
                    stack.append(tag_name)

                i = end + 1
            else:
                i += 1

        if stack:
            return False, f"标签未闭合: {', '.join(stack)}"
        return True, ""

    def is_valid_tag_name(tag):
        """检查是否为合法的issue XML标签名"""
        valid_tags = {
            'issue',
            'type',
            'description',
            'suggestedFix',
            'priority',
            'path',
            'line',
            'example'
        }
        return tag in valid_tags

    def extract_valid_issues(text):
        # 预检查可疑的 CDATA 标记
        suspicious_patterns = ['<![', 'CDATA[']
        for pattern in suspicious_patterns:
            if pattern in text and '<![CDATA[' not in text:
                # 如果包含可疑模式但不是标准 CDATA，直接拒绝
                return "", [("", "发现可疑的 CDATA 标记")]
        """提取并验证每个issue"""
        valid_issues = []
        start = 0

        while True:
            issue_start = text.find('<issue>', start)
            if issue_start == -1:
                break

            issue_end = text.find('</issue>', issue_start)
            if issue_end == -1:
                break

            issue = text[issue_start:issue_end + 8]

            # 按顺序验证并收集错误原因
            xml_valid, xml_error = check_xml_structure(issue)
            if not xml_valid:
                invalid_issues.append((issue, f"XML结构错误: {xml_error}"))
            else:
                tags_valid, tags_error = check_required_tags(issue)
                if not tags_valid:
                    invalid_issues.append((issue, tags_error))
                else:
                    valid_issues.append(issue)

            start = issue_end + 8

        return '\n'.join(valid_issues) if valid_issues else "", invalid_issues

    try:
        if not isinstance(input_text, str):
            return "", []
        return extract_valid_issues(input_text)
    except Exception as e:
        print(f"Error validating XML: {str(e)}")
        return "", []


def is_xml_format_correct(xml_text):
    try:
        # xml_text = xml_text.replace('\n', ' ').replace('\r', ' ')
        tree = ET.fromstring(xml_text)
    except Exception as e:
        logger.error(f" 处理 XML 时发生错误： ‘{str(e)}’ ---- 详细内容如下 : '{xml_text}' ")
        return False


def DetectEncoding(file_path):
    try:
        # 首先尝试以二进制模式读取文件
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            # 使用chardet检测编码
            result = chardet.detect(raw_data)
            detected_encoding = result['encoding']

            # 如果检测失败或置信度较低，使用常见编码列表
            if not detected_encoding or result['confidence'] < 0.9:
                # 尝试常见编码
                for encoding in ['utf-8', 'gbk', 'gb2312', 'ascii', 'iso-8859-1']:
                    try:
                        raw_data.decode(encoding)
                        return encoding
                    except UnicodeDecodeError:
                        continue
                # 如果都失败，返回默认编码
                return 'utf-8'

            return detected_encoding
    except Exception as e:
        # 发生异常时返回默认编码
        return 'utf-8'

# dify代码规范性检查
def check_code_standard(filePath, code):
    api_key, api_url = get_standard_api()
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        "inputs": {
            "filePath": filePath,
            "code": code
        },
        # Added query field
        "response_mode": "blocking",
        "conversation_id": "",
        "user": "codeReviewer"
    }
    retry_delay = retryDelay
    for attempt in range(maxRetries):
        try:
            response = requests.post(api_url, headers=headers, json=data, timeout=standardsTimeout)
            response.raise_for_status()

            result = response.json()
            return result.get('data').get('outputs').get('output')


        except Exception as e:
            logger.info(f"Standards Check: Failed , exception : {str(e)}")
            if attempt == maxRetries - 1:
                logger.info(f"Standards Check: Failed after {maxRetries} attempts for file '{filePath}'")
                return ""

            logger.info(f"Standards Check：Attempt {attempt + 1} for file '{filePath}' failed, retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

            retry_delay *= 2


def check_standards(data):
    review_result_path = os.path.join(outputPath, "reviewResult1.xml")
    if not os.path.exists(review_result_path):
        with open(review_result_path, "w", encoding="utf-8") as f:
            f.write("")  # 创建空文件
    total_start_time = time.time()
    total_files = len(data)
    successCount = 0
    for i, entry in enumerate(data, 1):
        entry_start_time = time.time()

        check_result = check_code_standard(entry['filePath'],
                                           readFile_without_number(os.path.join(sourcePath, entry['filePath'])))

        if check_result and isinstance(check_result, str):
            # logger.info(f"Standards Check response : {check_result}")
            start = check_result.find('<issue')
            end = check_result.rfind('</issue>') + len('</issue>')
            validate_response, invalid_issues = validate_xml_issues(check_result[start:end])
            if validate_response:
                try:
                    encoding = DetectEncoding(file_path=review_result_path)
                    with open(review_result_path, "a", encoding=encoding) as f:
                        f.write(f"{validate_response}\n")
                    # logger.info(f"Successfully wrote standards check results for {entry['filePath']}")
                    successCount += 1
                except Exception as e:
                    logger.error(f"Error writing standards check results: {str(e)}")
            else:
                logger.error(f"Invalid XML format in standards check results for {entry['filePath']}: {check_result[start:end]}")
            if invalid_issues:
                logger.info(f"{entry['filePath']}规范检查的结果中有无效的issues:")
                for i, (issue, reason) in enumerate(invalid_issues, 1):
                    logger.info(f"\n无效issue {i}: 原因: {reason} 。 内容：{issue}")

        entry_time = time.time() - entry_start_time
        elapsed_time = time.time() - total_start_time
        if(successCount == 0):
            avg_time_per_file = 60
        else:
            avg_time_per_file = elapsed_time / successCount
        remaining_files = total_files - i
        estimated_remaining = avg_time_per_file * remaining_files
        logger.info(f"Standards Check: File {entry['filePath']} takes {entry_time:.2f}s , current progress - {i}/{total_files} ({(i / total_files) * 100:.1f}%) , Elapsed: {format_time(elapsed_time)} / Remaining: {format_time(estimated_remaining)}")

    total_time = time.time() - total_start_time
    logger.info(f"Standards Check: All {total_files} files completed. Total time: {format_time(total_time)}\n")

def check_standards_with_script(data):
    review_result_path = os.path.join(outputPath, "reviewResult1.xml")
    if not os.path.exists(review_result_path):
        with open(review_result_path, "w", encoding="utf-8") as f:
            f.write("")  # 创建空文件
    total_start_time = time.time()
    total_files = len(data)
    successCount = 0
    for i, entry in enumerate(data, 1):
        entry_start_time = time.time()

        run_code_standards_script(entry['filePath'])

        entry_time = time.time() - entry_start_time
        elapsed_time = time.time() - total_start_time
        if(successCount == 0):
            avg_time_per_file = 60
        else:
            avg_time_per_file = elapsed_time / successCount
        remaining_files = total_files - i
        estimated_remaining = avg_time_per_file * remaining_files
        logger.info(f"Standards Check: File {entry['filePath']} takes {entry_time:.2f}s , current progress - {i}/{total_files} ({(i / total_files) * 100:.1f}%) , Elapsed: {format_time(elapsed_time)} / Remaining: {format_time(estimated_remaining)}")

    total_time = time.time() - total_start_time
    logger.info(f"Standards Check: All {total_files} files completed. Total time: {format_time(total_time)}\n")

def check_bugs(data, system_prompt, user_context):
    review_result1_path = os.path.join(outputPath, "reviewResult2.xml")
    if not os.path.exists(review_result1_path):
        with open(review_result1_path, "w", encoding="utf-8") as f:
            f.write("")  # 创建空文件
    total_start_time = time.time()
    total_files = len(data)
    successCount = 0
    global success
    for i, entry in enumerate(data, 1):
        if entry['filePath'].endswith('.h'):
            logger.info(f"Bugs Check: Skipping header file {entry['filePath']}")
            continue
        retry_delay = retryDelay
        entry_start_time = time.time()

        entry_context = user_context.replace("${filePath}", entry['filePath'])
        entry_context = entry_context.replace("${sourcePath}", sourcePath)
        entry_context = entry_context.replace("${sourceList}", list_subdirectories(sourcePath))

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": entry_context}
        ]
        # logger.info(f"Bugs Check session - system prompt : {system_prompt}")
        # logger.info(f"Bugs Check session - task : {entry_context}")
        success = True
        attempt = 0
        client = openai.OpenAI( api_key=openai.api_key, base_url=openai.api_base)
        while success:
            try:
                response = chat_with_model(client, messages)
                # assistant_response = response.get('content')
                assistant_response = response.content
                # reasoning_content = response.get('reasoning_content')
                # reasoning_content = response.reasoning_content

                function_name, arguments = parse_tool_call(assistant_response)
                if function_name:
                    tool_response = handle_function_call(function_name, arguments)
                    messages.append({"role": "assistant", "content": assistant_response})
                    messages.append({"role": "user", "content": tool_response})
                    # logger.info(f"Bugs Check session - agent resoning : {reasoning_content}")
                    # logger.info(f"Bugs Check session - agent response : {assistant_response}")
                    # logger.info(f"Bugs Check session - user : {tool_response}")
                    attempt = 0
                    retry_delay = retryDelay
                else:
                    start = assistant_response.find('<issue')
                    end = assistant_response.rfind('</issue>') + len('</issue>')
                    # logger.info(f"Bugs Check session - agent resoning : {reasoning_content}")
                    # logger.info(f"Bugs Check session - agent response : {assistant_response}")
                    validate_response, invalid_issues = validate_xml_issues(assistant_response[start:end])
                    if invalid_issues:
                        logger.info(f"{entry['filePath']}bug检查的结果中有无效的issues:")
                        for i, (issue, reason) in enumerate(invalid_issues, 1):
                            logger.info(f"\n无效issue {i}: 原因: {reason} 。 内容：{issue}")
                    if validate_response:
                        try:
                            encoding = DetectEncoding(file_path=review_result1_path)
                            with open(review_result1_path, "a", encoding=encoding) as f:
                                f.write(f"{validate_response}\n")
                            # logger.info(f"Successfully wrote bug check results for {entry['filePath']}")
                            successCount += 1
                        except Exception as e:
                            logger.error(f"Error writing bug check results: {str(e)}")
                    else:
                        logger.error(
                            f"Invalid XML format in bug check results for {entry['filePath']}: {assistant_response[start:end]}")
                    success = False
                    break
            except Exception as e:
                logger.info(f"Bugs Check: Failed , exception : {str(e)}")
                if attempt == maxRetries:
                    logger.info(f"Bugs Check: Failed after {maxRetries} attempts for file '{entry['filePath']}'")
                    success = False
                    break

                logger.info(f"Bugs Check: Attempt {attempt + 1} for file '{entry['filePath']}' failed, retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2
                attempt += 1

        entry_time = time.time() - entry_start_time
        elapsed_time = time.time() - total_start_time
        if (successCount == 0):
            avg_time_per_file = 60
        else:
            avg_time_per_file = elapsed_time / successCount
        remaining_files = total_files - i
        estimated_remaining = avg_time_per_file * remaining_files
        logger.info(f"Bugs Check: File {entry['filePath']} takes {entry_time:.2f}s , current progress - {i}/{total_files} ({(i / total_files) * 100:.1f}%) , Elapsed: {format_time(elapsed_time)} / Remaining: {format_time(estimated_remaining)}")

    total_time = time.time() - total_start_time
    logger.info(f"Bugs Check: All {total_files} files completed. Total time: {format_time(total_time)}\n")


def setup_logger(log_file_path):
    """Set up a thread-safe logger that writes to both file and console"""
    logger = logging.getLogger('CodeReviewer')
    logger.setLevel(logging.INFO)

    # Prevent adding duplicate handlers
    if not logger.handlers:
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

        # Create file handler with rotation
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Create global logger
logger = None

def init_logger(output_path):
    """Initialize the global logger"""
    global logger
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    logger = setup_logger(os.path.join(output_path, 'codeReview.log'))
    return logger

def run_code_standards_script(file_path):
    """调用外部脚本进行处理"""
    current_dir = os.getcwd()
    try:
        nsiqcppstyle_path = f'"{os.path.join(codePath, "nsiqcppstyle.py")}"'
        source_file = f'"{os.path.join(sourcePath, file_path)}"'
        filter_file = f'"{os.path.join(codePath, "filefilter.txt")}"'
        output_dir = f'"{outputPath}"'

        cmd = f'python {nsiqcppstyle_path} {source_file} -f {filter_file} --output xml -o {output_dir}'
        retcode = os.system(cmd)
    except Exception as e:
        logger.error(f"执行规范检查脚本时发生错误: {str(e)}")
        return False
    convert_nsiqcppstyle_report(file_path)
    return True


def convert_nsiqcppstyle_report(file_path):
    """
    转换nsiqcppstyle_report.xml为指定的issue格式
    参数:
        file_path: 要写入issue的目标文件路径
    """
    review_result_path = os.path.join(outputPath, "reviewResult1.xml")
    if not os.path.exists(review_result_path):
        return False
    report_path = os.path.join(outputPath, "nsiqcppstyle_report.xml")
    if not os.path.exists(report_path):
        return False
    try:
        # 以二进制模式读取文件内容
        with open(report_path, 'rb') as f:
            content = f.read()
            # 检测文件编码
            result = chardet.detect(content)
            encoding = result['encoding']

        # 使用检测到的编码重新读取文件
        with open(report_path, 'r', encoding=encoding) as f:
            content = f.read()
            # 移除可能的BOM标记
            if content.startswith('\ufeff'):
                content = content[1:]
            # 解析XML
            root = ET.fromstring(content)

        # 获取输出文件的编码
        encoding_out = DetectEncoding(review_result_path)

        # 打开目标文件以追加模式写入
        with open(review_result_path, "a", encoding=encoding_out) as f:
            # 遍历所有error元素
            for error in root.findall('.//error'):
                line = error.get('line', '')
                message = error.get('message', '').encode('utf-8').decode('utf-8')

                # 创建标准格式的issue
                issue = f"""<issue>
    <type><![CDATA[CODE_SPECIFICATION]]></type>
    <description><![CDATA[{message}]]></description>
    <priority><![CDATA[LOW]]></priority>
    <path><![CDATA[{file_path}]]></path>
    <line><![CDATA[{line}]]></line>
</issue>
"""
                # 写入文件
                f.write(issue)

        return True

    except ET.ParseError as e:
        logger.error(f"解析nsiqcppstyle报告时发生错误: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"转换nsiqcppstyle报告时发生错误: {str(e)}")
        return False

def main():
    current_dir = os.getcwd()
    logger.info(f"Current checking directory: {current_dir}")

    if not os.path.exists(outputPath):
        try:
            os.makedirs(outputPath)
            logger.info(f"Created output directory: {outputPath}")
        except OSError as e:
            logger.error(f"Error creating output directory: {e}")
            return
    if not os.path.exists(sourcePath):
        logger.error(f"Source path {sourcePath} does not exist.")
        return
    # 读取文件并解析为字典列表
    data = []
    if not os.path.exists(fileListPath) or fileListPath == "":
        changedFiles = os.path.join(outputPath, "changedFiles.txt")
        logger.info(f"fileListPath not found, will check all files in {sourcePath}...")
        file_paths = []
        for root, _, files in os.walk(sourcePath):
            if len(checkDirs) != 0 and not any(os.path.commonpath([root, os.path.join(sourcePath, d)]) ==
                                               os.path.join(sourcePath, d) for d in checkDirs):
                continue

            for file in files:
                if file.endswith(fileExtensions):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, sourcePath)
                    file_paths.append(rel_path)
                    entry = {"filePath": rel_path}
                    data.append(entry)
        logger.info(f"^^^^^^^^^^^ file_paths : {sourcePath}...")

        # Write paths to fileListPath
        with open(changedFiles, "w", encoding="utf-8") as f:
            f.write("\n".join(file_paths))
            logger.info(f"^^^^^^^^^^^ Write paths to fileListPath")
        logger.info(f"Created file list at: {changedFiles}")
    else:
        encoding = DetectEncoding(file_path=fileListPath)
        with open(fileListPath, "r", encoding=encoding) as file:
            content = file.read().strip()
            if not content:
                logger.info(f"File {fileListPath} is empty, will not check...")
                return

            # Reset file pointer to start
            file.seek(0)
            for line in file:
                filepath = line.strip()
                if filepath.endswith(fileExtensions):
                    full_path = os.path.join(sourcePath, filepath)
                    if os.path.exists(full_path):
                        entry = {"filePath": filepath}
                        data.append(entry)
                    else:
                        logger.warning(f"Warning: File not found - {filepath}")

    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    logger.info(json_data)

    system_prompt = get_system_prompt()
    user_context = get_user_prompt()

    start_time = time.time()
    threads = []

    if checkType in ["standards", "both"]:
        standards_thread = threading.Thread(target=check_standards_with_script, args=(data,))
        threads.append(standards_thread)
        standards_thread.start()

    if checkType in ["bugs", "both"]:
        bugs_thread = threading.Thread(target=check_bugs, args=(data, system_prompt, user_context,))
        threads.append(bugs_thread)
        bugs_thread.start()

    # 等待所有启动的线程完成
    for thread in threads:
        thread.join()
    elapsed_time = time.time() - start_time
    logger.info(f"Code Check: All files completed. Total time: {format_time(elapsed_time)}\n")

    review_result_path = os.path.join(outputPath, "reviewResult.xml")
    if not os.path.exists(review_result_path):
        with open(review_result_path, "w", encoding="utf-8") as f:
            f.write("")  # Create empty file

    content1 = ""
    content2 = ""
    review_result1_path = os.path.join(outputPath, "reviewResult1.xml")
    if os.path.exists(review_result1_path):
        try:
            encoding = DetectEncoding(file_path=review_result1_path)
            with open(review_result1_path, "r", encoding=encoding) as f:
                content = f.read()
                # 确保content是字符串类型
                content1 = content or ""
        except Exception as e:
            content1 = ""
            logger.error(f" 处理 reviewResult1.xml 时发生错误： ‘{str(e)}’ ")
    review_result2_path = os.path.join(outputPath, "reviewResult2.xml")
    if os.path.exists(review_result2_path):
        try:
            encoding = DetectEncoding(file_path=review_result2_path)
            with open(review_result2_path, "r", encoding=encoding) as f:
                content = f.read()
                # 确保content是字符串类型
                content2 = content or ""
        except Exception as e:
            content2 = ""
            logger.error(f" 处理 reviewResult2.xml 时发生错误： ‘{str(e)}’ ")
    encoding = DetectEncoding(file_path=review_result_path)
    with open(review_result_path, "w", encoding=encoding) as f:
        header = '<results label="CodeReviewer" version="1.0">\n'
        footer = "</results>"
        # 组合所有内容并确保都是字符串
        content = f"{header}{content1}{content2}{footer}"
        f.write(content)

    # os.remove("reviewResult2.xml")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the script with file name and source path.")
    parser.add_argument("--outputPath", type=str, required=True,
                        help="Directory path where review results and XML files will be saved")

    parser.add_argument("--fileListPath", type=str, default="",
                        help="Path to the file containing list of files to review in format 'filePath:path/to/file' on each line")

    parser.add_argument("--sourcePath", type=str, default="", required=True,
                        help="Root directory path containing all source files to be reviewed")

    parser.add_argument("--codePath", type=str, default="", required=True,
                        help="Root directory path containing all source files to be reviewed")

    parser.add_argument("--checkDirs", type=str, nargs="*", default=[],
                        help="Specific directories to check within the source path. If empty, all directories will be checked")

    parser.add_argument("--language", type=str, default="cpp", choices=get_language_extensions().keys(),
                        help="Programming language to check (default: cpp)")

    parser.add_argument("--checkType", type=str, default="both", choices=["bugs", "standards", "both"],
                        help="Type of checks to perform: 'bugs' for bug checks only, 'standards' for coding standards only, 'both' for both (default: both)")

    parser.add_argument("--standardsTimeout", type=int, default=800,
                        help="Timeout in seconds for standards check API calls (default: 800)")

    parser.add_argument("--bugsTimeout", type=int, default=300,
                        help="Timeout in seconds for bugs check API calls (default: 120)")

    parser.add_argument("--maxRetries", type=int, default=3,
                        help="Maximum number of retry attempts for failed API calls (default: 3)")

    parser.add_argument("--retryDelay", type=int, default=2,
                        help="Initial delay in seconds between retry attempts (default: 2)")

    args = parser.parse_args()
    global fileListPath, sourcePath, outputPath, fileExtensions, standardsTimeout, bugsTimeout, maxRetries, retryDelay, language, checkDirs, checkType, codePath

    if args.fileListPath == "":
        fileListPath = ""
    else:
        fileListPath = os.path.abspath(args.fileListPath)

    if args.sourcePath == "":
        sourcePath = os.path.dirname(os.path.abspath(__file__))
    else:
        sourcePath = os.path.abspath(args.sourcePath)
    codePath = os.path.abspath(args.codePath)
    checkDirs = args.checkDirs
    outputPath = os.path.abspath(args.outputPath)
    fileExtensions = get_language_extensions()[args.language]
    standardsTimeout = args.standardsTimeout
    bugsTimeout = args.bugsTimeout
    maxRetries = args.maxRetries
    retryDelay = args.retryDelay
    language = args.language
    checkType = args.checkType

    init_logger(outputPath)

    main()