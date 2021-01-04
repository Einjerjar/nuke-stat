import requests as req

from bs4 import BeautifulSoup

_URL_BASE_PROTOCOL = 'https'
_URL_ROOT = 'hentai2read.com'
_URL_BASE = '{}://{}'.format(_URL_BASE_PROTOCOL, _URL_ROOT)
_H2_VIEW = '{}/{{}}'.format(_URL_BASE)

_SCRAPE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/60.0.3112.90 Safari/537.36 '
}


class H2ReadGalleryInfo:
    def __init__(self, raw_data, gallery_id):
        # open('./sad.html', 'wb').write(raw_data)
        soup = BeautifulSoup(raw_data, 'html.parser')
        self.raw_html = raw_data

        rd = soup.find('ul', class_='list list-simple-mini')
        self.rd = rd

        c_temp = soup.find_all('h3')
        self.title = [x.find('a').text.strip() for x in c_temp if x.find('a')][0]

        self.parody = self.f_tags('Parody')
        self.ranking = self.f_tags('Ranking')
        self.status = self.f_tags('Status')
        self.year = self.f_tags('Release Year')
        self.views = self.f_tags('View')
        self.length = self.f_tags('Page')
        self.author = self.f_tags('Author')
        self.artist = self.f_tags('Artist')
        self.category = self.f_tags('Category')
        self.content = self.f_tags('Content')
        self.character = self.f_tags('Character')
        self.language = self.f_tags('Language')

        self.url = _H2_VIEW.format(gallery_id)
        self.id = gallery_id
        self.cover = soup.find('div', class_='img-container ribbon ribbon-modern ribbon-primary border-black '
                                             'ribbon-left').find('img').attrs['src']

    def f_tags(self, tag):
        # print(tag)
        return [x.text for x in self.rd.find(text=tag).parent.parent.find_all('a') if x.text != '-']

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.__str__()


class H2Read:
    ident = 'h2'

    @staticmethod
    def try_parse_link(link):
        f_link = link
        sp = f_link.split('/')

        if f_link.startswith(_URL_ROOT):
            f_link = sp[2]
        elif f_link.startswith('h2'):
            f_link = sp[1]

        return f_link

    @classmethod
    def get_gallery_info(cls, link):
        gallery_id = cls.try_parse_link(link)

        r_data = req.get(_H2_VIEW.format(gallery_id), headers=_SCRAPE_HEADERS)
        r_content = None

        try:
            r_content = r_data.content.decode('utf-8')
            # print('r_content, utf8')
        except Exception:
            try:
                r_content = r_data.content.decode('cp1252')
                # print('r_content, cp1252')
            except Exception:
                r_content = r_data.content.decode('cp1252')
                # print('r_content, cp1252')

        return H2ReadGalleryInfo(r_data.content, gallery_id)


if __name__ == '__main__':
    a = H2Read.get_gallery_info('koiito_kinenbi')
    print(a.title)
    print(a.cover)
