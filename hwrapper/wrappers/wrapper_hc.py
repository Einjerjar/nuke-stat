from hwrapper.bases import BaseResponse
from hwrapper.sites.hc import *


class HCHandler:
    @staticmethod
    def handle_link(link):
        hh = HCafe.get_gallery_info(link)

        return BaseResponse(hh.title, ', '.join(hh.artists), hh.url, {
            'Tags': ', '.join(hh.tags),
            'Page Count': hh.length,
            # 'ID': hh.id
        }, hh.id, hh.cover, 'hc', 0x1E73BE)
