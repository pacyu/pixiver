from imageiv import Daily


r = Daily(20190125)
res = r.one()
tag = res['illust_attrs'].tags().first().get_info()
print(tag['tag'])
