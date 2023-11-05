# NSSA_BackEnd

## 简介

数控系统安全态势感知与分析系统的后端代码，Python+Django+MySQL

## 项目架构

每个模块为一个单独的app，在根目录下使用命令`python manage.py startapp <name>`为自己的模块创建新的app，并在`/web/setting.py`中注册。

模块自己的路由在模块内定义，最后使用`include()`函数在`/web/urls.py`中同一添加

## 安装&启动

1. 安装python3.10
2. 项目要求的依赖在requirements.txt中，可通过pip install -r requirements.txt 安装相关依赖。
3. 启动服务 python manage.py runserver 0.0.0.0:8000

## 注意事项

1. 本地运行时记得修改`/web/setting.py`中的数据库设置
2. 严禁直接向master分支通过commit/push提交代码
   - 需开发新需求时，请创建以模块名/功能项为名的分支或直接fork仓库，在新分支或新仓库内进行开发及提交代码
   - 开发过程中，若主分支出现可能与当前分支代码有冲突的文件，请及时将主分支最新代码merge进当前分支
   - 开发完成后，向主仓库master分支提合并请求Pull Request；若PR内出现与主分支的文件冲突，请遵循上一条中的方法进行处理后再次提交PR
   - 提交PR后，同小组其它后端开发人员必须在PR内对所提交的代码有所review+评论
   - 最后，提醒管理员@DAchilles对PR进行review，仅允许管理员进行merge操作
3. commit的comment格式：

   add/feat/fix/del: 新增/修改/修复/删除的内容