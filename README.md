pixiver
=======

这是一个面向 `pixiv` 的网络爬虫，您也可以将其作为当命令行版浏览使用。

目前还有一些功能尚未完成：

 * 使用个人账户 cookie 来完成作品收藏、点赞功能、关注喜欢的作者等功能
 * 会员相关功能
 * 命令行版

特点 & 用例
----------

 + 可浏览 pixiv 每日、每周、每月、新人、原创、受男性欢迎、受女性欢迎、受男性欢迎 + R-18、受女性欢迎 + R-18排行版作品。

 + 可浏览作品下的所有评论。

 + 可浏览作品标签、排名、点赞数、收藏数等信息。

 + 可根据用户 id 获取相关信息：

```python
>>> from pixiver.user import User
>>> r = User(6415776)
Crawler Initializing...
Initialized!

### 查看用户昵称
>>> r.username
'ファルケン@'

### 查看关注总量
>>> r.following_total
548

### 是否是会员
>>> r.premium
True

### 社交链接
>>> r.social
{'twitter': {'url': 'https://twitter.com/YutoZin'}}

### 查看第一条关注用户信息
>>> r.following_all.first()
{'userId': '490219', 'userName': 'Hiten', 'profileImageUrl': ...}

### 
>>> r.following_all.first()['userName']
'Hiten'

### 查看作品 id
>>> r.illusts.first()
'72318445'
>>> r.illusts.next()
'72147871'
>>> 

```

 + 可根据图片 id 获取相关信息：

```python
>>> from pixiver import imageiv
>>> pi = imageiv.PixivImage(72773786)

### 查看评论
>>> comm.first()['comment']
'face can be better'

### 查看原图链接
>>> pi.original_url()
'https://i.pximg.net/img-original/img/2019/01/21/18/00/12/72773786_p0.jpg'

### 查看喜欢作品的人数
>>> pi.like_count()
12183

### 作者昵称
>>> pi.user_name()
'河CY'

### 作品收藏数
>>> pi.mark_count()
14370

### 作品评论数
>>> pi.comment_count()
64

### 查看评论
>>> comm = pi.view_comments()

### 第一条评论
>>> comm.first()['comment']
'face can be better'

### 第一条评论的用户昵称
>>> comm.first()['userName']
'...'

### 下一条评论
>>> comm.next()['comment']
''
>>> comm.next()['comment']
'(heart)'
>>> comm.next()['comment']
'wsl'
...
>>>

```

 + 可下载作品：

```python
>>> from pixiver import imageiv
>>> r = imageiv.Daily(20190122)
Crawler Initializing...
Initialized!
>>> gon = r.one()

### 查看作者昵称
>>> gon['illust_attrs'].user_name()
'河CY'

### 查看排名
>>> gon['rank']
1

### 原图链接
>>> gon['illust_attrs'].original_url()
'https://i.pximg.net/img-original/img/2019/01/21/18/00/12/72773786_p0.jpg'

### 喜欢就保存一个
>>> gon['illust_attrs'].save_original()
Saved!
>>>

```

 + 提供许多 api，可扩展到自己的项目：

为了保证对代理用户的使用性的良好，提供了两种方式浏览排行榜:

1. 按批次加载：`batch()` 一次将加载排行榜 50 个进行处理。对于网络不好的使用者来说，这可能会很头痛。但我还提供了另外一个方法2。
2. 一次一条加载：`one()` 一次加载排行榜的 1 个，并加入到队列中，这样依然能使用 `batch()` 一样的功能。

 - `batch()`:
```python
>>> from pixiver.imageiv import(
Daily, Weekly, Mouthly, Original,
Rookie, Male, Female, MaleR, FemaleR
)
>>> r = Daily()
>>> res = r.run(20190125)
Crawler Initializing...
Initialized!

### batch() 一次性加载 50 个对象
b = res.batch()

### 查看第一个图像尺寸

>>> b.first()['illust_attrs'].imsize()
(1228, 1736)

### 查看下一个图像尺寸
>>> b.next()['illust_attrs'].imsize()
(1500, 1062)

### 查看第一个作品原图链接
>>> b.first()['illust_attrs'].original_url()
'https://i.pximg.net/img-original/img/2019/01/24/00/00/05/72810724_p0.jpg'

### 查看第一个作品迷你图链接
>>> b.first()['illust_attrs'].mini_url()
'https://i.pximg.net/c/48x48/img-master/img/2019/01/24/00/00/05/72810724_p0_square1200.jpg'

### 作品标题
>>> b.first()['illust_attrs'].illust_title()
'森倉円初個展「Girl Friend」メインビジュアル'

### 作者昵称
>>> b.first()['illust_attrs'].user_name()
'森倉円*初個展2/15-3/6'

### 作品 id
>>> b.first()['illust_attrs'].illust_id()
'72810724'

### 作品创建日期（未作处理）
>>> b.first()['illust_attrs'].create_date()
'2019-01-23T15:00:05+00:00'

### 作品上传日期（未作处理）
>>> b.first()['illust_attrs'].upload_date()
'2019-01-23T15:00:05+00:00'

### 作品链接（这类图尺寸应该是除原图外，质量最好的）
>>> b.first()['illust_attrs'].regular_url()
'https://i.pximg.net/img-master/img/2019/01/24/00/00/05/72810724_p0_master1200.jpg'

### 查看作品浏览数
>>> b.first()['illust_attrs'].view_count()
103514

### 查看作品排名
>>> b.first()['rank']
1

### 查看排名日期
>>> b.first()['rank_date']
'20190125'

### 查看作品标签
>>> tags = b.first()['illust_attrs'].tags()
>>> tags.first()
{'tag_info': <image.ImageTag object at 0x00000000037ACE48>, 'romaji': 'orijinaru', 'translation': {'en': 'original'}}

### 一种更快的获取所有标签的方法

>>> for tag in b.first()['illust_attrs'].all()['tags']['tags']:
...     print(tag['tag'])
...
オリジナル
女の子
桜
なにこれ可愛い
桜の花
美少女
ロングヘアー
>>>

```

 - `one()`:

```python
>>> r = Daily(20190125)
Crawler Initializing...
Initialized!
>>> g = r.one()

### 用法一样很简单
>>> g['illust_attrs'].view_count()
108805

### 
>>> g['illust_attrs'].user_name()
'森倉円*初個展2/15-3/6'

### 
>>> t = g['illust_attrs'].tags()
>>> t.first()
{'tag_info': <image.ImageTag object at 0x00000000037ACE48>, 'romaji': 'orijinaru', 'translation': {'en': 'original'}}

###
>>> t.first()['tag_info'].get_info()
{'tag': 'オリジナル', 'abstract': '独自に創作したもの。', 'thumbnail': 'https://i.pximg.net/c/384x280_80_a2_g2/img-master/img/2010/01/28/15/28/49/8431682_p0_master1200.jpg'}

>>> t.first()['tag_info'].get_info()['tag']
'オリジナル'

### 一种更快的获取所有标签的方法

>>> for tag in g['illust_attrs'].all()['tags']['tags']:
...     print(tag['tag'])
...
オリジナル
女の子
桜
なにこれ可愛い
桜の花
美少女
ロングヘアー

### 查看喜欢数
>>> g['illust_attrs'].like_count()
14166

### 查看收藏数
>>> g['illust_attrs'].mark_count()
17145

### 查看评论数
>>> g['illust_attrs'].comment_count()
64

### 查看评论
### 空字符 '' 为大表情图
### (...) 这类是小表情

>>> comments = g['illust_attrs'].view_comments()
>>> comments.first()['comment']
''
>>> comments.next()['comment']
'観に行く！'
>>> comments.next()['comment']
'好看(sweat4)(sweat4)'
>>> comments.next()['comment']
'自分が外国人なのが一番残念ですね。\n日本までテレポートできればいいのに( ´•ω•` )'
>>> comments.next()['comment']
'Ooooooooh mah G A D'
>>> comments.next()['comment']
'素晴らしい'
>>> comments.next()['comment']
'可真棒'
>>> comments.next()['comment']
''
>>> comments.next()['comment']
'長い髪が舞うかわいい女の子'
>>> comments.next()['comment']
'好看好看'
>>> comments.next()['comment']
'感觉不错\n'
>>> comments.next()['comment']
''
>>> comments.next()['comment']
'好惊艳啊。。。'
>>> comments.next()['comment']
'벚꽃에 둘러싸여 찰랑이는 긴머리를 흩날리며 웃는 갈색머리의 아가씨 정말 예쁘군요♡♡'
>>>

```

