# import os
# import pymysql
# import pixiver
# import time
# import sys
# import __init__
#
#
# if __name__ == '__main__':
#     date = time.strftime('%Y%m%d', time.localtime())
#     args = {
#         '-m': [int(date) - 2, int(date) - 1], '-p': 1,
#         '-s': 'o', '-n': 5, '-l': 2, '-o': '', '-db': None
#     }
#
#     i = 1
#     while i < len(sys.argv):
#         if sys.argv[i] == '-m':
#             i += 1
#             args['-m'][0] = int(sys.argv[i])
#             i += 1
#             args['-m'][1] = int(sys.argv[i])
#         if sys.argv[i] == '-p':
#             i += 1
#             args['-p'] = int(sys.argv[i])
#         if sys.argv[i] == '-s':
#             i += 1
#             args['-s'] = sys.argv[i]
#         if sys.argv[i] == '-n':
#             i += 1
#             args['-n'] = int(sys.argv[i])
#         if sys.argv[i] == '-l':
#             i += 1
#             args['-l'] = int(sys.argv[i])
#         if sys.argv[i] == '-o':
#             i += 1
#             args['-o'] = sys.argv[i]
#         if sys.argv[i] == '-db':
#             i += 4
#             db = pymysql.connect(
#                 host=sys.argv[i - 3],
#                 user=sys.argv[i - 2],
#                 password=sys.argv[i - 1],
#                 db=sys.argv[i],
#                 charset='utf8mb4'
#             )
#             args['-db'] = db
#
#         i += 1
#
#     if args['-o'] == '':
#         if not os.path.exists('pixiv'):
#             print('请指定参数 -o ，用法见 __init__.py 文件')
#             print('或者，在当前目录下创建一个`pixiv`文件以存放图片')
#             print('项目目录结构：')
#             print('> crawlers')
#             print('> crawlers > pixiv')
#             print('> crawlers > pixiv > smalls')
#             print('> crawlers > pixiv > middles')
#             print('> crawlers > pixiv > origins')
#             print('> crawlers > __init__.py')
#             print('> crawlers > run.py')
#             print('> crawlers > pixiver.py')
#             print('> crawlers > README.md')
#             exit(1)
#
#     try:
#         with open('out.txt', 'a'):
#             pass
#     except FileNotFoundError:
#         with open('out.txt', 'w'):
#             pass
#
#     if len(sys.argv) < 2:
#         spider = pixiver.PixivCrawler(
#             start_date=int(date) - 2,
#             end_date=int(date) - 1,
#         )
#         spider.run()
#     else:
#         spider = pixiver.PixivCrawler(
#             start_date=args['-m'][0],
#             end_date=args['-m'][1],
#             page_numbers=args['-p'],
#             img_size=args['-s'],
#             speed=args['-n'],
#             delay=args['-l'],
#             output=args['-o'],
#             db=args['-db'])
#         spider.run()
#
#         try:
#             args['-db'].close()
#         except:
#             pass

from imageiv import Daily

# url = 'https://www.pixiv.net/member_illust.php?mode=manga_big&illust_id=72629798&page=0'
#
# b = Pixiv('darkchii', 'ngc6357', return_to=url)
#

r = Daily(20190125)

res = r.run()
tag = res['illust_attrs'].tags().first().get_info()

print(tag['tag'])
# print(r.json())
