from hwrapper.bases import BaseResponse
from hwrapper.sites.md import *


class MDHandler:
    @staticmethod
    def handle_link(link):
        hh = Mangadex.get_gallery_info(link)

        return BaseResponse(hh.title, ', '.join(hh.authors), hh.url, {
            'Description': hh.description,
            'Tags': ', '.join([str(x) for x in hh.tags]),
            'Rating': str(hh.rating),
            # 'ID': hh.id
        }, hh.id, hh.cover, 'eh', 0xDF691A)