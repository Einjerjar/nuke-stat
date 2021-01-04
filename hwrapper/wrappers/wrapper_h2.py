from hwrapper.bases import BaseResponse
from hwrapper.sites.h2 import *


class H2FieldBuilder:
    def __init__(self):
        self.fields = {}
    
    def try_add_field(self, f_name, f_data):
        if len(f_data) > 0:
            self.fields[f_name] = ', '.join(f_data)


class H2Handler:
    @staticmethod
    def handle_link(link):
        hh = H2Read.get_gallery_info(link)
        
        fields = H2FieldBuilder()
        fields.try_add_field('Parody', hh.parody)
        fields.try_add_field('Ranking', hh.ranking)
        fields.try_add_field('Status', hh.status)
        fields.try_add_field('Release Year', hh.year)
        fields.try_add_field('Views', hh.views)
        fields.try_add_field('Page Count', hh.length)
        fields.try_add_field('Category', hh.category)
        fields.try_add_field('Content', hh.content)
        fields.try_add_field('Character', hh.character)
        fields.try_add_field('Language', hh.language)

        print(hh.artist, hh.author)
        artists = hh.artist + hh.author

        return BaseResponse(hh.title, ', '.join(artists), hh.url, 
                            fields.fields,
                            hh.id, hh.cover, H2Read.ident, 0x1E73BE)
