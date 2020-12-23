import discord

from .bases import BaseResponse
from .eh import *
from .util import time_format


class EHHandler:
    @staticmethod
    def handle_link(link):
        ee = EHentai.get_gallery_info(link)

        artists = ee.filter_tags(EHTagTypes.ARTIST)
        parodies = ee.filter_tags(EHTagTypes.PARODY)
        characters = ee.filter_tags(EHTagTypes.CHARACTER)
        male = ee.filter_tags(EHTagTypes.MALE)
        female = ee.filter_tags(EHTagTypes.FEMALE)

        return BaseResponse(ee.title.en, artists, ee.url, {
            'Parodies': parodies,
            'Characters': characters,
            'Category': ee.category,
            'Male': male,
            'Female': female,
            'Uploaded': time_format(ee.uploaded),
            'Page Count': ee.length,
            'ID': '{}/{}'.format(ee.id, ee.token)
        }, ee.cover, 'eh', discord.Color(0xBC8F94))
