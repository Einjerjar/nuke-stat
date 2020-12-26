import requests as req

from bs4 import BeautifulSoup

_URL_BASE_PROTOCOL = 'https'
_URL_ROOT = 'hentai.cafe/hc.fyi'
_URL_BASE = '{}://{}'.format(_URL_BASE_PROTOCOL, _URL_ROOT)

_SCRAPE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
}

_HC_VIEW = '{}/{{}}'.format(_URL_BASE)


class HCafeGalleryInfo:
    def __init__(self, raw_data, gallery_id):
        open('sad.html', 'w').write(raw_data)
        soup = BeautifulSoup(raw_data, 'html.parser')
        self.raw_html = raw_data

        rd = soup.find('p')
        self.rd = rd

        self.title = soup.find('h3').text
        self.url = _HC_VIEW.format(gallery_id)
        self.id = gallery_id
        self.cover = soup.find('img').attrs['src']
        self.tags = []
        self.artists = []

        tags = soup.find_all('a', {'rel': 'tag'})

        for j in tags:
            if '/tag/' in j.attrs['href']:
                jt = j.text
                if jt not in self.tags:
                    self.tags.append(jt)
            if '/artist/' in j.attrs['href']:
                self.artists.append(j.text)

        read = soup.find('a', {'class': 'x-btn'}).attrs['href']

        f_read = req.get(read, headers=_SCRAPE_HEADERS)

        f_soup = BeautifulSoup(f_read.content.decode('utf-8'), 'html.parser')
        page_count = f_soup.find('div', {'class': 'tbtitle'}).find_all('a')

        self.length = len(page_count)

    def __repr__(self):
        pass

    def __str__(self):
        return self.title


class HCafe:
    @staticmethod
    def try_parse_link(link):
        f_link = link
        sp = f_link.split('/')

        if f_link.startswith(_URL_ROOT):
            f_link = sp[2]
        elif f_link.startswith('hc.fyi'):
            f_link = sp[1]
        elif f_link.startswith('hc'):
            f_link = sp[1]

        return f_link

    @classmethod
    def get_gallery_info(cls, link):
        gallery_id = cls.try_parse_link(link)

        r_data = req.get(_HC_VIEW.format(gallery_id), headers=_SCRAPE_HEADERS)

        return HCafeGalleryInfo(r_data.content.decode('utf-8'), gallery_id)


if __name__ == '__main__':
    u = ['hentai.cafe/hc.fyi/1457', 'hc.fyi/1457', 'hc/1457']
    for i in u:
        print(HCafe.try_parse_link(i), i)

    hc = HCafe.get_gallery_info('hc/1457')
    print(hc.title)
