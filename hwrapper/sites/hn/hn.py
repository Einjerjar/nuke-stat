import requests as req

from bs4 import BeautifulSoup

_URL_BASE_PROTOCOL = 'https'
_URL_ROOT = 'hentainexus.com'
_URL_BASE = '{}://{}'.format(_URL_BASE_PROTOCOL, _URL_ROOT)

_SCRAPE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
}

_HN_VIEW = '{}/view/{{}}'.format(_URL_BASE)


class HNexusGalleryInfo:
    def __init__(self, raw_data):
        soup = BeautifulSoup(raw_data, 'html.parser')
        self.raw_html = raw_data
        rd = {}

        rows = soup.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            temp = [x for x in cols[1] if x != '\n' and x != ' ']
            for i in range(len(temp)):
                x = temp[i]
                if hasattr(x, 'find_all') and len(x.find_all('span', {'class': 'tag'})) > 0:
                    temp[i] = x.find('a')
            temp = [x.text.strip() if hasattr(x, 'find_all') else x.strip() for x in temp]
            rd[cols[0].text] = ', '.join(temp)

        self.raw_data = rd
        self.title = soup.find('h1', {'class': 'title'}).text
        self.artist = rd['Artist'] or ''
        self.language = rd['Language'] or ''
        self.magazine = rd['Magazine'] or ''
        self.parody = rd['Parody'] or ''
        self.publisher = rd['Publisher'] or ''
        self.length = int(rd['Pages'])
        self.tags = rd['Tags'].split(', ')
        self.desc = rd['Description']
        cover = soup.find('figure').find('img')
        self.cover = cover.attrs['src']
        self.id = cover.find_parent('a').attrs['href'].split('/')[2]
        self.url = _HN_VIEW.format(self.id)

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title


class HNexus:
    ident = 'hn'

    @staticmethod
    def try_parse_link(link):
        f_link = link
        sp = f_link.split('/')

        if f_link.startswith(_URL_ROOT):
            f_link = sp[2]
        elif f_link.startswith('hn'):
            f_link = sp[1]
        return f_link

    @classmethod
    def get_gallery_info(cls, link):
        gallery_id = cls.try_parse_link(link)

        r_data = req.get(_HN_VIEW.format(gallery_id), headers=_SCRAPE_HEADERS)
        return HNexusGalleryInfo(r_data.content.decode('utf-8'))


if __name__ == '__main__':
    u = ['hentainexus.com/view/8200', 'hn/8200']
    for i in u:
        print(HNexus.try_parse_link(i), i)
    url = 'https://hentainexus.com/view/8200'
