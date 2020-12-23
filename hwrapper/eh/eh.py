import json
import requests as req

from enum import Enum, auto

_URL_BASE_PROTOCOL = 'https'
_EH_URL_ROOT = 'e-hentai.org'
_EH_URL_BASE = '{}://{}'.format(_URL_BASE_PROTOCOL, _EH_URL_ROOT)
_EH_URL_GAL = '{}/g/{{}}/{{}}'.format(_EH_URL_BASE)
_EH_URL_API = '{}://api.{}/api.php'.format(_URL_BASE_PROTOCOL, _EH_URL_ROOT)
_EH_REQ_BASE = '{{ "method": "gdata", "gidlist": [[ {}, "{}" ]], "namespace": 1 }}'

class EHTitle:
    def __init__(self, rd):
        self.en = rd['title']
        self.jp = rd['title_jpn']


class EHTagTypes(Enum):
    PARODY = 'parody'
    CHARACTER = 'character'
    ARTIST = 'artist'
    FEMALE = 'female'
    MALE = 'male'

    @classmethod
    def get_type(cls, t):
        return cls(t)


class EHTag:
    def __init__(self, tag):
        tag = tag.split(':')
        self.raw_type = tag[0]
        self.t_type = EHTagTypes.get_type(tag[0])
        self.name = tag[1]


class EHGalleryInfo:
    def __init__(self, raw_data):
        rd_a = json.loads(raw_data)
        rd = rd_a['gmetadata'][0]
        self.raw_data = rd
        self.id = rd['gid']
        self.token = rd['token']
        self.title = EHTitle(rd)
        self.category = rd['category']
        self.cover = rd['thumb']
        self.uploader = rd['uploader']
        self.uploaded = int(rd['posted'])
        self.length = rd['filecount']
        self.rating = rd['rating']
        self.tags = [EHTag(x) for x in rd['tags']]
        self.url = _EH_URL_GAL.format(self.id, self.token)

    def __repr__(self):
        return '[{}/{}] {}'.format(self.id, self.token, self.title.en)

    def filter_tags_raw(self, t_type):
        return [x for x in self.tags if x.t_type == t_type]

    def filter_tags(self, t_type):
        return ', '.join([x.name for x in self.filter_tags_raw(t_type)])


class EHentai:
    def __init__(self):
        pass

    @staticmethod
    def try_parse_g_id(g_id):
        f_id = g_id
        if f_id.startswith('<'):
            f_id = f_id[1:-1]
        if f_id.startswith('http'):
            x = f_id.split('/')
            f_id = [x[4], x[5]]
        elif f_id.startswith('g/'):
            x = f_id.split('/')
            f_id = [x[2], x[3]]
        else:
            f_id = f_id.split('/')
        return f_id


    @classmethod
    def get_gallery_info(cls, g_id):
        f_id = cls.try_parse_g_id(g_id)

        r_data = req.post(_EH_URL_API, data=_EH_REQ_BASE.format(f_id[0], f_id[1]))
        return EHGalleryInfo(r_data.content.decode('utf-8'))


if __name__ == '__main__':
    ee = EHentai.get_gallery_info('https://e-hentai.org/g/1771363/6be2d60f02/')
    print(ee)