import re
from dataclasses import dataclass
from typing import List, Any

from hwrapper.wrappers.wrapper_nh import NHHandler
from hwrapper.wrappers.wrapper_eh import EHHandler
from hwrapper.wrappers.wrapper_hn import HNHandler
from hwrapper.wrappers.wrapper_hc import HCHandler
from hwrapper.wrappers.wrapper_md import MDHandler
from hwrapper.wrappers.wrapper_h2 import H2Handler


@dataclass
class HPatterns:
    start: list
    # int patterns for modules that use ints as reference
    # x is the int value, so for cases like nh, `x` and on eh `x/x`
    int_patterns: list


@dataclass
class HWrapper:
    patterns: HPatterns
    handler: Any

    def can_handle_link(self, link):
        if link.startswith('http'):
            link = link.split('://')[1]
        for i in self.patterns.start:
            if link.startswith(i):
                return True
        for i in self.patterns.int_patterns:
            c_pat = re.compile(i)
            c_search = c_pat.search(link)
            if c_search and len(c_search.groups()) > 0:
                return True

    def get_module(self):
        pass


wrappers: List[HWrapper] = [
    HWrapper(HPatterns(['e-hentai.org', 'eh'], [r'g\/(\d+\/[\dabcdef]+)', r'(^\d+\/[\dabcdef]+)']), EHHandler),
    HWrapper(HPatterns(['hentai2read.com', 'h2'], []), H2Handler),
    HWrapper(HPatterns(['mangadex.org', 'md'], [r'md\/(\d+)']), MDHandler),
    HWrapper(HPatterns(['hentainexus.com', 'hn'], [r'hn\/(\d+)']), HNHandler),
    HWrapper(HPatterns(['hentai.cafe', 'hc.fyi', 'hc'], [r'hc\/(\d+)']), HCHandler),
    HWrapper(HPatterns(['nhentai.net', 'nh'], [r'g\/(\d+)', r'(^\d+)']), NHHandler),
]


def get_wrapper(g_id):
    for i in wrappers:
        if i.can_handle_link(g_id):
            return i.handler
    return None


if __name__ == '__main__':
    tests = [
        'e-hentai.org/g/123/456', 'eh/123/456', 'g/123/456',
        'mangadex.org/title/59266/nishimori-san-chi-no-shinobu-kun', 'md/59266',
        'hentainexus.com/view/123', 'hn/123',
        'hentai.cafe/hc.fyi/123', 'hc.fyi/123', 'hc/123'
        'nhentai.net/g/123', 'g/123', 'nh/123',
        'hentai2read.com/koiito_kinenbi/', 'h2/koiito_kinenbi'
    ]

    for j in tests:
        print(get_wrapper(j), j)