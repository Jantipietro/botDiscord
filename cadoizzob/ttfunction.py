import mapmk
import discord
import ttplayer
import os 

path = "tt/"


def checkname(ctx):
    if ctx.message.author.nick == None :
        return ctx.message.author.name
    else :
        return ctx.message.author.nick
# 3 functions to find a player in the ctx . 
def findInMap(ctx ,idPlayer, mapmk8, maps, shroom):
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+str(ctx.guild)+"/"+ shroom + mapmk8)  
    if data != 'no file':
        mk.dataToMapmk(data)
        addMap = False
        i = 1 # will count how many players in the map
        for player in mk._ttplayers :
            if player.getPlayerId() == int(idPlayer) :
                playerName = player.getPlayerName()
                addMap = True
                place = i # Classement of the player 
                i += 1
            else :
                i += 1
        if addMap == True :
            maps.append((mapmk8, place , (i-1) ))
        if addMap == False :
            playerName = str(idPlayer)
        return (playerName, maps)
    return ("", maps)
    
async def drawFind(ctx , maps, playerName, shroom):
    title = "Player : {0}".format(playerName)
    if shroom == 'noshroom/':
        title += " Shroomless"
    description = ""
    for (mapmk8, place , i) in maps:
        description += "{0}  {1}/{2} , ".format(mapmk8, place , i)
    if description == "" :
        await ctx.send ("Pas de temps pour {0}".format(playerName))
    else :
        embedMap = discord.Embed(title=title,description=description)
        embedMap.set_thumbnail(url = "https://cdn.discordapp.com/attachments/729655998146674748/731625550858158102/cadoizz-bot-400x400px.png")
        await ctx.send(embed = embedMap)

async def find(ctx, idPlayer, shroom):
    maps = list()
    name = ""
    for mapmk8 in mapmk.MK8DXmap.keys() :
        if mapmk8 != 'week' :
            (playerName , maps ) = findInMap(ctx,idPlayer,mapmk8, maps, shroom)
            if playerName != "" :
                name = playerName # Keep the playerName 
    if name == "" :
        name = idPlayer
    await drawFind(ctx, maps, name, shroom)

# 3 function to get the Stats of the ctx . 
def MapStats(ctx, mapmk8, playersStats, shroom):
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+str(ctx.guild)+"/"+shroom+mapmk8)  
    if data != 'no file':
        mk.dataToMapmk(data)
        mk.addStats(playersStats)
    
async def drawStats(ctx, playersStats, shroom):
    # trie par nombre de point 
    sorted_playersStats = sorted(playersStats.values(), key=lambda value : value[1] , reverse= True)
    title = "Stats : {0}".format(ctx.guild)
    if shroom == 'noshroom/':
        title += " Shroomless"
    description = ""
    i= 1
    for playerlist in sorted_playersStats:
        description += "**{3}.{0}** : {1} points ( {2}/48 maps )\n".format(playerlist[0], playerlist[1] , playerlist[2], i)
        i += 1
    if description == "" :
        await ctx.send ("Pas de stats pour ce serveur.")
    else :
        embedMap = discord.Embed(title=title,description=description)
        embedMap.set_thumbnail(url = "https://cdn.discordapp.com/attachments/729655998146674748/731625550858158102/cadoizz-bot-400x400px.png")
        await ctx.send(embed = embedMap)
    

async def Stats(ctx, shroom):
    playersStats = dict()
    for mapmk8 in mapmk.MK8DXmap.keys() :
        if mapmk8 != 'week' :
            MapStats(ctx, mapmk8, playersStats, shroom)
    await drawStats(ctx, playersStats, shroom)

async def setMapmkObjective(ctx, mapmk8, time, bonus, shroom) :
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+str(ctx.guild)+"/"+shroom+mapmk8)
    if data != 'no file':
        mk.dataToMapmk(data)
    if bonus == '':
        mk.setObjective(time)
    else :
        mk.setBonusObjective(time)
    mk.writeFile(path+str(ctx.guild)+"/"+shroom+mapmk8)


async def deleteFile(ctx, file, mapmk8):
    try :
        os.remove(file)
        await ctx.send (" La fichier de la map {0} a été supprimé".format(mapmk8))
    except :
        await ctx.send("Pas de fichier de ce nom")

async def deleteTtplayerfromMap(ctx,mapmk8, id, shroom):
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+str(ctx.guild)+"/"+shroom+mapmk8)
    if data != 'no file':
        mk.dataToMapmk(data)
        mk.deleteTtplayer(id)
        if len(mk._ttplayers) !=0 :
            mk.writeFile(path+str(ctx.guild)+"/"+shroom+mapmk8)
        else :
            await ctx.send("Plus de joueur dans la map")
            await deleteFile(ctx, path+str(ctx.guild)+"/"+shroom+mapmk8, mapmk8)

async def deleteTtplayerfromAll(ctx, id, shroom):
    for mapmk8 in mapmk.MK8DXmap.keys() :
        await deleteTtplayerfromMap(ctx, mapmk8, id, shroom)
    await ctx.send("Le joueur avec l'id {0} a été supprimé de tous les fichiers".format(id))

async def addTimeInFile(ctx, mapmk8, time ,shroom):
    mk = mapmk.mapmk(mapmk8, '' , '') #create a object mapmk with the name of the map
    data = mk.getFileR(path+str(ctx.guild)+"/"+shroom+mapmk8) # get the data from file
    mk.dataToMapmk(data)
    name = checkname(ctx)  # check if someone has a nick name
    newplayer = ttplayer.TtPlayer( ctx.message.author.id, #create new ttplayer
                name,
                time)
    mk.addplayer(newplayer)
    mk.writeFile(path+str(ctx.guild)+"/"+shroom+mapmk8)
    await ctx.send( "Votre temps a bien été enregistré.")



async def drawMapmk(ctx , mapmk8, shroom):
    mk = mapmk.mapmk(mapmk8, '', '') #create a object mapmk with the name of the map
    data = mk.getFileR(path+str(ctx.guild)+"/"+shroom+mapmk8) # get the data from file
    if data == 'no file':
        await ctx.send( "Pas de fichier pour cette map, ajoutes un temps pour le créer.")
    else :
        mk.dataToMapmk(data)
        description=""
        if mk._objective != "" :
            description += "Objectif : **" + mk._objective + "**\n"
        if mk._bonusObjective != "":
            description  += "Objectif Bonus: **" + mk._bonusObjective + "**\n"
        description +='\n'
        i = 1
        for player in mk._ttplayers:
            description += "**"+str(i)+". "
            description += player.string()
            i+=1
        title = mapmk.MK8DXmap.get(mapmk8)
        if shroom == 'noshroom/':
            title += ' Shroomless'
        embedMap = discord.Embed(title=title,description=description)
        embedMap.set_thumbnail(url = "https://cdn.discordapp.com/attachments/729655998146674748/731625550858158102/cadoizz-bot-400x400px.png")
        await ctx.send(embed = embedMap)
