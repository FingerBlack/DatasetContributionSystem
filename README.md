# DatasetContributionSystem

#### 任务目标

* [x] 数据集的管理（使用django自带的管理系统）
* [x] 用户的管理：注册，会员，权限（使用django自带的管理系统）（VIP与非VIP定义，设计Django权限结构表，代表URL访问权限）
* [x] 数据集的展示、下载、搜索
* [x] 用户上传与下载数据集
* [x] 用户发布~~与接收~~任务
* [x] 用户对数据集质量的评价
* [x] 数据集报错与修改（参数未完成）

#### ToDo-List

* 需要设计Feedback相关参数
* 需要设计数据集评价相关参数（包括显示url，或在某个url中显示，显示位置，接受参数等）
* 设计用户的**会员、权限**

#### Discussion

* 可以考虑限制只能做图像数据集，不然上传格式会很乱 （任务具体要求限制格式，用于报错识别？）
* 同意，目前可只支持分类和目标定位任务，即一幅图像只有1或5个标注：类别[必有，int]，(xmin，ymin，xmax，ymax)[可选，float]
* 如何支持数据集管理？

#### 框架

* 后端框架：Django 2.2.6
* 前端框架：Bootstrap JQuery

#### 网站结构

##### App

* userManagement

  完成页面`/login/` `/signup` `/profile/` `/logout/` `/resetPassword/`

* query

  完成页面`/query/(dataset/task)/`

* dataset

  完成页面`/dataset/(string:datasetname)` `/upload/` `/dataset/(string:datasetname)/comment/`

* task

  完成页面`/task/post/` `/task/(int:Id)/`

* feedback

  完成页面`/feedback/report/` `/feedback/(int:Id)/`
  
* homepage

  完成页面`/`

#### 网页功能

* `/` 

  首页

  包含登陆/注册按钮，在左侧展现最新数据集列表，右侧显示目前的任务

  Top List：按评价推荐数据集，按赏金推荐任务(可选)

* `/login/`

  用户登录

  参数：`username`：用户名，`password`：密码

  用户登陆界面有用户名、密码和验证码输入框，用户输入之后，先将用户输入的验证码与验证码的真值比较，如果相同就将用户名和密码加密后传到后台进行验证，如果验证通过则用户完成登陆。

  ~~验证码先搁一搁~~ ~~验证码应该可以直接调什么库之类的 实在不行搞几十张验证码放在后台~~

* `/signup/`

  用户注册

  参数：用户名`username`密码`password`邮箱`email`等基本信息。

  发送验证邮件，包括邮件验证码，输入验证码以后才可以注册。

  返回注册成功/注册失败页面

* `/profile/`

  个人信息

  显示用户个人信息，包括密码修改，资料编辑等。

* `/logout/`

  登出

  登出后清除cookies，设置用户状态为未登陆

* `/resetPassword/`

  密码重置(找回)

  邮箱验证，或者输入老密码

  ~~？邮箱验证咋做~~

* `/query/(dataset/task)/`

  查询数据集/任务

  * `/query/dataset/`

    参数包括：`size`数据集尺寸范围，`name`数据集名称，`type`数据集类别(分类，定位，分割)等

    显示数据集搜索结果

  * `/query/task/`

    参数包括：`name`任务名称，`time`发布日期，`type`任务类别等

    显示任务搜索结果

* `/dataset/(string:datasetname)/`

  数据集展示

  展示名称为datasetname的数据集，显示基本预览信息，包括数据集大小，数量，价格等

  如果datasetname留空，则显示平台全部数据集

* `/dataset/(string:datasetname)/comment/`
  
  数据集用户评价
  
  展示之前用户对于名称为datasetname的数据集的评价
  
  并提供添加新评价的窗口和添加按钮
  
  参数包括: `name`任务名称，`time`发布时间，`username`评价用户名称，`commment`评价内容等

* `/upload/`

  上传数据

  单张图像及对应标注，上传必须为zip，包括每张图片和对应xml

* `/download/`

  下载数据集

  将选定的数据集打包下载，`name`：数据集名称，`filename`：下载文件名称

  若filename留空，则全部下载，**注意下载间隔限制**

  以zip压缩将下载文件打包后回传，包含图片和xml

* `/task/post/`

  发布任务

  参数：名称，类别，要求，报酬等

* `/task/(int:Id)/`

  查看任务

  如果taskid留空，则显示所有任务，否则显示任务基本信息

* `/feedback/report/`

  报错页面
  
  上传数据集内容（成功：成功上传符合要求的数据，失败：格式等具体要求简单识别）
  
  下载数据集内容（成功：成功下载，失败：权限问题）
  
  参数：`id`报错序号，`name`任务名称，`type`feedback类型（上传或下载|成功或失败），`time`错误产生时间，`username`用户名

* `/feedback/(int:Id)/`

  查看数据集上传任务错误类型与具体内容
  
  内容错误（是否为图片）；格式错误（是否超过限定大小）；数量错误（资源数量与任务要求是否一致）；权限错误（VIP与非VIP）
  
  添加修改按钮，重新下载或上传
  
  参数：`name`任务名称，`type`错误类型，`time`时间，`username`用户名称，`warning`错误具体信息
  
  
