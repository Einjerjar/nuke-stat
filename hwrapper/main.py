import re
from dataclasses import dataclass
from typing import List, Any

from .nhwrapper import NHHandler


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
        for i in self.patterns.start:
            if link.startswith(i):
                return True
        for i in self.patterns.int_patterns:
            c_pat = re.compile(i.replace('x', '\\d+'))
            c_search = c_pat.search(link)
            if c_search and c_search.group:
                return True

    def get_module(self):
        pass


wrappers: List[HWrapper] = [
    HWrapper(HPatterns(['nhentai.net', 'g'], ['x']), NHHandler),
]


def get_wrapper(g_id):
    for i in wrappers:
        if i.can_handle_link(g_id):
            return i.handler
    return None


if __name__ == '__main__':
    print(get_wrapper('g/339083').handle_link('g/339083'))
