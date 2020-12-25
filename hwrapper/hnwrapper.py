import discord

from .bases import BaseResponse
from .hn import *
from .util import time_format


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
            'ID': hh.id
        }, hh.cover, 'eh', discord.Color(0xDF691A))
