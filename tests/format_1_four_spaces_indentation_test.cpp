/*
 * 测试缩进规则
 * - 必须使用4个空格进行缩进
 * - 禁止使用制表符
 */

// 测试1：类定义缩进
class TestClass {      // 正确：无缩进
    int member;        // 正确：4空格缩进
  int wrong;          // 错误：2空格缩进
	int tabIndent;      // 错误：使用制表符
   int wrong2;        // 错误：3空格缩进
};

// 测试2：函数定义缩进
void testFunction()    // 正确：无缩进
{                     // 正确：无缩进
    if (true) {       // 正确：4空格缩进
        return;       // 正确：8空格缩进
    }                 // 正确：4空格缩进
  return;            // 错误：2空格缩进
}

// 测试3：空行和注释
void testEmpty()
{
                      // 正确：空行忽略缩进检查
    // 正确的注释     // 正确：4空格缩进
  // 错误的注释       // 错误：2空格缩进,注释不检查
	// Tab缩进注释     // 错误：使用制表符
}

// 测试4：复杂嵌套
void testNesting() {
    for (int i = 0; i < 10; i++) {    // 正确：4空格
        if (condition) {               // 正确：8空格
            doSomething();            // 正确：12空格
        }
  }                                   // 错误：2空格
}

// 测试5：长行和空行
void testLongLines()
{
    ReallyLongFunctionName(           // 正确：4空格
        parameter1,                    // 正确：8空格
      parameter2,                     // 错误：6空格
	    parameter3);                   // 错误：制表符+空格混用

}