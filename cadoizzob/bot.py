#!/usr/bin/env python3
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
import shutil
import mapmk
import ttplayer
from text import *
from ttCommand import ttCommandGestion, deleteGuildFile 
from settings import createguildsets, guildvarchange, get_prefix_cmd, get_language,get_prefix
from settingsCommand import *
#Put your Token bot here 
TOKEN = ""
bot = discord.Client()
# You can change the prefix here 
bot= commands.Bot(command_prefix = get_prefix_cmd, help_command=None, case_insensitive=True)

# put arg in the good format to get rid of 
def lowerArg (args):
    lowerarg=[]
    for arg in args:
        # to use tag instead of finding the user id 
        if tagsample.match(arg):
            newarg = arg.strip('<!@>')
            lowerarg.append(str.lower(newarg))
        else :
            lowerarg.append(str.lower(arg))
    return lowerarg

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("-------")

@bot.event
async def on_guild_join(guild):
    createguildsets(guild.id)
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('Hey there! this is the message i send when i join a server\nMy prefix is c! so write c!help for more info')
        break

@bot.command()
async def help(ctx):
    await ctx.send(helpTexts.get(get_language(ctx)).get("help").format(get_prefix(ctx)))

#Settings Command 
@bot.command()
@commands.has_permissions(administrator = True)
async def settings(ctx, *args):
    if not args:
        await ctx.send(settingsTexts.get(get_language(ctx)).get("args").format(get_prefix(ctx)))
    args = lowerArgSets(args)
    if args[0] == "help" :
        await ctx.send(settingsTexts.get(get_language(ctx)).get("help").format(get_prefix(ctx)))
    # Change prefix
    elif args[0] == "prefix":
        if len(args) == 2 :
            guildvarchange(args[0], str(ctx.guild.id) , args[1])
            await ctx.send(settingsTexts.get(get_language(ctx)).get("prefix").format(args[1]))
        else :
            await ctx.send(settingsTexts.get(get_language(ctx)).get("tooManyArgs").format(get_prefix(ctx)))
    # Change language
    elif args[0] == "language":
        if len(args) == 2 and (args[1] == "fr" or args[1] == "en") :
            guildvarchange(args[0], str(ctx.guild.id) , args[1])
            await ctx.send(settingsTexts.get(get_language(ctx)).get("language").format(args[1]))
        else :
            await ctx.send(settingsTexts.get(get_language(ctx)).get("tooManyArg").format(get_prefix(ctx))
            + settingsTexts.get(get_language(ctx)).get("wrongLanguage").format(get_prefix(ctx)))
    #elif args[0] == "check":
    #    await ctx.send(settingsTexts.get(get_language(ctx)).get("check").format(get_language(ctx), get_prefix(ctx)))
    #elif args[0] == "teams" :
    #    await teamsCommand(ctx, args)
    else:
        await ctx.send(settingsTexts.get(get_language(ctx)).get("noCmd").format(get_prefix(ctx)))

# c!war Command 
@bot.command()
async def war(ctx, *args):
    if not args:
        await ctx.send(warTexts.get(get_language(ctx)).get("args").format(get_prefix(ctx)))
    if args[0] == 'help':
        await ctx.send(warTexts.get(get_language(ctx)).get("help").format(get_prefix(ctx)))
    elif args[0] == 'vacances':
        for i in range(14,25): # de 14 à 24
            if (get_language(ctx)== "en"):
                message = await ctx.send('war '+str(i%13)+'PM')
            else : 
                message = await ctx.send('war '+str(i%24)+'h')
            await message.add_reaction("✅")
            await message.add_reaction("❌")
            await message.add_reaction("❔")
    else :
        for i in range(len(args)):
            if (get_language(ctx)== "en"):
                message = await ctx.send('war '+args[i])
            else:
                message = await ctx.send('war '+args[i]+'h')
            await message.add_reaction("✅")
            await message.add_reaction("❌")
            await message.add_reaction("❔")

# c!tt Command
@bot.command()
async def tt(ctx, *args):
    if not args :
        await ctx.send(ttTexts.get(get_language(ctx)).get("noArg").format(get_prefix(ctx)))
    else :
        args= lowerArg(args)
        if args[0] == 'help':
            await ctx.send ( ttTexts.get(get_language(ctx)).get("help").format(get_prefix(ctx)))
            await ctx.send ( ttTexts.get(get_language(ctx)).get("help2").format(get_prefix(ctx)))
        elif args[0] == 'deleteall':
            await deleteGuildFile(ctx)
        elif args[0] == '200':
            del args[0]
            await ttCommandGestion(ctx,args , speedPath)
        else :
            await ttCommandGestion(ctx,args , '') # 150 cc


@bot.event
async def on_reaction_add(reaction, user):
    if (reaction.message.author.id == 729648516795990146 and reaction.count == 4):
            await reaction.message.remove_reaction(reaction, bot.user)

@bot.event
async def on_reaction_remove(reaction, user):
    if (reaction.message.author.id == 729648516795990146 and reaction.count == 1):
        await reaction.message.add_reaction(reaction)

bot.run(TOKEN)
