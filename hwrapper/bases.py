from dataclasses import dataclass
from typing import Dict

import discord


@dataclass
class BaseResponse:
    title: str
    author: str
    url: str
    fields: Dict[str, str]
    cover: str = ''
    source: str = ''
    color: discord.Color = discord.Color.blurple()
