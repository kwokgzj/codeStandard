// 不超过50行的函数 - OK
void GoodFunction() {
    int a = 1;
    int b = 2;
    int c = a + b;
}

// 超过50行的函数 - Violation
void BadFunction() {
    int i = 0;
    i += 1;
     i += 2;
     i += 3;
      i += 4;
      i += 5;
    i += 1;



     i += 2;



     i += 3;

      i += 4;
      i += 5;
    i += 1;



     i += 2;



     i += 3;

      i += 4;
      i += 5;
    i += 1;



     i += 2;



     i += 3;

      i += 4;
      i += 5;
    i += 1;



     i += 2;



     i += 3;

      i += 4;
      i += 5;
    i += 1;



     i += 2;



     i += 3;

      i += 4;
      i += 5;
    i += 1;



     i += 2;



     i += 3;

      i += 4;
      i += 5;
    i += 1;



     i += 2;



     i += 3;

      i += 4;
      i += 5;
    i += 1;



     i += 2;



     i += 3;

      i += 4;
      i += 5;
    i += 1;



     i += 2;



     i += 3;

      i += 4;
      i += 5;
    i += 1;



     i += 2;



     i += 3;

      i += 4;
      i += 5;
    i += 1;



     i += 2;



     i += 3;

      i += 4;
      i += 5;
    i += 1;



     i += 2;



     i += 3;

      i += 4;
      i += 5;
    i += 1;



     i += 2;



     i += 3;

      i += 4;
      i += 5;
    i += 1;



     i += 2;



     i += 3;

      i += 4;
      i += 5;
}

// 包含空行但不超过50个非空行的函数 - OK
void GoodFunctionWithEmptyLines() {
    int x = 1;

    int y = 2;

    int z = 3;

    int result = x + y + z;

}

// 包含注释的函数 - OK
void GoodFunctionWithComments() {
    // 初始化变量
    int value = 0;

    // 增加值
    value++;

    // 再次增加
    value += 2;

    /* 多行注释
     * 测试注释不计入行数
     */
    value *= 2;
}