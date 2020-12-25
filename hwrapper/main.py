import re
from dataclasses import dataclass
from typing import List, Any

from .nhwrapper import NHHandler
from .ehwrapper import EHHandler
from .hnwrapper import HNHandler


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
    HWrapper(HPatterns(['e-hentai.org', 'eh'], [r'g\/(\d+\/[\dabcdef]+)', r'(\d+\/[\dabcdef]+)']), EHHandler),
    HWrapper(HPatterns(['hentainexus.com', 'hn'], [r'hn\/(\d+)']), HNHandler),
    HWrapper(HPatterns(['nhentai.net', 'nh'], [r'g\/(\d+)', r'(\d+)']), NHHandler),
]


def get_wrapper(g_id):
    for i in wrappers:
        if i.can_handle_link(g_id):
            return i.handler
    return None