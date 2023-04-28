# 如何编写一个稳定的CST costfunction
由于陆老师PyCST-Kai代码中提供了一些天线建模的例子，单次仿真实验基本是成功的。
但是当进行大量的优化仿真时，CST的脚本不同于HFSS有一定的不稳定性，很难连续的进行仿真。

## ***为了避免漫长的玄学试错过程，请逐条遵守***

### 参考
API控制: 陆凯老师的 CST_Library （**不是**官方help库）和 项目中wintest.py（一些窗口自动化函数）

例子：项目中CostFunction_CST 对于s11的操作

效果：每次运行costfunction时，CST能够自动化打开窗口和project，自动化关闭project和窗口。
**只有这样**能够在同一次脚本运行时，稳定地重复打开不同的.cst文件（当然只能单线程仿真）。

### 具体注意事项
1. 调整电脑CPU配置 https://www.bilibili.com/video/BV1LK411B7ZS/?spm_id_from=333.337.search-card.all.click&vd_source=16efeee2500783445f096d0883e90368
否则会在自动化进程中非常容易出现由于算力不足导致CST自闭。

2. 使用**两个语句**打开.cst文件（其他排列组合有报错风险）
```
    cst_temp = cst_interface.cst()
    cst_temp.open_mws(cstpos)#打开cst文件
```
   
3. 重复判断是否打开（只有一次有可能打不开导致中断）
```
    while True:
        cst_temp = cst_interface.cst()
        cst_temp.open_mws(cstpos)#打开cst文件
        time.sleep(5)#睡眠一会
        if wintest.is_CST_open("DRAtest"): #直到打开成功
            break
```

4. 关闭前删除CST中仿真结果，相当于工作栏Post-Processing中delete results:
`cst_temp.delete_result()`

   连续仿真时**不要保存！！！不要用**这行代码：
 ` # cst_temp.save_cst()`

5. 退出当前project：`cst_temp.quit_cst()` ；用wingui控制关闭CST窗口：`wintest.close_cst_window("DRAtest")`