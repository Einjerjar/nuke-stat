_URL_BASE_PROTOCOL = 'https'
_URL_ROOT = 'hentai.cafe/hc.fyi'
_URL_BASE = '{}://{}'.format(_URL_BASE_PROTOCOL, _URL_ROOT)
_HC_VIEW = '{}/{{}}'.format(_URL_BASE)


class MangadexGalleryInfo:
    def __init__(self, raw_data):
        pass

    def __repr__(self):
        pass


class Mangadex:
    @staticmethod
    def try_parse_link(link):
        pass

    @classmethod
    def get_gallery_info(cls, link):
        return MangadexGalleryInfo(link)