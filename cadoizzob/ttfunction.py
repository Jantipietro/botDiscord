import mapmk
import discord
import ttplayer
import os 
from text import path, ttTexts
from settings import get_language

# Bad fonction to get author nickname or name
def checkname(ctx):
    if ctx.message.author.nick == None :
        return ctx.message.author.name
    else :
        return ctx.message.author.nick

# 3 functions to find a player in the ctx . 
# Find idPLayer in mapmk8 and idPLayer and his place in maps
# return namePlayer to get the name if your are looking for someone
def findInMap(ctx ,idPlayer, namePlayer, mapmk8, maps, shroom):
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+str(ctx.guild.id)+"/"+ shroom + mapmk8)  
    if data != 'no file':
        mk.dataToMapmk(data)
        addMap = False
        i = 1 # will count how many players in the map
        for player in mk._ttplayers :
            if player.getPlayerId() == int(idPlayer) :
                namePlayer = player.getPlayerName()
                addMap = True
                place = i # Classement of the player
                break
            else :
                i += 1
        if addMap == True :
            maps.append((mapmk8, place , len(mk._ttplayers) ))
        return namePlayer
    return namePlayer
    
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
    playerName = ""
    for mapmk8 in mapmk.MK8DXmap.keys() :
        if mapmk8 != 'week' :
            playerName = findInMap(ctx,idPlayer,playerName,mapmk8, maps, shroom)
    if playerName == "" :
        playerName = idPlayer
    await drawFind(ctx, maps, playerName, shroom)

# 3 function to get the Stats of the ctx . 
# get stats of one maps
def MapStats(ctx, mapmk8, playersStats, shroom):
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+str(ctx.guild.id)+"/"+shroom+mapmk8)  
    if data != 'no file':
        mk.dataToMapmk(data)
        mk.addStats(playersStats)

# Return total stats points at 10^-5 
# add nbplayer to the total for every map missing 
def fillPoint(total, mapPlayed, nbplayer):
    return round((total + (nbplayer*(48-mapPlayed)))/48, 5)

async def drawStats(ctx, playersStats, shroom):
    # sort by the average place
    nbPlayer = len(playersStats)
    sorted_playersStats = sorted(playersStats.values(), key=lambda value : fillPoint(value[1],value[2],nbPlayer), reverse= False)
    title = "Stats Average place : {0}".format(ctx.guild)
    if shroom == 'noshroom/':
        title += " Shroomless"
    description = ""
    i= 1
    for playerlist in sorted_playersStats:
        description += "**{3}.{0}** : {1} ( {2}/48 maps )\n".format(playerlist[0], fillPoint(playerlist[1],playerlist[2],nbPlayer) , playerlist[2], i)
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

#Set on mapmk8 the objective time. 
# Two type of objective.
async def setMapmkObjective(ctx, mapmk8, time, bonus, shroom) :
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+str(ctx.guild.id)+"/"+shroom+mapmk8)
    if data != 'no file':
        mk.dataToMapmk(data)
    if bonus == '':
        mk.setObjective(time)
    else :
        mk.setBonusObjective(time)
    mk.writeFile(path+str(ctx.guild.id)+"/"+shroom+mapmk8)

async def deleteFile(ctx, file, mapmk8):
    try :
        os.remove(file)
        await ctx.send (ttTexts.get(get_language(ctx)).get("mapFileSup").format(mapmk8))
    except :
        await ctx.send(ttTexts.get(get_language(ctx)).get("noMapFile"))

#Delete if from mapmk8
async def deleteTtplayerfromMap(ctx,mapmk8, id, shroom):
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+str(ctx.guild.id)+"/"+shroom+mapmk8)
    if data != 'no file':
        mk.dataToMapmk(data)
        mk.deleteTtplayer(id)
        if len(mk._ttplayers) !=0 :
            mk.writeFile(path+str(ctx.guild.id)+"/"+shroom+mapmk8)
        else :
            await ctx.send(ttTexts.get(get_language(ctx)).get("noMorePlayer").format(mapmk8))
            await deleteFile(ctx, path+str(ctx.guild.id)+"/"+shroom+mapmk8, mapmk8)

#Delete if from all maps
async def deleteTtplayerfromAll(ctx, id, shroom):
    for mapmk8 in mapmk.MK8DXmap.keys() :
        await deleteTtplayerfromMap(ctx, mapmk8, id, shroom)
    await ctx.send(ttTexts.get(get_language(ctx)).get("supPlayer").format(id))

#Add ctx.author time in mapmk8
async def addTimeInFile(ctx, mapmk8, time ,shroom):
    mk = mapmk.mapmk(mapmk8, '' , '') #create a object mapmk with the name of the map
    data = mk.getFileR(path+str(ctx.guild.id)+"/"+shroom+mapmk8) # get the data from file
    mk.dataToMapmk(data)
    name = checkname(ctx)  # check if someone has a nick name
    newplayer = ttplayer.TtPlayer( ctx.message.author.id, #create new ttplayer
                name,
                time)
    mk.addplayer(newplayer)
    mk.writeFile(path+str(ctx.guild.id)+"/"+shroom+mapmk8)
    await ctx.send( ttTexts.get(get_language(ctx)).get("addTimeMap").format(mapmk8))

async def drawMapmk(ctx , mapmk8, shroom):
    mk = mapmk.mapmk(mapmk8, '', '') #create a object mapmk with the name of the map
    data = mk.getFileR(path+str(ctx.guild.id)+"/"+shroom+mapmk8) # get the data from file
    if data == 'no file':
        await ctx.send(ttTexts.get(get_language(ctx)).get("noFileMap"))
    else :
        mk.dataToMapmk(data)
        description=""
        if mk._objective != "" :
            description += "Objectif : **" + mk._objective + "**\n"
        if mk._bonusObjective != "":
            description  += "Objectif Bonus: **" + mk._bonusObjective + "**\n"
        description +='\n'
        i = 1
        placeField =""
        nameField= ""
        timeField = ""
        for player in mk._ttplayers:
            placeField +=str(i)+"\n"
            nameField += str(player.getPlayerName())+"\n"
            timeField += str(player.getPlayerTime())+"\n"
            i= i+1
        title = mapmk.MK8DXmap.get(mapmk8)
        if shroom == 'noshroom/':
            title += ' Shroomless'
        embedMap = discord.Embed(title=title,description=description)
        embedMap.add_field(name='Place', value = placeField , inline= True)
        embedMap.add_field(name='Name', value = nameField , inline= True)
        embedMap.add_field(name='Time', value = timeField , inline= True)
        embedMap.set_thumbnail(url = "https://cdn.discordapp.com/attachments/729655998146674748/731625550858158102/cadoizz-bot-400x400px.png")
        await ctx.send(embed = embedMap)

#Look for ctx.author.id in mapmk8 in the guild fromServ
def getCopyInMap(ctx , fromServ, mapmk8, maps, shroom):
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+fromServ+"/"+ shroom + mapmk8)  
    if data != 'no file':
        mk.dataToMapmk(data)
        for player in mk._ttplayers :
            if player.getPlayerId() == ctx.author.id :
                maps.append((mapmk8, player.getPlayerTime() ))
                break
        return maps
    return maps

#Copy ctx.author.id's time from fromServ
async def copy(ctx,fromServ, shroom):
    maps = list()
    for mapmk8 in mapmk.MK8DXmap.keys() :
        if mapmk8 != 'week' :
            maps = getCopyInMap(ctx, fromServ, mapmk8, maps, shroom)
    for (mapeuh, time) in maps :
        await addTimeInFile(ctx, mapeuh, time ,shroom)