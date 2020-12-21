import requests as req
import json

from enum import Enum, unique, auto


class NHPageTypes(Enum):
    PNG = 'p'
    GIF = 'g'
    JPG = 'j'

    @classmethod
    def get_type(cls, t):
        return cls(t)

    @classmethod
    def get_ext(cls, t):
        return cls(t).name.lower()


class NHTagTypes(Enum):
    LANG = 'language'
    PARODY = 'parody'
    GROUP = 'group'
    ARTIST = 'artist'
    CHARACTER = 'character'
    CATEGORY = 'category'
    TAG = 'tag'

    @classmethod
    def get_type(cls, t):
        return cls(t)


_NH_URL_BASE = 'https://nhentai.net'
_NH_URL_API = 'api/gallery'
_NH_URL_GAL = 'g'

_NH_URL_COVER = 'https://t.nhentai.net/galleries/{}/cover.{}'


class NHTitle:
    def __init__(self, titles):
        self.en = titles['english']
        self.jp = titles['japanese']
        self.pr = titles['pretty']


class NHPage:
    def __init__(self, page):
        self.raw_type = page['t']
        self.width = page['w']
        self.height = page['h']
        self.type = NHPageTypes.get_ext(self.raw_type)


class NHTag:
    def __init__(self, tag):
        self.tag_id = tag['id']
        self.raw_type = tag['type']
        self.type = NHTagTypes.get_type(tag['type'])
        self.name = tag['name']
        self.url = tag['url']
        self.count = tag['count']


class NHGalleryInfo:
    def __init__(self, raw_data):
        rd = json.loads(raw_data)
        self.raw_data = rd
        self.id = rd['id']
        self.media_id = rd['media_id']
        self.title = NHTitle(rd['title'])
        self.page_info = [NHPage(x) for x in rd['images']['pages']]
        self.cover = NHPage(rd['images']['cover'])
        self.thumb = NHPage(rd['images']['thumbnail'])
        self.scanlator = rd['scanlator']
        self.tags = [NHTag(x) for x in rd['tags']]
        self.length = rd['num_pages']
        self.fav_count = rd['num_favorites']

    def get_cover_url(self):
        return _NH_URL_COVER.format(self.media_id, self.cover.type)


class NHentai:
    def __init__(self):
        pass

    @staticmethod
    def get_gallery_info(g_id):
        r_data = req.get('{}/{}/{}'.format(_NH_URL_BASE, _NH_URL_API, g_id))
        return NHGalleryInfo(r_data.content.decode('utf-8'))


if __name__ == '__main__':
    NHentai.get_gallery_info(316574)
