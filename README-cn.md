pixiver
=======

[![logo2](https://img.shields.io/badge/pypi-0.0.8.02212-blue.svg)](https://pypi.org/project/pixiver/)
[![build](https://travis-ci.org/darkchii/pixiver.svg?branch=master)](https://travis-ci.org/darkchii/pixiver)

这是一个通过 pixiv ajax API 接口访问[ [pixiv] ](https://www.pixiv.net/)资源的 python 包。

安装
----

`$ pip install -U pixiver`

快速开始
-------

```python
from pixiver.pixiv import Pixiv

p = Pixiv(username='user', password='pw')
pw = p.works(73225282)
pw.mark()
pw.like()
pw.bookmark()
pw.save_original()
```

入门指南
-------

目前 `pixiver` 支持以下功能：

注意: 删除线表示 pixiv 没有提供这类服务或 api。

 + 可浏览 pixiv 每日、每周、每月、新人、原创、受男性欢迎、受女性欢迎排行榜作品。（不需要登录）

 + 可浏览 每日 + R-18、每周 + R-18、受男性欢迎 + R-18、受女性欢迎 + R-18 排行榜与其它 R-18 相关内容。（需要登录）

 + 可根据作品 id 查看作品相关信息。（不需要登录）

 + 可浏览作品下的所有评论。（不需要登录）

 + 可浏览作品标签、排名、点赞数、收藏数等信息。（不需要登录）
 
 + 可点赞、收藏喜欢的作品。（需要登录）（token + cookie 验证）
 
 + 可关注喜欢的作者。（需要登录）（token + cookie 验证）

 + 可下载不同尺寸的作品。（不需要登录）

 + 可根据用户 id 获取相关信息。（不需要登录）

 + 其他。

下面开始学习如何使用吧！（个人建议使用 python console）

1. 排行榜

```python
from pixiver.pixiv import Pixiv

p = Pixiv(username='username', password='password')
# or Pixiv(cookie=True, path='../cookie')
pr = p.rank(20190219)
```

对于正确合法的日期，加载成功后将会显示：

```
Pixiver Initializing...
Initialized!
```

接下来这里我们有两种方式可以浏览排行版

* 使用 `batch()` 一次加载排行榜前 50 个图像进行处理。但对于网络不好的使用者来说，这可能会很头痛。不过我还提供了另一种加载方式（见方法2）。

```
>>> pr.batch()
```

获取当前批次第一个作品

```
>>> prf = pr.first()
```

查看图像尺寸

```
>>> prf['illust_attrs'].imsize()
(height, width)
```

查看作品原图链接

```
>>> prf['illust_attrs'].original_url()
'...'
```

查看作品迷你图链接

```
>>> prf['illust_attrs'].mini_url()
'...'
```

作品标题

```
>>> prf['illust_attrs'].illust_title()
'...'
```

作者昵称

```
>>> prf['illust_attrs'].author_name()
'...'
```

作品 id

```
>>> prf['illust_attrs'].illust_id()
'id'
```

作品创建日期（未作处理）

```
>>> prf['illust_attrs'].create_date()
'...T15:00:05+00:00'
```

作品上传日期（未作处理）

```
>>> prf['illust_attrs'].upload_date()
'...T15:00:05+00:00'
```


作品链接（这类图应该是除原图外，质量最好的）

```
>>> prf['illust_attrs'].regular_url()
'...'
```

查看作品浏览数

```
>>> prf['illust_attrs'].view_count()
...
```

查看点赞数

```
>>> prf['illust_attrs'].like_count()
...
```

查看收藏数

```
>>> prf['illust_attrs'].mark_count()
...
```

查看评论数

```
>>> prf['illust_attrs'].comment_count()
...
```

查看作品排名

```
>>> prf['rank']
...
```

查看评论

```
>>> prfvc = prf['illust_attrs'].view_comments()
>>> prfvc.first()['comment']
...
>>> prfvc.first()['userName']
...
>>> prfvc.next()['comment']
...
```

查看作品标签信息

```
>>> tags = prf['illust_attrs'].view_tags()
>>> tf = tags.first()
>>> tf
<tagiv.WorksTag object 0x00..>
>>> tf.view_tag()
# tag
...
```

一种更快的获取所有标签的方法

```
>>> for tag in prf['illust_attrs'].all()['tags']['tags']:
...     print(tag['tag'])
...
# output some tags
...
```

查看图像

```
>>> prf['illust_attrs'].view_regul_image()
```

喜欢就保存一个（默认保存查看的图像类型）

```
>>> prf['illust_attrs'].save() # 尺寸为 regular
Saved!
```

一种直接保存原图的方式

```
>>> prf['illust_attrs'].save_original()
Saved!
```

获取下一个作品

```
>> prn = pr.next()
```

用法与前一个一样

```
>>> prn['illust_attrs'].imsize()
(height, width)
```

* 一次加载一条：`one()` 一次加载排行榜前 50 个中的 1 个，并加入到队列中，这样依然能使用 `batch()` 一样的功能。

```
>>> pro = pr.one()
```

用法也一样

查看浏览量

```
>>> pro['illust_attrs'].view_count()
...
```

作者昵称

```
>>> pro['illust_attrs'].author_name()
'...'
```

查看标签

```
>>> t = pro['illust_attrs'].view_tags()
>>> tf = t.first()
>>> tf.tag_info()
{'tag': '...', 'abstract': '...', 'thumbnail': '...'}
>>> tf.view_tag()
'...'
>>> for tag in pro['illust_attrs'].all()['tags']['tags']:
...     print(tag['tag'])
...
```

查看点赞数

```
>>> pro['illust_attrs'].like_count()
...
```

查看收藏数

```
>>> pro['illust_attrs'].mark_count()
...
```

查看评论数

```
>>> pro['illust_attrs'].comment_count()
...
```

查看评论

```
>>> provc = ro['illust_attrs'].view_comments()
>>> provc.first()['comment']
...
>>> provc.curr()['comment']
...
>>> provc.next()['comment']
...
>>> provc.last()['comment']
...
```

其他排行榜用法相同，类名分别为：

```
rankiv.Daily
rankiv.Weekly
rankiv.Mouthly
rankiv.Rookie
rankiv.Original
rankiv.Male
rankiv.Female
```

R-18 排行榜需要登录（目前只能手动设置 cookie 才能浏览）
```
rankiv.DailyR
rankiv.WeeklyR
rankiv.MaleR
rankiv.FemaleR
```

2. 根据 `pixiv` 用户 id 查看相关信息

```python
from pixiver.pixiv import Pixiv
p = Pixiv()
pu = p.user(6415776)
```

查看用户昵称

```
>>> pu.author_name
'...'
```

查看关注总量

```
>>> pu.following_total
...
```

是否是会员

```
>>> pu.premium
...
```

社交链接，返回数据类型： json

```
>>> pu.social
{'twitter': {'url': '...'}}
```

查看其关注用户信息，返回数据类型： json 

```
>>> pu.following_all.first()
{'userId': '...', 'userName': '...', 'profileImageUrl': ...}
```

查看作品 id

```
>>> pu.illusts.first()  # 返回 Works 类
<worksiv.Works object 0x00...>
```

3. 根据作品 ID 浏览相关信息

```
>>> from pixiver.pixiv import Pixiv
>>> p = Pixiv()
>>> pw = p.works(imgid)
```

查看评论

```
>>> pwvc = pw.view_comments()
>>> pwvc.first()['comment']
...
```

评论者的昵称

```
>>> pwvc.first()['userName']
...
```

下一条评论

```
>>> pwvc.next()['comment']
...
```

最后一条评论

```
>>> pwvc.last()['comment']
...
```

原图链接

```
>>> pw.original_url()
...
```

喜欢作品的人数

```
>>> pw.like_count()
...
```

作者昵称

```
>>> pw.author_name()
'...'
```

作品收藏数

```
>>> pw.mark_count()
...
```

作品评论数

```
>>> pw.comment_count()
...
```

4. 其他：

浏览 R-18 排行（暂时不能通过账户及密码登录以获取正确 cookies）

```
>>> from pixiver.pixiv import Pixiv
>>> p = Pixiv(username='username', password='password')
>>> pr = p.rank(20190219, typed='daily_r18')
Pixiver Initializing...
Initialized!
>>> pro = pr.one()
...
```

点赞、收藏、关注

```
>>> from pixiver.pixiv import Pixiv
>>> p = Pixiv(cookie=True, path='../cookie')
>>> pr = p.works(69193024)
>>> pr.like()
Liked!
>>> pr.mark()
Marked!
>>> pr.bookmark()
Bookmarked!
>>> pr.author_name()
'...'
>>>
```

可以下载标签图

```
>>> from pixiver.pixiv import Pixiv
>>> p = Pixiv()
>>> pw = p.works(worksid)
>>> pw.view_tags().first().save_tag_image()
>>>
```

作品的几种尺寸

```
# 查看 mini 图
>>> r.view_mini_image()
...

# 查看 thumb 图
>>> r.view_thumb_image()
...

# 查看 small 图
>>> r.view_small_image()
...

# 查看 regular 图
>>> r.view_regul_image()
...

# 查看原图
>>> r.view_orig_image()
...
```

评论中，空字符 '' 为大表情图，(...) 这类是小表情

暂时不支持以下功能：

 * 查看表情、动图
 * 会员相关功能
 * 命令行版

最后
---

欢迎大家对用法提出更好的意见！

欢迎对指南做更好的补充说明！

欢迎一起做贡献！

谢谢支持！
