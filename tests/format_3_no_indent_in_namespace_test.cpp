/*
 * 测试命名空间内不需要缩进的规则
 */

// 测试1：正确的命名空间代码（无缩进）
namespace Test1 {
class MyClass {
    void method() {
        int x = 1;
    }
};
void foo() {
    int y = 2;
}
} // namespace Test1

// 测试2：错误的命名空间代码（有缩进）
namespace Test2 {
    class WrongClass {        // 错误：缩进
        void method() {
            int x = 1;
        }
    };
    void wrongFoo() {        // 错误：缩进
        int y = 2;
    }
} // namespace Test2

// 测试3：嵌套命名空间
namespace Outer {
namespace Inner {
class NestedClass {          // 正确：无缩进
    void method() {
        int x = 1;
    }
};
} // namespace Inner
} // namespace Outer

// 测试4：匿名命名空间
namespace {
class Anonymous {            // 正确：无缩进
    int x;
};
void anonymousFunction() {   // 正确：无缩进
    int y;
}
}

// 测试5：带注释的命名空间
namespace Test5 {
// 这是一个注释
class CommentedClass {       // 正确：无缩进
    int x;
};

void function() {           // 正确：无缩进
    int y;
}
} // namespace Test5

// 测试6：多重嵌套
namespace A {
namespace B {
namespace C {
class DeepNested {          // 正确：无缩进
    void method() {
        int x = 1;
    }
};
} // namespace C
} // namespace B
} // namespace A