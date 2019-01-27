pixiver
=======

这是一个面向 `pixiv` 的网络爬虫，您也可以将其作为当命令行版浏览使用。

目前还有一些功能尚未完成：

    使用自己账户 cookie 来完成作品收藏、点赞功能、关注喜欢的作者。
    
    会员相关功能。

特点 & 用例
----------

可浏览 pixiv 每日、每周、每月、新人、原创、受男性欢迎、受女性欢迎、受男性欢迎 + R-18、受女性欢迎 + R-18排行。

可浏览作品下的所有评论。

可浏览作品标签、排名、点赞数、收藏数等信息。

可根据用户 id 获取相关信息：

```python
>>> from pixiver.user import User
>>> r = User(6415776)
Crawler Initializing...
Initialized!
>>> r.username
'ファルケン@'
>>> r.following_total
548
>>> r.premium
True
>>> r.social
{'twitter': {'url': 'https://twitter.com/YutoZin'}}
>>> r.following_all.first()
{'userId': '490219', 'userName': 'Hiten', 'profileImageUrl': 'https://i.pximg.net/user-pro
file/img/2019/01/08/15/39/34/15232824_c72927b1f26546d25e0f5f6e20fb1764_170.png', 'userComm
ent': "イラストレーター、台湾人。東京在住。\r\n\r\n◆お仕事履歴►http://www.hitenkei.net/pr
ofile.html\r\n\r\n\r\n◆ご依頼、連絡はHPのプロフィールを確認の上メールにてお願いいたします
。\u3000\r\n\u3000\r\n※お仕事を募集しておりません。\r\n※目前無法承接任何新規的委託案件\r
\nhttp://www.hitenkei.net/profile.html\r\n\r\n\r\n►Twitter\r\nhttps://twitter.com/HitenKei
\r\n\r\n------------------------------------------------------\r\n\r\n◆現在マイピクは募集
しておりません。\r\n// 目前不接受加好友的請求，謝謝。 \r\n// I don't accept any MyPixiv re
quest currently, thanks.\r\n\r\n◆＊個人使用範囲（イラストを裁断し、SNSアイコン、ヘッター
や壁紙は問題ありません、※PC壁紙、待受は私用のみ、ネットにアップするのはご遠慮ください）以
外\r\nイラストに対しての裁断、加工、転載は禁止です。\r\n加工、画像の使用許可メッセージには
基本的に返事しません、\r\nまたイラストの「加工」をどうぞご遠慮ください。\r\n\r\n// 除了作
為個人頭像、手機或電腦桌布使用以外，\r\n請不要以任何形式轉載或加工我的作品；\r\n恕不回應徵
求轉載或加工許可的信件，謝謝。\r\n\r\n// Feel free to use my works for private use such as
 SNS icon \r\nor wallpaper, but please don't repost my works on other sites or remakes, th
anks:)", 'following': False, 'isBlocking': False, 'illusts': [{'id': '72445878', 'title':
'あけおめ！', 'illustType': 0, 'xRestrict': 0, 'restrict': 0, 'sl': 2, 'description': '',
'url': 'https://i.pximg.net/c/250x250_80_a2/img-master/img/2019/01/02/02/11/34/72445878_p0
_square1200.jpg', 'tags': ['オリジナル', '女の子', '着物', '文句無しに可愛い', 'ウリ坊', '
オリジナル10000users入り', '視線'], 'userId': '490219', 'width': 1000, 'height': 1480, 'pa
geCount': 1, 'isBookmarkable': True, 'bookmarkData': None}, {'id': '72300463', 'title': '
偽装', 'illustType': 0, 'xRestrict': 0, 'restrict': 0, 'sl': 2, 'description': '', 'url':
'https://i.pximg.net/c/250x250_80_a2/img-master/img/2018/12/26/00/00/03/72300463_p0_square
1200.jpg', 'tags': ['オリジナル', 'C95', '水仙', '茶髪ロング', 'オリジナル10000users入り',
 '彼女の世界', 'ハイヒール'], 'userId': '490219', 'width': 1412, 'height': 1000, 'pageCoun
t': 1, 'isBookmarkable': True, 'bookmarkData': None}, {'id': '72264526', 'title': '『聖語
の皇弟と魔剣の騎士姫\u3000～蒼雪のクロニクル～   Ⅰ』', 'illustType': 0, 'xRestrict': 0, '
restrict': 0, 'sl': 2, 'description': '', 'url': 'https://i.pximg.net/c/250x250_80_a2/img-
master/img/2018/12/24/14/45/48/72264526_p0_square1200.jpg', 'tags': ['オリジナル', '仕事絵
', '聖語の皇弟と魔剣の騎士姫', 'ラノベ', 'カロリーナ=マルヴァレフト', '氷乃華雪音', '蒼生=
カレン=ブラッドフォード', '蒼空'], 'userId': '490219', 'width': 1000, 'height': 1403, 'pag
eCount': 2, 'isBookmarkable': True, 'bookmarkData': None}, {'id': '72217608', 'title': 'C9
5新刊『Re:IMPERMANENT』', 'illustType': 0, 'xRestrict': 0, 'restrict': 0, 'sl': 2, 'descri
ption': '', 'url': 'https://i.pximg.net/c/250x250_80_a2/img-master/img/2018/12/22/00/00/56
/72217608_p0_square1200.jpg', 'tags': ['オリジナル', 'C95', '視線', '水仙', '茶髪ロング',
'オリジナル10000users入り'], 'userId': '490219', 'width': 851, 'height': 1200, 'pageCount'
: 3, 'isBookmarkable': True, 'bookmarkData': None}], 'novels': []}
>>> r.following_all.first()['userName']
'Hiten'
>>> r.illusts.first()
'72318445'
>>> r.illusts.next()
'72147871'
>>> 

```

可根据图片 id 获取相关信息：

```python
>>> from pixiver import imageiv
>>> pi = imageiv.PixivImage(72773786)
>>> comm.first()['comment']
'face can be better'
>>> pi.original_url()
'https://i.pximg.net/img-original/img/2019/01/21/18/00/12/72773786_p0.jpg'
>>> pi.like_count()
12183
>>> pi.user_name()
'河CY'
>>> pi.mark_count()
14370
>>> pi.comment_count()
64
>>> comm = pi.view_comments()
>>> comm.first()['comment']
'face can be better'
>>> comm.next()['comment']
''
>>> comm.next()['comment']
'(heart)'
>>> comm.next()['comment']
'wsl'
...
```

可下载作品：

```python
>>> from pixiver import imageiv
>>> r = imageiv.Daily(20190122)
Crawler Initializing...
Initialized!
>>> gon = r.one()
>>> gon['illust_attrs'].user_name()
'河CY'
>>> gon['rank']
1
>>> gon['illust_attrs'].original_url()
'https://i.pximg.net/img-original/img/2019/01/21/18/00/12/72773786_p0.jpg'
>>> gon['illust_attrs'].save_original()
Saved!
>>>

```

提供许多 api，可扩展到自己的项目。

```python
>>> from pixiver.imageiv import(
Daily, Weekly, Mouthly, Original,
Rookie, Male, Female, MaleR, FemaleR
)
>>> r = Daily()
>>> res = r.run(20190125)
Crawler Initializing...
Initialized!
>>> res.batch().first()['illust_attrs'].imsize() # 50 items
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
Crawler Initializing...
Initialized!
>>> g = r.one()
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

