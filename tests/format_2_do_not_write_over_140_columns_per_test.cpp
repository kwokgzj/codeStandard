/*
 * 测试单行字符长度规则
 * - 单行不能超过140个字符
 * - 空白行除外
 */

// 测试1：正常长度的代码行
void normalFunction() {                             // 正确：短行
    int shortVariable = 100;                        // 正确：短行
    doSomething();                                  // 正确：短行
}

// 测试2：空行

// 测试3：接近限制的行（140字符）
void functionWithLongLine() {
    string str = "This is a very long string that is exactly 140 characters long including spaces and other characters to test the line length limit rule...."; // 正确：140字符
}

// 测试4：超过限制的行
void functionWithTooLongLine() {
    string veryLongString = "This string is definitely longer than 140 characters because we want to test if the rule correctly identifies lines that exceed the maximum allowed length for a single line of code..........."; // 违规：超过140字符
}

// 测试5：长注释行
// This is a very very very very very very very very very very very very very very very very very very very very very very long comment line that exceeds 140 characters

// 测试6：长函数声明
void ExtremelyLongFunctionNameThatWillDefinitelyExceedTheLimitBecauseItIsSoLongAndHasSoManyParametersAndIsJustTooLongToBeOnASingleLine(int param1, int param2, int param3, int param4) { // 违规：超过140字符
}

// 测试7：长模板声明
template<typename ExtremelyLongTemplateParameterNameThatMakesTheLineTooLong, typename AnotherVeryLongTemplateParameterNameThatAddsToTheLength, typename YetAnotherLongName> // 违规：超过140字符
class Test {};

// 测试8：多行字符串（每行单独计算）
const char* multiLineString =
    "First line is fine\n"                         // 正确：短行
    "Second line is also fine\n"                   // 正确：短行
    "This third line is intentionally made very very very very very very very very very very very very very very very long to exceed the limit\n"; // 违规：超过140字符

// 测试9：宏定义
#define LONG_MACRO_NAME_THAT_EXCEEDS_THE_LIMIT     this_is_a_very_very_very_very_very_very_very_very_very_very_very_very_very_very_very_long_macro_definition_that_should_trigger_the_rule // 违规：超过140字符

// 测试10：带缩进的长行
void indentedFunction() {
    if (someCondition) {
        while (anotherCondition) {
            for (int i = 0; i < 100; i++) {
                doSomethingWithAVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryLongFunctionName(); // 违规：超过140字符
            }
        }
    }
}