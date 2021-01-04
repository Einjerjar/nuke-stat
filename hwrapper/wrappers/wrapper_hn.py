from hwrapper.bases import BaseResponse
from hwrapper.sites.hn import *


class HNHandler:
    @staticmethod
    def handle_link(link):
        hh = HNexus.get_gallery_info(link)

        return BaseResponse(hh.title, hh.artist, hh.url, {
            'Description': hh.desc,
            'Language': hh.language,
            'Magazine': hh.magazine,
            'Publisher': hh.publisher,
            'Parodies': hh.parody,
            'Tags': ', '.join(hh.tags),
            'Page Count': hh.length,
            # 'ID': hh.id
        }, hh.id, hh.cover, HNexus.ident, 0xDF691A)
