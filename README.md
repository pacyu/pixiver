pixiver
=======

[![logo1](https://img.shields.io/badge/python-3.6.7-blue.svg)](https://www.python.org/downloads)
[![logo2](https://img.shields.io/badge/requests-2.20.1-green.svg)](https://pypi.org/project/requests/)
![logo6](https://img.shields.io/badge/platform-win7|win10-lightgrey.svg)

这是一个面向 `pixiv` 的网络爬虫

您也可以将其作为当命令行版浏览使用

note: 本地网络以及代理好的话效率是不错的，不然只能多试几次

用例
----

```python
>>> from image import Daily, Weekly, Mouthly, Original, Rookie
>>> r = Daily(20190125)
>>> res = r.run()
# 50 items
>>> res.batch().first()['illust_attrs'].imsize()
(1228, 1736)
>>> res.next().batch().first()['illust_attrs'].imsize()
(1500, 1062)
>>> res.batch().first()['illust_attrs'].original_url()
'https://i.pximg.net/img-original/img/2019/01/24/00/00/05/72810724_p0.jpg'
>>> res.batch().first()['illust_attrs'].mini_url()
'https://i.pximg.net/c/48x48/img-master/img/2019/01/24/00/00/05/72810724_p0_square1200.jpg'
>>> res.batch().first()['illust_attrs'].illust_title()
'森倉円初個展「Girl Friend」メインビジュアル'
>>> res.batch().first()['illust_attrs'].user_name()
'森倉円*初個展2/15-3/6'
>>> res.batch().first()['illust_attrs'].illust_id()
'72810724'
>>> res.batch().first()['illust_attrs'].create_date()
'2019-01-23T15:00:05+00:00'
>>> res.batch().first()['illust_attrs'].upload_date()
'2019-01-23T15:00:05+00:00'
>>> res.batch().first()['illust_attrs'].regular_url()
'https://i.pximg.net/img-master/img/2019/01/24/00/00/05/72810724_p0_master1200.jpg'
>>> res.batch().first()['illust_attrs'].view_count()
103514
>>> res.batch().first()['rank']
1
>>> res.batch().first()['rank_date']
'20190125'
>>> tags = res.batch().first()['illust_attrs'].tags()
>>> tags.first()
{'tag_info': <image.ImageTag object at 0x00000000037ACE48>, 'romaji': 'orijinaru', 'translation': {'en': 'original'}}
...
>>> r = Daily(20190125)
>>> s = r.run()
Crawler Initializing...
Initialized!
>>> g = s.one()
>>> g['illust_attrs'].view_count()
108805
>>> g['illust_attrs'].user_name()
'森倉円*初個展2/15-3/6'
>>> t = g['illust_attrs'].tags()
>>> t.first()
{'tag_info': <image.ImageTag object at 0x00000000037ACE48>, 'romaji': 'orijinaru', 'translation': {'en': 'original'}}
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
>>> g['illust_attrs'].like_count()
14166
>>> g['illust_attrs'].mark_count()
17145
>>> g['illust_attrs'].comment_count()
64
>>> comments = g['illust_attrs'].view_comments()
### 空字符为大表情图
### ()这类是小表情
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

