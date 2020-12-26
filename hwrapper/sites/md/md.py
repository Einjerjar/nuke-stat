import json
import requests as req

from .md_tags import tags

_URL_BASE_PROTOCOL = 'https'
_URL_ROOT = 'mangadex.org'
_URL_BASE = '{}://{}'.format(_URL_BASE_PROTOCOL, _URL_ROOT)
_MD_API = '{}/api/v2/manga/{{}}'.format(_URL_BASE)
_MD_TITLE = '{}/title/{{}}'.format(_URL_BASE)


def unknown_tag(_id):
    return {
        'id': _id,
        'name': 'UnknownTag >> pls contact bot author to update tag DB',
        'group': 'UNKNOWN',
        'description': 'UnknownTag >> pls contact bot author to update tag DB'
    }


class MangadexTag:
    def __init__(self, tag):
        self.t_id = tag['id']
        self.t_name = tag['name']
        self.group = tag['group']
        self.description =  tag['description']

    def __repr__(self):
        return self.t_name

    def __str__(self):
        return self.t_name


class MangadexRating:
    def __init__(self, rating):
        self.by = rating['bayesian']
        self.mn = rating['mean']
        self.count = rating['users']

    def __repr__(self):
        return self.by

    def __str__(self):
        return str(self.by)


class MangadexGalleryInfo:
    def __init__(self, raw_data):
        rd = json.loads(raw_data)['data']
        self.raw_data = rd

        self.id = rd['id']
        self.title = rd['title']
        self.description = rd['description']
        self.cover = rd['mainCover']
        self.artists = rd['artist']
        self.authors = rd['author']
        self.tags = [MangadexTag(Mangadex.tags[str(x)] if str(x) in Mangadex.tags else unknown_tag(x)) for x in rd['tags']]
        self.rating = MangadexRating(rd['rating'])
        self.view = rd['views']
        self.follows = rd['follows']
        self.url = _MD_TITLE.format(self.id)

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title


class Mangadex:
    tags = tags

    @staticmethod
    def try_parse_link(link):
        f_link = link
        sp = f_link.split('/')

        if f_link.startswith(_URL_ROOT):
            f_link = sp[2]
        elif f_link.startswith('md'):
            f_link = sp[1]

        return f_link

    @classmethod
    def get_gallery_info(cls, link):
        gallery_id = cls.try_parse_link(link)

        r_data = req.get(_MD_API.format(gallery_id))

        return MangadexGalleryInfo(r_data.content.decode('utf-8'))


if __name__ == '__main__':
    u = ['mangadex.org/title/59266/nishimori-san-chi-no-shinobu-kun', 'md/59266']
    for i in u:
        print(Mangadex.try_parse_link(i), i)