# Gitee操作指南

## 快速操作

0. ### git操作的概念图

   ![输入图片说明](Gitee%E6%93%8D%E4%BD%9C%E6%8C%87%E5%8D%97.assets/160923_57905309_9256245.png)

   https://www.cnblogs.com/runnerjack/p/9342362.html

1. ### 从本地上传到gitee云端

   完成本地编辑后，先add，然后commit，之后push

   `git add .`

   `git commit -m "test commit"`

   `git push gitee-ssh main`

   类似下面这样
   ![image-20210618125207075](Gitee%E6%93%8D%E4%BD%9C%E6%8C%87%E5%8D%97.assets/image-20210618125207075.png)

   

2. ### 从gitee云端下载到本地

   两种方案：fetch和pull，建议前者。因为前者可以提供多一次的对比，减少自己本地代码被错误的云端更新覆盖的机会。

   fetch常结合merge一起用，git fetch + git merge == git pull。一般要用git fetch+git merge，因为git pull会将代码直接合并，造成冲突等无法知道，fetch代码下来要git diff 或者log来看一下差异，然后再合并。

   

   fetch: download new branches and data from a remote repository。

   可以git fetch [alias]

   取某一个远程repo，

   也可以git fetch --all

   取到全部repo fetch将会取到所有你本地没有的数据，所有取下来的分支可以被叫做remote branches，它们和本地分支一样(可以看diff，log等，也可以merge到其他分支)，但是Git不允许你checkout到它们。

   git fetch不会更新你本地的代码，而只会更新远程库的最新代码**状态**到本地，即只是拿到了远程库最新的commit历史信息，也即你想要的‘仅仅是日志信息’。

   

   具体来看，fetch操作如下：

   `git fetch gitee-ssh main`

   `git log gitee-ssh/main ^main`

   `git merge FETCH_HEAD`

   类似下面这样：

   ![image-20210618134316254](Gitee%E6%93%8D%E4%BD%9C%E6%8C%87%E5%8D%97.assets/image-20210618134316254.png)

   注意：如果进入了git log想出来，确保输入法在英文状态下，输入q即可（https://blog.csdn.net/weixin_41287260/article/details/89813851）。

   

   pull的操作简单直接：

   `git pull gitee-ssh main`

   

3. ### 其他操作

## 更多信息

1. ### git的操作可以参考

   https://blog.csdn.net/WEB_CSDN_SHARE/article/details/79243308?utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-1.control&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-1.control

2. ### 廖雪峰的介绍可以参考 

   https://www.liaoxuefeng.com/wiki/896043488029600/1163625339727712

   ### 另外，增加一点那个页面没有的信息。

   ### 为生成ssh公钥方法，输入下面的字符串，并一直按确认键，直到完成。

   ssh-keygen -t rsa -C username@xyz.com

   ### 记下密钥位置，比如：

   Your identification has been saved in /Users/.ssh/id_rsa.
   Your public key has been saved in /Users/.ssh/id_rsa.pub.

   ### 进入密钥位置，打开公钥，可以拷贝出来：

   cat .ssh/id_rsa.pub

   ### Github的默认主干分支叫main，Gitee的叫master，需要注意差异，最好保持一致。否则，可能会见到这样的错误：

   git push gitee master
   error: src refspec master does not match any.
   error: failed to push some refs to '

   ### 廖雪峰教程中没有提到授权ssh的步骤，可能会导致无法同步。解决方法是输入下面的命令行，按指示操作（Are you sure you want to continue connecting (yes/no/[fingerprint])?这里先输入yes，再确认）。

   ssh -T git@gitee.com

   ### 确认成功之后，再次进行ssh校验，就可以看到自己的用户名了。

   ssh -T git@gitee.com
   Hi **! You've successfully authenticated, but GITEE.COM does not provide shell access.







