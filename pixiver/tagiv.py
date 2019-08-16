from requests.compat import unquote_plus
from pixiver import basiciv
from PIL import Image
from io import BytesIO


class WorksTag(basiciv.BasicConfig):

    def __init__(self, tag=None, **kwargs):
        super(WorksTag, self).__init__(**kwargs)
        if tag:
            self.url = 'https://www.pixiv.net/ajax/tag/' \
                       '%s/interface' % tag
            self.im_data = None

            r = self.sess.get(
                self.url,
                headers=self.sess.headers,
                timeout=5
            )
            self.interface = r.json()

            if self.interface['error']:
                raise basiciv.exceptions.AjaxRequestError(
                    self.interface['message']
                )

            if self.interface['body']:
                self.im_tag_url = self.interface['body']['thumbnail']
                self.im_name = self.im_tag_url.split('/')[-1]
                self.illust_id = self.im_name.split('.')[0] \
                    .replace('_p0_master1200', '') \
                    .replace('_p0', '')
            else:
                self.interface['body'] = {
                    'tag': unquote_plus(tag),
                    'abstract': None,
                    'thumbnail': None
                }

    def details(self):
        return self.interface['body']

    def view_tag(self):
        return self.interface['body']['tag']

    def view_abstract(self):
        return self.interface['body']['abstract']

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
        return False
