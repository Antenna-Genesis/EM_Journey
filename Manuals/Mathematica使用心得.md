# Mathematica使用心得

## 1.变量与函数

Mathematica中的变量无需独立声明，若出现但未给出其取值范围，则程序将会视其为一个单纯的符号去加入运算

默认情况下未赋值的变量运行后是蓝色字，已赋值变量是黑色提示，而作为函数的参数则为绿色字

## 函数：

声明格式为： **函数名** + **参数列表** + **:=** + **表达式**

其中参数列表中参数格式为：**参数名**+**_**

函数的输入输出值可以为矩阵形式，{{第1行元素}, {第二行元素}, ……}

该软件的内置函数的首字母均为大写

## 2.后缀

后缀是在已经计算的表达式的基础上再进行函数操作

如![img](file:///C:/Users/Zjz/AppData/Local/Temp/msohtmlclip1/01/clip_image002.png) 

常用于处理运算结果时简化代码，使其更加直观

## 3.矩阵相关运算

https://blog.csdn.net/harryhare/article/details/53870824

特别注意：进行取出矩阵元素操作时，输入值不能是//Martix格式，否则会提示错误

## 4.画图与Manipulate操作

**Plot[f, {x, xmin, xmax}]**

  (* 绘制f的图像，自变量x范围是xmin到xmax *)

Plot[{f1, f2}, {x, xmin, xmax}]

**(* 绘制多个函数fi *)**

 Manipulate交互式操作（解决单变量多参量的可视化问题）

例：

![image-20211215104458119](C:\Users\Zjz\AppData\Roaming\Typora\typora-user-images\image-20211215104458119.png)

![image-20211215104506506](C:\Users\Zjz\AppData\Roaming\Typora\typora-user-images\image-20211215104506506.png)