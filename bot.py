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
    print('Logged in as {} | {} | {} | {}'.format(bot.user.name, bot.user.display_name, bot.user.bot, bot.user.id))


@bot.command(aliases=['ni'], help='[ni] get nuke\'s info in the format of <source/nuke>')
async def nuke_info(ctx: Context, gid):
    gid = str(gid)
    if gid.startswith('<'):
        gid = gid[1:-1]

    ni = get_wrapper(gid)
    if ni is None:
        await ctx.send('Sorry pal, don\'t know how to handle that one.')
        return

    resp: BaseResponse = ni.handle_link(gid)

    if resp is None:
        await ctx.send('That gallery doesn\'t exist tho?')
        return

    print(resp.title)

    f_embed = discord.Embed(title=resp.title,
                            description='By: {}'.format(resp.author),
                            timestamp=datetime.datetime.utcnow(),
                            color=resp.color,
                            url=resp.url)

    for x in resp.fields:
        if len(str(resp.fields[x]).strip()) > 0:
            f_embed.add_field(name=x, value=resp.fields[x])

    f_embed.add_field(name='Source', value='{}/{}'.format(resp.source, resp.gallery_id))

    if len(str(resp.cover).strip()) > 0:
        f_embed.set_thumbnail(url=resp.cover)

    await ctx.send(embed=f_embed)


@bot.command(aliases=['nc'], help='[nc] get the cover for the nuke')
async def nuke_cover(ctx: Context, gid):
    ni = get_wrapper(gid)
    if ni is None:
        await ctx.send('Sorry pal, don\'t know how to handle that one.')
        return

    resp: BaseResponse = ni.handle_link(gid)

    if resp is None:
        await ctx.send('That gallery doesn\'t exist tho?')
        return

    await ctx.send(resp.cover)


@bot.command(aliases=['nl'], help='[nl] list available sources and their prefixes')
async def nuke_list(ctx: Context):
    x = [
        '```md',
        '# Available sources and their prefixes',
        '',
        '- md : Mangadex',
        '- eh : EHen',
        '- nh : NHen',
        '- hc : HCafe',
        '- hn : HNexus',
        '```'
    ]

    await ctx.send('\n'.join(x))


@bot.command()
async def about(ctx: Context):
    e = discord.Embed(title='About')
    e.add_field(name='Author', value='[Einjerjar](https://github.com/einjerjar)')
    e.add_field(name='Source', value='[GH/nuke-stat](https://github.com/einjerjar/nuke-stat)')
    e.add_field(name='Donate', value='[Buy me a coffee](https://ko-fi.com/einjerjar)')
    e.set_thumbnail(url=bot.user.avatar_url)

    await ctx.send(embed=e)


@bot.command(aliases=['gl'], hidden=True)
async def g_list(ctx: Context):
    # Hard coded command for checking all joined guilds, only works on testing server
    if str(ctx.guild.id) != os.getenv('DEV_GUILD'):
        return

    # Might remove the guild name chunk if guild count goes over 20 or so
    g_l = []
    c_l = 0
    for i in bot.guilds:
        i: discord.Guild = i
        g_l.append('{} @ {}'.format(i.name, i.id))
        c_l += 1

    await ctx.send('**Joined {} Guilds**\n{}'.format(c_l, '\n'.join(g_l)))


bot.run(os.getenv('BOT_TOKEN'))
