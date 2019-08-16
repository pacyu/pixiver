import json
from pixiver import pixiv


def view_img(w):
    w.view_regul_image()


def like(w):
    if w.like():
        print('Save successful!')
    else:
        print('Save Failed!')


def mark(w):
    if w.mark():
        print('Mark successful!')
    else:
        print('Mark Failed!')


def bookmark(w):
    if w.bookmark():
        print('Bookmark successful!')
    else:
        print('Bookmark Failed!')


if __name__ == "__main__":
    # account = json.load(open('../pixiv_user.json'), )
    # p = pixiv.Pixiv(username=account['username'], password=account['password'])
    # w = p.works(76189623)
    # like(w)
    pww = pixiv.worksiv.Works(76189623)
    view_img(pww)
