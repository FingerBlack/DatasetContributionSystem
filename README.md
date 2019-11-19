# DatasetContributionSystem

#### 任务目标

* [x] 数据集的管理
* [x] 用户的管理：注册，会员
* [x] 数据集的展示、下载、搜索
* [x] 用户上传与下载数据集
* [x] 用户发布任务
* [x] 用户对数据集质量的评价
* [x] 数据集报错与修改

#### ToDo-List

* [ ] 搜索功能正则匹配(2019.11.20)
* [ ] 搜索功能实现搜索结果分页(2019.11.25)
* [ ] 搜索功能排序(2019.11.30)
* [ ] 完成任务功能(2019.11.20)
* [ ] 完成数据集下载功能(2019.11.30)

* [ ] 完成评论功能(2019.11.20)
* [ ] 完成修改评论功能(2019.11.30)
* [ ] 完成用户个人信息修改(2019.11.30)
* [ ] 完成数据集上传到数据库(2019.11.30)

#### Discussion

* 只能做图像数据集，限制格式
* 目前只支持分类和目标定位任务，即一幅图像只有1或5个标注：类别[必有，int]，(xmin，ymin，xmax，ymax)[可选，float]

#### 框架

* 后端框架：Django 2.2.6
* 前端框架：Bootstrap JQuery

#### 网站结构

##### App

* homepage

  `/`
  
* userManagement

  `/login/`
  
  `/signup/`
  
  `/profile/`
  
  `/logout/`
  
  `/resetPassword/`

* query

  `/query/(dataset/task)/`

* dataset
  
  `/dataset/`
  
  `/dataset/create/`
  
  `/dataset/(string:datasetname)/`
  
  `/dataset/(string:datasetname)/upload/`
  
  `/dataset/(string:datasetname)/download/`
  
* comment

  `/dataset/(string:datasetname)/comment/`

  `/dataset/(string:datasetname)/comment/post/`

* feedback

  `/dataset/(string:datasetname)/feedback/`

  `/dataset/(string:datasetname)/feedback/post/`

  `/dataset/(string:datasetname)/feedback/(int:Id)/`

* task

  `/dataset/(string:datasetname)/task/`
  
  `/dataset/(string:datasetname)/task/post/`
  
  `/dataset/(string:datasetname)/task/(int:Id)/edit/`

  `/dataset/(string:datasetname)/task/(int:Id)/contribution/`

#### 网页功能

* `/`

  首页

  包含登陆/注册按钮，在左侧展现最新数据集列表，右侧显示目前的任务

  Top List：按评价推荐数据集，按赏金推荐任务(可选)

* `/login/`

  用户登录

  参数：`username`：用户名，`password`：密码

  如果可能加入验证码

* `/signup/`

  用户注册

  参数：用户名`username`密码`password`邮箱`email`等基本信息。

  发送验证邮件，包括邮件验证码，输入验证码以后才可以注册。

  返回注册成功/注册失败页面

* `/profile/`

  个人信息

  显示用户个人信息与贡献值信息（与赏金挂钩），包括密码修改，资料编辑等。

* `/logout/`

  登出

  登出后清除cookies，设置用户状态为未登陆

* `/resetPassword/`

  密码重置(找回)邮箱验证

* `/query/(dataset/task)/`

  查询数据集/任务（支持模糊搜索与排序）

  * `/query/dataset/`

    参数包括：`size`数据集尺寸范围，`name`数据集名称，`type`数据集类别(分类，定位，分割)等

    显示数据集搜索结果

  * `/query/task/`

    参数包括：`name`任务名称，`time`发布日期，`type`任务类别，`payment`报酬（贡献赏金）等

    显示任务搜索结果

* `/dataset/`

  显示所有数据集
  
  参数包括：`size`数据集尺寸范围，`name`数据集名称，`type`数据集类别(分类，定位，分割)等

* `/dataset/create/`

  创建数据集
  
  参数包括：`size`数据集尺寸范围，`name`数据集名称，`type`数据集类别(分类，定位，分割)等

* `/dataset/(string:datasetname)/`

  数据集展示

  展示名称为datasetname的数据集，显示基本预览信息，包括数据集大小，数量，价格，下载所需贡献值等

* `/dataset/(string:datasetname)/upload/`

  上传数据

  单张图像及对应标注，上传必须为zip，包括每张图片和对应xml

* `/dataset/(string:datasetname)/download/`

  下载数据集

  将选定的数据集打包下载，`name`：数据集名称，`filename`：下载文件名称

  若filename留空，则全部下载，**注意下载间隔限制**

  以zip压缩将下载文件打包后回传，包含图片和xml

  注意，如果没有下载默认购买，弹窗提醒。

* `/dataset/(string:datasetname)/comment/`

  数据集用户评价

  展示为用户对于名称为datasetname的数据集的评价

  参数包括: `name`任务名称，`time`发布时间，`username`评价用户名称，`commment`评价内容等

* `/dataset/(string:datasetname)/comment/post/`

  提交用户评价

* `/dataset/(string:datasetname)/feedback/`

  查看数据集错误

   内容错误（是否为图片）
   格式错误（是否超过限定大小）
   数量错误（资源数量与任务要求是否一致）
   时间错误（是否超过任务截止时间）

* `/dataset/(string:datasetname)/feedback/post/`

  提交报错页面

  内容错误（是否为图片）
  格式错误（是否超过限定大小）
  数量错误（资源数量与任务要求是否一致）
  时间错误（是否超过任务截止时间）

  参数待定

* `/dataset/(string:datasetname)/feedback/(int:Id)/`

  查看数据集上传任务错误类型与具体内容

  内容错误（是否为图片）；格式错误（是否超过限定大小）；数量错误（资源数量与任务要求是否一致）；

  添加修改按钮，重新下载或上传

  参数：`name` 任务名称，`type` 错误类型，`time` 时间，`username` 用户名称，`warning` 错误具体信息等

* `/dataset/(string:datasetname)/task/`

  查看任务

  如果taskid留空，则显示所有任务，否则显示任务基本信息

* `/dataset/(string:datasetname)/task/post/`

  发布任务

  参数：名称，类别，要求，报酬等

* `/dataset/(string:datasetname)/task/(int:Id)/edit/`

  编辑任务

* `/dataset/(string:datasetname)/task/(int:Id)/contribution/`

  任务贡献列表
