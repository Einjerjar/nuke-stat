from dataclasses import dataclass
from typing import Dict

import discord


@dataclass
class BaseResponse:
    title: str
    author: str
    url: str
    fields: Dict[str, str]
    gallery_id: str
    cover: str = ''
    source: str = ''
    color: int = 0x7289da
