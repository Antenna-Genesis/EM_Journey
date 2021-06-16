# Gitee操作指南

## 廖雪峰的介绍可以参考 

https://www.liaoxuefeng.com/wiki/896043488029600/1163625339727712

## 另外，增加一点那个页面没有的信息。

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

### 同步本地文件到云端：完成本地编辑后，需要先add，然后commit，之后push

git add .

git commit -m "test commit"

git push gitee main

类似下面这样
![输入图片说明](https://images.gitee.com/uploads/images/2021/0614/161207_1ab2918f_9256245.png "屏幕截图.png")

### 同步云端文件到本地：fetch或者pull
fetch常结合merge一起用，git fetch + git merge == git pull
一般要用git fetch+git merge，因为git pull会将代码直接合并，造成冲突等无法知道，fetch代码下来要git diff orgin/xx来看一下差异然后再合并。

作者：忆飞
链接：https://www.jianshu.com/p/a5c4d2f99807
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
### git的操作可以参考

https://blog.csdn.net/WEB_CSDN_SHARE/article/details/79243308?utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-1.control&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-1.control

### git概念图解
![输入图片说明](https://images.gitee.com/uploads/images/2021/0614/160923_57905309_9256245.png "屏幕截图.png")
https://www.cnblogs.com/runnerjack/p/9342362.html

### 进入git log模式不要慌，按照这个来处理

https://blog.csdn.net/weixin_41287260/article/details/89813851



