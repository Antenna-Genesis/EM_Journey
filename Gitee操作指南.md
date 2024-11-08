# Gitee操作指南

## 快速操作

0. ### git操作的概念图以及初始化

    1. #### 概念图

       ![image-20210620113440340](Gitee操作指南.assets/image-20210620113440340.png)

       https://www.cnblogs.com/runnerjack/p/9342362.html

    2. #### 初始化（假设首先从云端同步到本地）

       1. ##### 创建gitee账户（YN：显然第一步是拥有自己的公钥，不然根本不可能访问gitee，具体可见https://help.gitee.com/repository/ssh-key/generate-and-add-ssh-public-key）

       2. ##### 打开命令行，进入想要存放代码库文件夹的本地磁盘位置

          例如：cd /Users/some_folder

       3. ##### 从云端克隆代码库文件夹到本地(仅限第一次操作)

          例如：git clone git@gitee.com:kai-lu/SS-Scripts.git（YN：注意，这里是例子，实际是git@gitee.com:kai-lu/EM_Journey.git，一旦写错后面解绑非常麻烦）

          克隆操作之后，云端和本地代码库自动关联了起来

       4. ##### Pull也可以从云端同步代码本地的方式，但需要事先在本地创建用于存放代码库的文件夹

          1. 在本地建好文件夹之后，在命令行中操作，进入该文件夹。

             例如：cd new_folder

          2. 初始化该文件夹：git init

          3. 将本地和云端代码库关联

             例如：git remote add ssgitee git@gitee.com:kai-lu/SS-Scripts.git

             之后，可以通过git remote -v来检查

          4. 如果错误的在本地做了初始化，或者想要取消本地的git关联，可以 rm -rf .git （YN：我使用这句会报错）

       5. ##### Ready，go！如其他需求，和组内其他人讨论或者自行搜索

1. ### 从本地上传到gitee云端
（YN: 这里一定要进入EM_Journaey文件夹）

   完成本地编辑后，先add，然后commit，之后push

   `git add .`

   `git commit -m "test commit"`

   `git push gitee-ssh main`

    其中，add . 和add --all等效

   类似下面这样:

   ![image-20210618125207075](Gitee%E6%93%8D%E4%BD%9C%E6%8C%87%E5%8D%97.assets/image-20210618125207075.png)

   （YN：补充一下，即使按上面流程走一遍这里还是可能报错（参考：https://www.jiyik.com/tm/xwzj/opersys_5451.html）

fatal: 'gitee-ssh' does not appear to be a git repository

fatal: Could not read from remote repository.

审核：

１、git remote -v　需要看到

origin  git@gitee.com:kai-lu/EM_Journey.git (fetch)

origin  git@gitee.com:kai-lu/EM_Journey.git (push)

２、git branch -a　需要看到

main

  remotes/origin/HEAD -> origin/main

  remotes/origin/main

３、推送

git push origin master

）

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

   注意：如果进入了git log想出来，确保输入法在英文状态下，输入q即可（ https://blog.csdn.net/weixin_41287260/article/details/89813851 ）。

   

   pull的操作简单直接：

   `git pull gitee-ssh main`

   （YN：如果没用，使用git pull origin master）

3. ### 更多信息
   1. ### git的操作可以参考

      https://blog.csdn.net/WEB_CSDN_SHARE/article/details/79243308?utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-1.control&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-1.control

   2. ### 廖雪峰的介绍可以参考 

      https://www.liaoxuefeng.com/wiki/896043488029600/1163625339727712

      #### 另外，增加一点那个页面没有的信息（ https://gitee.com/help/articles/4181#article-header0 ）。

      #### 	廖雪峰教程中没有提到授权ssh的步骤，可能会导致无法同步。

      ​		ssh -T git@gitee.com

      ### 		确认成功之后，再次进行ssh校验，就可以看到自己的用户名了。

      ​		ssh -T git@gitee.com
      ​		Hi **! You've successfully authenticated, but GITEE.COM does not provide shell access.

      

      #### 	为生成ssh公钥，输入下面的字符串，并一直按确认键，直到完成。

      ​		ssh-keygen -t rsa -C username@xyz.com

      #### 	记下密钥位置，比如：

      ​		Your identification has been saved in /Users/.ssh/id_rsa.
      ​		Your public key has been saved in /Users/.ssh/id_rsa.pub.

      #### 	进入密钥位置，打开公钥，可以拷贝出来：

      ​		cat .ssh/id_rsa.pub

   3. ### Github的默认主干分支叫master，Gitee的叫main，需要注意差异，最好保持一致。否则，可能会见到这样的错误：

      ​	git push gitee master
      ​	error: src refspec master does not match any.
      ​	error: failed to push some refs to '

      

      

      







