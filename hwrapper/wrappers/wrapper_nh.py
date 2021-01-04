from hwrapper.bases import BaseResponse
from hwrapper.sites.nh import *
from hwrapper.util import time_format


class NHHandler:
    @staticmethod
    def handle_link(link):
        nn = NHentai.get_gallery_info(link)

        if not nn.valid:
            return None

        languages = nn.filer_tags(NHTagTypes.LANG)
        parodies = nn.filer_tags(NHTagTypes.PARODY)
        groups = nn.filer_tags(NHTagTypes.GROUP)
        artists = nn.filer_tags_raw(NHTagTypes.ARTIST)
        characters = nn.filer_tags(NHTagTypes.CHARACTER)
        categories = nn.filer_tags(NHTagTypes.CATEGORY)
        tags = nn.filer_tags(NHTagTypes.TAG)

        n_artists = ', '.join(['[{}]({})'.format(x.name, x.url) for x in artists])

        return BaseResponse(nn.title.en, n_artists, nn.url, {
            'Groups': groups,
            'Languages': languages,
            'Parodies': parodies,
            'Characters': characters,
            'Categories': categories,
            'Tags': tags,
            'Uploaded': time_format(nn.uploaded),
            'Page Count': nn.length,
            # 'ID': nn.id
        }, nn.id, nn.cover, NHentai.ident, 0xED2553)
