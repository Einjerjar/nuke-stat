import requests as req

from bs4 import BeautifulSoup


_URL_BASE_PROTOCOL = 'https'
_HN_URL_ROOT = 'hentainexus.com'
_HN_URL_BASE = '{}://{}'.format(_URL_BASE_PROTOCOL, _HN_URL_ROOT)
_HN_VIEW = '{}/view/{{}}'.format(_HN_URL_BASE)


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
                if hasattr(x, 'find_all') and len(x.find_all('span', {'class':'tag'})) > 0:
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


class HNexus:
    @staticmethod
    def try_parse_g_id(g_id):
        f_id = g_id
        f_s = f_id.split('/')
        if f_id.startswith('http'):
            f_id = f_s[4]
        elif f_id.startswith('hentainexus.com'):
            f_id = f_s[2]
        elif f_id.startswith('hn'):
            f_id = f_s[1]
        return f_id

    @classmethod
    def get_gallery_info(cls, link):
        f_id = cls.try_parse_g_id(link)
        r_data = req.get(_HN_VIEW.format(f_id), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 ('
                                                      'KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'})
        return HNexusGalleryInfo(r_data.content.decode('utf-8'))


if __name__ == '__main__':
    url = 'https://hentainexus.com/view/8200'
    x = HNexus.get_gallery_info(url)
    print(x.cover, x.title, x.id, x.url)