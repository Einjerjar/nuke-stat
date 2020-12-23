import json
import requests as req

from enum import Enum, auto

_URL_BASE_PROTOCOL = 'https'
_NH_URL_ROOT = 'nhentai.net'
_NH_URL_BASE = '{}://{}'.format(_URL_BASE_PROTOCOL, _NH_URL_ROOT)
_NH_URL_API_G = '{}/api/gallery/{{}}'.format(_NH_URL_BASE)
_NH_URL_GAL = '{}/g/{{}}'.format(_NH_URL_BASE)

_NH_THUMB_PRE = 't'
_NH_IMG_PRE = 'i'

_NH_URL_COVER = '{}://{}.{}/galleries/{{}}/cover.{{}}'.format(_URL_BASE_PROTOCOL, _NH_THUMB_PRE, _NH_URL_ROOT)
_NH_URL_THUMB = '{}://{}.{}/galleries/{{}}/thumbnail.{{}}'.format(_URL_BASE_PROTOCOL, _NH_THUMB_PRE, _NH_URL_ROOT)
_NH_URL_IMG = '{}://{}.{}/galleries/{{}}/{{}}.{{}}'.format(_URL_BASE_PROTOCOL, _NH_IMG_PRE, _NH_URL_ROOT)

_NH_URL_TAG = '{}{{}}'.format(_NH_URL_BASE)


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

    def filer_tags_raw(self, t_type):
        return [x for x in self.tags if x.t_type == t_type]

    def filer_tags(self, t_type):
        return ', '.join([x.name for x in self.filer_tags_raw(t_type)])


class NHentai:
    def __init__(self):
        pass

    @staticmethod
    def try_parse_g_id(g_id):
        f_id = g_id
        if type(f_id) == str:
            try:
                f_id = int(f_id)
            except ValueError:
                if f_id.startswith('<'):
                    f_id = f_id[1:-1]
                if f_id.startswith('http'):
                    f_id = int(f_id.split('/')[4])
                elif f_id.startswith('g/'):
                    f_id = int(f_id.split('/')[1])
                elif f_id.startswith(_NH_URL_ROOT):
                    f_id = int(f_id.split('/')[2])
        return f_id

    @classmethod
    def get_gallery_info(cls, g_id):
        f_id = cls.try_parse_g_id(g_id)

        r_data = req.get(_NH_URL_API_G.format(str(f_id)))
        return NHGalleryInfo(r_data.content.decode('utf-8'))


if __name__ == '__main__':
    nn = NHentai.get_gallery_info('g/339083')
    print(nn.tags[0].url)
