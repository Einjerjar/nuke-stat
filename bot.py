import datetime
import logging
import os

import discord
from discord.ext.commands import Bot, Context
from dotenv import load_dotenv

from hwrapper import get_wrapper, BaseResponse

logging.basicConfig(level=logging.INFO)
load_dotenv()

bot = Bot(command_prefix=os.getenv('PREFIX') or '=')


@bot.event
async def on_ready():
    print('Logged in as {}#{}'.format(bot.user.name, bot.user.id))


@bot.command(aliases=['ni'], help='get nuke info')
async def nuke_info(ctx: Context, gid):
    ni = get_wrapper(gid)
    if ni is None:
        await ctx.send('Sorry pal, don\'t know how to handle that one.')
        return

    resp: BaseResponse = ni.handle_link(gid)

    f_embed = discord.Embed(title=resp.title,
                            description='By: {}'.format(resp.author),
                            timestamp=datetime.datetime.utcnow(),
                            color=resp.color,
                            url=resp.url)

    for x in resp.fields:
        if len(str(resp.fields[x]).strip()) > 0:
            f_embed.add_field(name=x, value=resp.fields[x])

    if len(str(resp.cover).strip()) > 0:
        f_embed.set_thumbnail(url=resp.cover)

    await ctx.send(embed=f_embed)


@bot.command(aliases=['nc'], help='get the cover for the nuke')
async def nuke_cover(ctx: Context, gid):
    nn = NHentai.get_gallery_info(gid)
    await ctx.send(nn.cover)


# @bot.command(aliases=['np'], help='get page x of the nuke')
# async def nuke_page(ctx: Context, gid, page:int):
#     page -= 1
#     nn = NHentai.get_gallery_info(gid)
#     if nn.length > page >= 0:
#         await ctx.send(nn.page_info[page])
#     else:
#         await ctx.send('Page out of bounds ma boi')


bot.run(os.getenv('BOT_TOKEN'))
