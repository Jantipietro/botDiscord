#!/usr/bin/env python3
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Bot
from discord.app_commands import AppCommandError
from datetime import date, datetime, timedelta
from typing import Literal, Optional
import json
import asyncio
import os, time
import shutil
import mapmk
import ttplayer
from text import *
from ttCommand import ttCommandGestion, deleteGuildFile, createCommand
from ttEdit import ModifyEmbed
from settings import createguildsets, guildvarchange, get_language, opensettings,writesettings

#Put your Token bot here 
TOKEN = ""

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

intents = discord.Intents.default()
# You can change the prefix here 
bot = MyClient(intents=intents)

bot.cptWar = 0
bot.cptTt = 0
bot.cptSettings = 0 
bot.cptWrongCommand = 0
bot.cptHelp = 0

# put arg in the good format to get rid of 
def lowerArg (args):
    lowerarg=[]
    for arg in args:
        # to use tag instead of finding the user id 
        if tagsample.match(arg):
            newarg = arg.strip('<!@>')
            lowerarg.append(str.lower(newarg))
        elif urlsample.match(arg):
            lowerarg.append(arg)
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
    # keep track of setting 
    createguildsets(guild.id)
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('Hey there! this is the message i send when i join a server\n Every command use "/" now, every command has is help command. Contact #Cadoizz#5176 if any problem')
        break

@bot.tree.command()
async def help(interaction : discord.Interaction):
    bot.cptHelp += 1
    await interaction.channel.send(helpTexts.get(get_language(interaction.guild_id)).get("help"))
    await interaction.response.send_message("Done" , ephemeral = True)

#Settings Command 
@bot.tree.command()
@app_commands.describe(
    option="What command do you want",
    language = "The language you want 'fr' or 'en'( contact us if you want to help to add another language )"
)
async def settings(interaction : discord.Interaction, option : Literal['help', 'language'], language : Optional[Literal['fr', 'en']]):
    bot.cptSettings +=1 
    if option == "help" :
        await interaction.response.send_message(settingsTexts.get(get_language(interaction.guild_id )).get("help"))
    # Change language
    elif option == "language":
        if (language == "fr" or language == "en") :
            guildvarchange( option,str(interaction.guild_id), language)
            await interaction.response.send_message(settingsTexts.get(get_language(interaction.guild_id )).get("language").format(language))
        else :
            await interaction.response.send_message((settingsTexts.get(get_language(interaction.guild_id )).get("tooManyArg"))
            + settingsTexts.get(get_language(interaction.guild_id )).get("wrongLanguage"))
    else:
        await interaction.response.send_message(settingsTexts.get(get_language(interaction.guild_id )).get("noCmd"))

# c!war Command 
@bot.tree.command()
@app_commands.describe(
    first = "The first time you want to draw",
    second = "The last time you want to draw"
)
async def war(interaction : discord.Interaction, first: app_commands.Range[int,0,24] , second : app_commands.Range[int,0,48]):
    guildvarchange( "last_use", str(interaction.guild_id) , str(datetime.now()))
    await interaction.response.send_message("Done" , ephemeral=True)
    bot.cptWar +=1
    textChannel = interaction.channel
    for i in range(first,second+1):
        if (get_language(interaction.guild_id,  )== "en"):
            message = await textChannel.send('war '+str(i%13))
        else:
            message = await textChannel.send('war '+str(i%24)+'h')
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        await message.add_reaction("❔")


def createARGS(args ,third ,four, five):
    if ( third != None ):
        args.append(third)
    if ( four != None):
        args.append(four)
    if ( five != None):
        args.append(five)
    return args
        
# c!tt Command
@bot.tree.command()
@app_commands.describe(
    option = "Categorie you want, Care DeleteAll! ",
    categorie = "This one is mandatory if you want to make anything if option is 150 or 200",
    third = "Add your parameters like show in the help command starting with third",
    four = "Second parameters you need to put ( orders shown in help )",
    five = "Thirds parameters ( orders show in help ) "

)
async def tt(interaction : discord.Interaction, option : Literal['help', '200cc', '150cc', 'deleteall', 'maps', 'create'], categorie : Optional[Literal['shroom', 'ni']] , third : str = None , four : str = None, five : str = None):
    guildvarchange("last_use", str(interaction.guild_id) , str(datetime.now()))
    bot.cptTt +=1
    args = []
    args = createARGS(args,third, four, five)
    args= lowerArg(args)
    lengArg = len(args)
    if option == 'help' and lengArg == 0:
        TextChannel = interaction.channel
        await TextChannel.send ( ttTexts.get(get_language(interaction.guild_id)).get("help"))
        await TextChannel.send ( ttTexts.get(get_language(interaction.guild_id)).get("help2"))
        await TextChannel.send ( ttTexts.get(get_language(interaction.guild_id)).get("help3"))
    elif option == 'deleteall' and categorie == None and lengArg == 0:
    #only permission manage_message allow to delete tt's file
        await deleteGuildFile(interaction.guild_id, interaction.channel, interaction.user.guild_permissions.manage_messages)
    # Draw png with all maps nickname that it use
    elif option == 'maps' and lengArg == 0:
        await interaction.channel.send("https://media.discordapp.net/attachments/579573532263055381/583008091541471234/abveration.png?width=1202&height=510")
        await interaction.channel.send("https://cdn.discordapp.com/attachments/608269384976302153/1052947025903222866/maps-dlc-bot_3e_vague.png")
        #Create files with the server name
    elif option == 'create' and lengArg == 0:
        await createCommand(interaction.guild_id , interaction.channel,interaction.user.guild_permissions.manage_messages)
    elif ( lengArg != 0) :
        if option == '200cc':
            await ttCommandGestion(interaction,categorie,args , speedPath) # speedPath = 200cc
        elif option == '150cc':
            await ttCommandGestion(interaction,categorie,args , '') # 150 cc
        else :
            await interaction.channel.send("Gone Wrong")
    else :
        await interaction.channel.send("Gone Wrong")
    
    await interaction.response.send_message("Done" , ephemeral = True)

    


@bot.event
async def on_reaction_add(reaction, user):
    if (reaction.message.author.id == bot.user.id):
        if reaction.message.embeds and user.id != bot.user.id :
            if reaction.emoji == "⬅️" or  reaction.emoji == "➡️": # row right
                await ModifyEmbed(reaction)
        if (reaction.count == 4):
            await reaction.message.remove_reaction(reaction, bot.user)
        

@bot.event
async def on_reaction_remove(reaction, user):
    if (reaction.message.author.id == 729648516795990146 and reaction.count == 1):
        await reaction.message.add_reaction(reaction)

# @bot.tree.error
# async def on_command_error( interaction : discord.Interaction, error: AppCommandError) -> None:
#     await interaction.response.send_message("Error : probably false argument ( no gestion of error for now)", ephemeral=True)

# @bot.event
# async def on_command_error(ctx,error):
#     bot.cptWrongCommand +=1
#     await ctx.send(helpTexts.get(get_language(inter)).get("help"))

@bot.tree.command()
async def stats(interaction):
    if ( interaction.guild_id == 302544642585526293 or interaction.guild_id == 518942329181175808):
        settings = opensettings()
        nbfile = 0
        cptFileUseToday = 0
        now = datetime.today()
        nb_second_per_day = 60*60*24
        for f in   settings:
            duration = now - datetime.strptime( settings[f]["last_use"], '%Y-%m-%d %H:%M:%S.%f') 
            # "2022-09-20 21:28:58.863288"
            duration_in_s = duration.total_seconds()
            if ( duration_in_s < nb_second_per_day):
                cptFileUseToday +=1
            nbfile +=1
        message = "```Nombre de serveur qui ont modifié le bot aujourd'hui : {} sur {} serveurs\nNombre de commande utilisé :\nWar : {} \nTt : {} \nSettings : {}\nHelp : {}\nCmd Raté: {}```".format(cptFileUseToday, nbfile, bot.cptWar,bot.cptTt,bot.cptSettings,bot.cptHelp, bot.cptWrongCommand)
        await interaction.response.send_message(message)
    else :
        await interaction.response.send_message("you can't do this command")

# @bot.command()
# @commands.cooldown(100,24*3600)
# async def save(ctx, *args):
#     if ( ctx.message.author.id == 302536904824586241):
#         now = date.today()
#         currentTime = now.strftime("%x")
#         path = currentTime.replace("/","_")
#         outputPath="stats/"+ path+".txt"
#         stats = { "War" : bot.cptWar, "Tt" : bot.cptTt, "Settings" :bot.cptSettings, "Help" : bot.cptHelp, "Wrong" : bot.cptWrongCommand }
#         try :
#             with open(outputPath, "w") as f :
#                 json.dump(stats,f)
#                 f.close()
#             bot.cptWar = 0
#             bot.cptTt = 0
#             bot.cptSettings = 0
#             bot.cptHelp = 0
#             bot.cptWrongCommand = 0
#             await ctx.send("saved!")
#         except : 
#             await ctx.send("Didn't work!")
#     else :
#         await ctx.send("Tu n'as pas le droit")

# @bot.command()
# @commands.cooldown(100,24*3600)
# async def total(ctx, *args):
#     if ( ctx.message.author.id == 302536904824586241):
#         listfiles = os.listdir("stats/")
#         nbWar, nbTt , nbSettings , nbHelp , nbWrong = 0,0,0,0,0
#         for statsFile in listfiles :
#             with open("stats/"+statsFile,'r') as w:
#                 stats = json.load(w)
#                 for key in stats.keys():
#                     if key == "War":
#                         nbWar += stats.get(key)
#                     if key == "Tt":
#                         nbTt += stats.get(key)
#                     if key == "Settings":
#                         nbSettings += stats.get(key)
#                     if key == "Help":
#                         nbHelp += stats.get(key)
#                     if key == "Wrong":
#                         nbWrong += stats.get(key)
#         DateDiff = date.today() - date(2021,5,28)# nb days since the start of stats
#         days = DateDiff.days
#         message = "```Nombre de commande utilisé en moyenne depuis le 28 mai 2021 :\nWar : {:.2f} \nTt : {:.2f} \nSettings : {:.2f}\nHelp : {:.2f}\nCmd Raté: {:.2f}```".format(nbWar/days,nbTt/days,nbSettings/days,nbHelp/days,nbWrong/days)
#         await ctx.send(message)

# @bot.tree.command()
# async def update(interaction : discord.Interaction):
#     if ( interaction.guild_id == 302544642585526293 or interaction.guild_id == 518942329181175808):
#         nbfile = 0
#         if (os.path.exists(path)):
#             listfile = os.listdir(path)

#             for f in listfile :
#                 for speed in os.listdir(path+f):
#                     if ( os.path.exists(path+f+"/"+speed+"/bap")):
#                         os.rename(path+f+"/"+speed+"/bap", path+f+"/"+speed+"/brrm")
#                 nbfile +=1
#         await interaction.response.send_message("nbfile = " + str(nbfile))
        

bot.run(TOKEN)
