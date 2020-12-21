import datetime
import discord
import logging
import os

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

    def filer_tags(tags, type):
        return [x.name for x in tags if x.type == type]

    # print('{} :: {}'.format(gid, ', '.join([x.name for x in nn.tags])))

    langs = ', '.join(filer_tags(nn.tags, NHTagTypes.LANG))
    parodies = ', '.join(filer_tags(nn.tags, NHTagTypes.PARODY))
    groups = ', '.join(filer_tags(nn.tags, NHTagTypes.GROUP))
    artists = ', '.join(filer_tags(nn.tags, NHTagTypes.ARTIST))
    characters = ', '.join(filer_tags(nn.tags, NHTagTypes.CHARACTER))
    categories = ', '.join(filer_tags(nn.tags, NHTagTypes.CATEGORY))
    tags = ', '.join([x.name for x in nn.tags if x.type == NHTagTypes.TAG])
    out = nn.title.pr \
          + '\nArtist: ' + artists \
          + '\nGroup: ' + groups \
          + '\nLanguage: ' + langs \
          + '\nParodies:' + parodies \
          + '\nCharacters: ' + characters \
          + '\nCategories: ' + categories \
          + '\nTags: ' + tags \
          + '\nPages: ' + str(nn.length)

    eOut = discord.Embed(title=nn.title.pr,
                 description='By: {}'.format(artists),
                 timestamp=datetime.datetime.utcnow(),
                 color=discord.Color.blue())
    if groups != '':
        eOut.add_field(name='Group', value=groups)
    if langs != '':
        eOut.add_field(name='Language', value=langs)
    if parodies != '':
        eOut.add_field(name='Parodies', value=parodies)
    if characters != '':
        eOut.add_field(name='Characters', value=characters)
    if categories != '':
        eOut.add_field(name='Categories', value=categories)
    if tags != '':
        eOut.add_field(name='Tags', value=tags)
    eOut.add_field(name='Pages', value=nn.length)
    eOut.add_field(name='ID', value=gid)
    eOut.set_thumbnail(url=nn.get_cover_url())

    await ctx.send(embed=eOut)


bot.run(os.getenv('BOT_TOKEN'))

