#!/usr/bin/env python3
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
import shutil
import re
import mapmk
import ttplayer
import json
from ttfunction import *
#Put your Token bot here 
TOKEN = "NzI5NjQ4NTE2Nzk1OTkwMTQ2.Xxl8RQ.QxAGUjYIHoRKc92YtPMqEzaxeDo"
bot = discord.Client()
# You can change the prefix here 
bot= commands.Bot(command_prefix ="c!")

path = "tt/"
shroomPath = "shroom/"
noShroomPath = "noshroom/"

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("-------")

# FOrmat of the TT time; example : 
timesample = re.compile('\d:\d{2}\.\d{3}')
idsample = re.compile('\d{10,30}')
tagsample = re.compile('<@!\d{10,30}>')

# Dict of string for the war command 
warText = { 
    "help": "```----- FR -----\n\n"
            + "c!war vacances  --> Propose des wars de 14h à 01h du matin\n"
            + "c!war XX XX...  --> Propose des wars à XXh. Exemple : c!war 18 21 23\n\n"
            + "Principes importants du bot :\n"
            + "• Le bot ajoute un 'h' à chaque mot écrit après c!war (sauf 'c!war vacances')\n"
            + "• Le bot ajoute les 3 emotes sur son propre message suite à la commande utilisée\n"
            + "• Sur tous les messages du discord : le bot enlève sa propre emote dès qu'il y a 4 émotes sur le message + le bot remet sa propre emote dès que les emotes redescendent à 1 (de ce fait il garde toujours l'ordre des emotes)\n\n"
            + "Si vous avez des retours ou des idées de commandes à ajouter qui pourraient être sympas, n'hésitez pas à me MP à @Cadoizz#5176 !\n\n\n"
            + "----- EN -----\n\n"
            + "c!war vacances  --> Propose wars from 14h to 01h of the morning\n"
            + "c!war XX XX...  --> Propose wars at XXh. Example: c!war 18 21 23\n\n"
            + "Important principles of the bot:\n"
            + "• The bot adds an 'h' to every word written after c!war (except 'c!war vacances')\n"
            + "• Once the command is used the bot will add the 3 emotes to its own message\n"
            + "• On all discord messages: the bot removes its own emote as soon as therare 4 emotes on the message + the bot gives his own emote as soon as the emotes go down to 1 (thereby it always keeps the emote order)\n\n"
            + "If you have any feedback or ideas to add that might be nice, feel free to DM me at @Cadoizz#5176!```",
    
    "args" : "Pas d'arguments à la commande war! pour plus d'infos **c!war help** ",
    "noOption" : "Coucou on a pas ton option **c!war help** est la pour te servir"  
    }

@bot.command()
async def war(ctx, *args):
    if not args:
        await ctx.send(warText.get("args"))
    if args[0] == 'help':
        await ctx.send(warText.get("help"))
    elif args[0] == 'vacances':
        for i in range(14,26): # de 14 à 24
            message = await ctx.send('war '+str(i%24)+'h')
            await message.add_reaction("✅")
            await message.add_reaction("❌")
            await message.add_reaction("❔")
    elif args[0] < '24':
        for i in range(len(args)):
            message = await ctx.send('war '+args[i]+'h')
            await message.add_reaction("✅")
            await message.add_reaction("❌")
            await message.add_reaction("❔")

    else :
        await ctx.send(warText.get("noOption"))

ttTexts = {
    "help"      :  "```<map> correspond soit aux raccourcis anglais des maps de mk8dx et à 'week' si vous voulez vous faire un tt de la semaine, de plus la commande c!tt maps , renvoie une image avec les raccourcis utilisés.\n"
                    +"<time> doit suivre le modèle suivant : x:xx.xxx ; où les x sont des chiffres\n"
                    +"<id> correspond à l'identifiant discord de quelqu'un sinon celà ne marche pas \n"
                    +"Tous les arguments peuvent être passé en miniscule ou majuscule, le bot les lira en minuscules.\n "
                    +"----------------------------------------------------------\n"
                    +"Ces commandes ne demandent aucun droit n'importe qui sur le serveur peut les utiliser\n"
                    +"Ajouter 'ni' après c!tt , fait réfèrence au run no item , soit shroomless! Toutes les commandes suivantes marche de la même manière avec 'ni'. Exemple : c!tt ni find . \n\n "
                    +"c!tt <map> --> affiche si un fichier existe les temps de la map.\n" 
                    +"c!tt <map> <time> --> ajoute ton temps à la <map>\n"
                    +"c!tt <map> delete --> Supprime ton temps de la map\n"
                    +"c!tt find --> Trouve toutes les maps ou tu apparais\n"
                    +"c!tt find <id> --> Trouve toutes les maps ou <id> apparait\n"                   
                    +"c!tt stats --> Montre un classement des membres par point\n"
                    +"Il faut 3 membres dans une map pour qu'elle compte et la map 'week' ne compte pas\n\n"
                    +"----------------------------------------------------------\n"
                    +"Les commandes ci-dessous demandent d'avoir le droit de gérer les messages sur le serveur\n\n"
                    +"c!tt create --> Creer un dossier pour le serveur et permet d'y stocker les maps\n\n"
                    +"c!tt delete --> Supprime le dossier du serveur et ce qu'il y'a dedans\n\n"
                    +"c!tt delete <id> --> Supprime tous les temps de <id> dans les fichiers\n\n"
                    +"c!tt delete <map> --> Supprime le fichier d'une map \n\n"
                    +"c!tt <map> delete <id> --> Supprime le joueur <id> dans le fichier <map>\n\n"
                    +"c!tt <map> objective <time> --> Ajoute <time> à la variable objective\n\n"
                    +"c!tt <map> bonus <time> --> Ajoute <time> à la variable ObjectiveBonus\n\n"
                    +"c!tt <map> objective delete --> Supprime le temps objective\n\n"
                    +"c!tt <map> bonus delete --> Supprime le temps objectiveBonus\n```",
    "perm"      : "Tu n'as pas les perms pour cette commande",
    "arg"       : "Pas d'arguments à la commande tt ! pour plus d'infos **c!tt help** ",
    "create"    : "Votre Serveur a maintenant un fichier des TT , il vous reste à les remplirs",
    "pathExist" : "Votre serveur a deja un fichier, **c!tt help**, pour savoir comment rentré vos temps",
    "delete"    : "Les fichiers de TT ont bien été supprimé",
    "wrongName" : "Cette commande ou map n'existe pas",
    "noFile"    : "Votre serveur n'a pas de fichier , utiliser la commande *c!tt create** pour en avoir un"
                    +" et pouvoir ajoutez vos temps sur les maps.",
    "noFileMap" : "Pas de fichier pour cette map, ajoutes un temps pour le créer." ,
    "badFormat" : "Temps au mauvais format, exemple : 1:20.546 \n ou trop d'arguments.",
    "registred" : "Votre temps a bien été enregistré."
}

async def findCommand(ctx , args , shroom):
    if len(args) == 1 :
        await find(ctx, ctx.author.id, shroom)
    elif len(args) == 2 :
        if idsample.match(args[1]):
            await find(ctx, args[1], shroom)
        else :
            await ctx.send("Ceci ne ressemble pas un id discord.")
    else :
        await ctx.send("Faut juste mettre l'id du joueur après find couillon")

async def deleteCommand(ctx , args , shroom ):
    if not ctx.message.author.guild_permissions.manage_messages:
        await ctx.send( ttTexts.get("perm"))
    #Delete all the file and the server name's file too
    elif len(args) == 1 :
        try :
            shutil.rmtree(path+str(ctx.guild))
            await ctx.send( ttTexts.get("delete"))
        except :
            # normally never happens, don't think rmtree can fail but in case
            await ctx.send("Vos fichiers n'ont pas été supprimé, ceci ne devrait pas arrivé")
    # Delete an id from all the file 
    elif len(args) == 2 :
        if idsample.match(args[1]):
            await deleteTtplayerfromAll(ctx, args[1], shroom)
        # Delete a map file
        elif mapmk.MK8DXmap.get(args[1]) != None :
            await deleteFile(ctx , path+str(ctx.guild)+"/"+shroom +args[1] , args[1])
        else :
            await ctx.send("Ceci ne ressemble pas a un id discord, ou pas de nom de map")
    else :
        await ctx.send("Trop d'args frerot!")

async def mapmkCommand( ctx , args , shroom):
    if os.path.exists(path+str(ctx.guild)):
        # DRAW TT 
        if len(args)== 1 :
            await drawMapmk(ctx, args[0], shroom)
        # Add objectif 
        elif args[1] == 'objective' or args[1] == 'bonus' :
            if not ctx.message.author.guild_permissions.manage_messages:
                await ctx.send( ttTexts.get("perm"))
            elif len(args) == 3 :
                if timesample.match(args[2]):
                    if args[1] == 'objective' :
                        await setMapmkObjective(ctx, args[0], args[2], '', shroom)
                        await ctx.send("Objectif ajouté ")
                    else :
                        await setMapmkObjective(ctx, args[0], args[2], 'bonus', shroom)
                        await ctx.send("Objectif Bonus ajouté ")
                # put objectif at null
                elif args[2] == 'delete':
                    if args[1] == 'objective' :
                        await setMapmkObjective(ctx, args[0], '', '', shroom)
                        await ctx.send("Objectif Supprimé ")
                    else :
                        await setMapmkObjective(ctx, args[0], '', 'bonus', shroom)
                        await ctx.send("Objectif Bonus Supprimé ")
                else :
                    await ctx.send( ttTexts.get("badFormat"))
            else:
                await ctx.send (" Trop d'arguments")
        # Delete time into file
        elif args[1]== 'delete':
            if len(args)== 2 :
                await deleteTtplayerfromMap(ctx,args[0], ctx.message.author.id, shroom)
                await ctx.send("Votre temps a bien été supprimé")
            elif len(args)==3:
                if not ctx.message.author.guild_permissions.manage_messages:
                    await ctx.send( ttTexts.get("perm"))
                elif idsample.match(args[2]):
                    await deleteTtplayerfromMap(ctx,args[0], args[2], shroom)
                    await ctx.send("Le temps du joueur a bien été supprimé.")
                else :
                    await ctx.send("L'id du joueur ne ressemble a rien frérot.")
        # ADD TTplayer in file
        elif timesample.match(args[1]):
            await addTimeInFile(ctx, args[0], args[1], shroom)
        else : 
            # Bad timing format
            await ctx.send( ttTexts.get("badFormat"))
    else :
        #No server file 
        await ctx.send( ttTexts.get("noFile"))

def lowerM (args):
    lowerarg=[]
    for arg in args:
        # to use tag instead of finding the user id ( made it after writing a lot of file )
        if tagsample.match(arg):
            newarg = arg.strip('<!@>')
            lowerarg.append(str.lower(newarg))
        else :
            lowerarg.append(str.lower(arg))
    return lowerarg

@bot.command()
async def tt(ctx, *args):
    if not args :
        await ctx.send(  ttTexts.get("arg"))
    else :
        args= lowerM(args)
        if args[0] == 'help':
            await ctx.send ( ttTexts.get("help"))
        # Draw png with all maps and how to write it
        elif args[0] == 'maps' :
            await ctx.send("https://media.discordapp.net/attachments/579573532263055381/583008091541471234/abveration.png?width=1202&height=510")
        elif args[0] == 'stats':
            await Stats(ctx, shroomPath)
        #Chercher le joueur dans les maps 
        elif args[0] == 'find' :
            await findCommand(ctx, args , shroomPath)
        #Create files with the server name
        elif args[0] == 'create':
            if not ctx.message.author.guild_permissions.manage_messages :
                await ctx.send( ttTexts.get("perm"))
            else :
                try :
                    os.makedirs(path+str(ctx.guild)+"/"+shroomPath)
                    os.makedirs(path+str(ctx.guild)+"/"+noShroomPath)
                    await ctx.send( ttTexts.get("create"))
                except :
                    await ctx.send( ttTexts.get("pathExist"))
        # Delete all file from the server that call this.
        elif args[0] == 'delete':
            await deleteCommand(ctx, args , shroomPath)
        # Check if the first arg is a map name
        elif mapmk.MK8DXmap.get(args[0]) != None :
            await mapmkCommand(ctx, args , shroomPath)
        # Noshroom way ^^
        elif args[0] == 'ni' :
            del args[0] # to call the other function , delete the arg "ni"
            if args[0] == 'stats':
                await Stats(ctx, noShroomPath)
            #Chercher le joueur dans les maps 
            elif args[0] == 'find' :
                await findCommand(ctx, args , noShroomPath)
                    # Delete all file from the server that call this.
            elif args[0] == 'delete':
                await deleteCommand(ctx, args , noShroomPath)
            # Check if the first arg is a map name
            elif mapmk.MK8DXmap.get(args[0]) != None :
                await mapmkCommand(ctx, args , noShroomPath)
            else :
                await ctx.send("Commande inconnue !")
        else :
        # wrong map name or command doesn't exist
            await ctx.send( ttTexts.get("wrongName"))


@bot.event
async def on_reaction_add(reaction, user):
    if reaction.count == 4:
            await reaction.message.remove_reaction(reaction, bot.user)

@bot.event
async def on_reaction_remove(reaction, user):
    if reaction.count == 1:
        await reaction.message.add_reaction(reaction)

bot.run(TOKEN)
