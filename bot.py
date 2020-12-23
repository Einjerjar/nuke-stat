import datetime
import logging
import os

import discord
from discord.ext.commands import Bot, Context
from dotenv import load_dotenv

from nh import NHentai, NHTagTypes

logging.basicConfig(level=logging.INFO)
load_dotenv()

bot = Bot(command_prefix='=')


@bot.event
async def on_ready():
    print('Logged in as {}#{}'.format(bot.user.name, bot.user.id))


@bot.command(aliases=['ni'], help='get nuke info')
async def nuke_info(ctx: Context, gid: int):
    nn = NHentai.get_gallery_info(gid)

    def filer_tags(type):
        return ', '.join([x.name for x in nn.tags if x.type == type])

    # print('{} :: {}'.format(gid, ', '.join([x.name for x in nn.tags])))

    languages = filer_tags(NHTagTypes.LANG)
    parodies = filer_tags(NHTagTypes.PARODY)
    groups = filer_tags(NHTagTypes.GROUP)
    artists = filer_tags(NHTagTypes.ARTIST)
    characters = filer_tags(NHTagTypes.CHARACTER)
    categories = filer_tags(NHTagTypes.CATEGORY)
    tags = filer_tags(NHTagTypes.TAG)

    f_embed = discord.Embed(title=nn.title.pr,
                            description='By: {}'.format(artists),
                            timestamp=datetime.datetime.utcnow(),
                            color=discord.Color.blue())
    if groups != '':
        f_embed.add_field(name='Group', value=groups)
    if languages != '':
        f_embed.add_field(name='Language', value=languages)
    if parodies != '':
        f_embed.add_field(name='Parodies', value=parodies)
    if characters != '':
        f_embed.add_field(name='Characters', value=characters)
    if categories != '':
        f_embed.add_field(name='Categories', value=categories)
    if tags != '':
        f_embed.add_field(name='Tags', value=tags)
    f_embed.add_field(name='Uploaded', value=nn.uploaded)
    f_embed.add_field(name='Page Count', value=nn.length)
    f_embed.add_field(name='ID', value=str(gid))
    f_embed.set_thumbnail(url=nn.get_cover_url())

    await ctx.send(embed=f_embed)


bot.run(os.getenv('BOT_TOKEN'))
