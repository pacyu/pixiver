from requests.compat import unquote_plus
from pixiver import exceptions
from pixiver import baseiv
from PIL import Image
from io import BytesIO


class ImageTag(baseiv.ConfigHeaders):

    def __init__(self, tag):
        super().__init__()
        self.url = 'https://www.pixiv.net/ajax/tag/' \
                   '%s/info' % tag
        self.im_data = None

        r = self.sess.get(
            self.url,
            headers=self.sess.headers,
            timeout=5
        )
        self.info_json = r.json()

        if self.info_json['error']:
            raise exceptions.AjaxRequestError(
                self.info_json['message']
            )

        if self.info_json['body']:
            self.im_tag_url = self.info_json['body']['thumbnail']
            self.im_name = self.im_tag_url.split('/')[-1]
            self.illust_id = self.im_name.split('.')[0] \
                .replace('_p0_master1200', '') \
                .replace('_p0', '')
        else:
            self.info_json['body'] = {
                'tag': unquote_plus(tag),
                'abstract': None,
                'thumbnail': None
            }

    def tag_info(self):
        return self.info_json['body']

    def view_tag(self):
        return self.info_json['body']['tag']

    def view_abstract(self):
        return self.info_json['body']['abstract']

    def view_thumbnail_image(self):
        if not self.im_data:
            headers = {
                'Referer': 'https://www.pixiv.net/member_illust.php?'
                           'mode=medium&illust_id=' + self.illust_id,
            }
            rg = self.sess.get(
                self.im_tag_url,
                headers=headers,
                timeout=2
            )
            self.im_data = rg.content

        im = Image.open(BytesIO(self.im_data))
        im.show()

    def save_tag_image(self):
        if not self.im_data:
            headers = {
                'Referer': 'https://www.pixiv.net/member_illust.php?'
                           'mode=medium&illust_id=' + self.illust_id,
            }
            rg = self.sess.get(
                self.im_tag_url,
                headers=headers,
                timeout=2)
            self.im_data = rg.content

        with open(self.im_name, 'wb') as f:
            f.write(self.im_data)
        print('Saved!')
