# HModules Base Format

```python
_URL_BASE_PROTOCOL = 'https'
_URL_ROOT = 'hentai.cafe/hc.fyi'
_URL_BASE = '{}://{}'.format(_URL_BASE_PROTOCOL, _URL_ROOT)

class GalleryInfo:
    def __init__(self, raw_data):
        pass
    
    def __repr__(self):
        pass
    
class Gallery:
    @staticmethod
    def try_parse_link(link):
        return link
    
    @classmethod
    def get_gallery_info(cls, link):
        link = cls.try_parse_link(link)
        return GalleryInfo(link)
```