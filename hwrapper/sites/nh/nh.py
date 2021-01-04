import json
from enum import Enum, auto

import requests as req

_URL_BASE_PROTOCOL = 'https'
_URL_ROOT = 'nhentai.net'
_URL_BASE = '{}://{}'.format(_URL_BASE_PROTOCOL, _URL_ROOT)
_NH_URL_API_G = '{}/api/gallery/{{}}'.format(_URL_BASE)
_NH_URL_GAL = '{}/g/{{}}'.format(_URL_BASE)

_NH_THUMB_PRE = 't'
_NH_IMG_PRE = 'i'

_NH_URL_COVER = '{}://{}.{}/galleries/{{}}/cover.{{}}'.format(_URL_BASE_PROTOCOL, _NH_THUMB_PRE, _URL_ROOT)
_NH_URL_THUMB = '{}://{}.{}/galleries/{{}}/thumbnail.{{}}'.format(_URL_BASE_PROTOCOL, _NH_THUMB_PRE, _URL_ROOT)
_NH_URL_IMG = '{}://{}.{}/galleries/{{}}/{{}}.{{}}'.format(_URL_BASE_PROTOCOL, _NH_IMG_PRE, _URL_ROOT)

_NH_URL_TAG = '{}{{}}'.format(_URL_BASE)


class NHPageExts(Enum):
    PNG = 'p'
    GIF = 'g'
    JPG = 'j'

    @classmethod
    def get_type(cls, t):
        return cls(t)

    @classmethod
    def get_ext(cls, t):
        return cls(t).name.lower()


class NHPageTypes(Enum):
    PAGE = auto()
    COVER = auto()
    THUMB = auto()


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


class NHTitle:
    def __init__(self, titles):
        self.en = titles['english']
        self.jp = titles['japanese']
        self.pr = titles['pretty']


class NHPage:
    def __init__(self, page, media_id, index=0, p_type=NHPageTypes.PAGE):
        self.raw_type = page['t']
        self.width = page['w']
        self.height = page['h']
        self.p_type = p_type
        self.ext = NHPageExts.get_ext(self.raw_type)
        self.media_id = media_id
        self.index = index

    def __repr__(self):
        if self.p_type is NHPageTypes.COVER:
            return _NH_URL_COVER.format(self.media_id, self.ext)
        elif self.p_type is NHPageTypes.THUMB:
            return _NH_URL_THUMB.format(self.media_id, self.ext)

        return _NH_URL_IMG.format(self.media_id, self.index + 1, self.ext)


class NHTag:
    def __init__(self, tag):
        self.tag_id = tag['id']
        self.raw_type = tag['type']
        self.t_type = NHTagTypes.get_type(tag['type'])
        self.name = tag['name']
        self.url = _NH_URL_TAG.format(tag['url'])
        self.count = tag['count']


class NHGalleryInfo:
    def __init__(self, raw_data):
        rd = json.loads(raw_data)
        self.raw_data = rd
        self.valid = True

        if 'error' in rd:
            self.valid = False
            return

        self.id = rd['id']
        self.media_id = rd['media_id']
        self.title = NHTitle(rd['title'])
        self.page_info = [NHPage(rd['images']['pages'][i], self.media_id, index=i) for i in
                          range(len(rd['images']['pages']))]
        self.cover = NHPage(rd['images']['cover'], self.media_id, p_type=NHPageTypes.COVER)
        self.thumb = NHPage(rd['images']['thumbnail'], self.media_id, p_type=NHPageTypes.THUMB)
        self.scanlator = rd['scanlator']
        self.tags = [NHTag(x) for x in rd['tags']]
        self.length = rd['num_pages']
        self.fav_count = rd['num_favorites']
        self.uploaded = rd['upload_date']
        self.url = _NH_URL_GAL.format(self.id)

    def __repr__(self):
        return '[{}] {}'.format(self.id, self.title.en)

    def __str__(self):
        return self.title

    def filer_tags_raw(self, t_type):
        return [x for x in self.tags if x.t_type == t_type]

    def filer_tags(self, t_type):
        return ', '.join([x.name for x in self.filer_tags_raw(t_type)])


class NHentai:
    ident = 'nh'

    @staticmethod
    def try_parse_link(link):
        f_id = link
        sp = f_id.split('/')

        if f_id.startswith(_URL_ROOT):
            f_id = int(sp[2])
        elif f_id.startswith('g/') or f_id.startswith('nh/'):
            f_id = int(sp[1])
        elif f_id.startswith(_URL_ROOT):
            f_id = int(sp[2])
        return str(f_id)

    @classmethod
    def get_gallery_info(cls, link):
        gallery_id = cls.try_parse_link(link)

        r_data = req.get(_NH_URL_API_G.format(gallery_id))
        return NHGalleryInfo(r_data.content.decode('utf-8'))


if __name__ == '__main__':
    u = ['nhentai.net/g/339083', 'g/339083', 'nh/339083']
    for i in u:
        print(NHentai.try_parse_link(i), i)
