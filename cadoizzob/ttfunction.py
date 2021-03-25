import mapmk
import discord
import ttplayer
import os 
from text import path, ttTexts, tagsample
from settings import get_language
from datetime import datetime
from text import speedPath, urlImgCadoizzob, nofile

nbPlayerDisplayedStats = 50
nbPlayerDisplayedMap = 20

# Bad fonction to get author nickname or name
def checkname(ctx):
    if ctx.message.author.nick == None :
        return ctx.message.author.name
    else :
        return ctx.message.author.nick

#Update : Make it cleaner
def titleType(shroom):
    if shroom.startswith(speedPath,0,len(speedPath)): 
        if shroom == speedPath+'noshroom/':
                return ' Shroomless 200cc'
        else :
            return ' 200cc'
    if shroom == 'noshroom/':
        return " Shroomless"
    return ''

async def setEmoji(message,page , length, option = ""):        #add row left or right
        if ( page != 1) :
            await message.add_reaction("⬅️") # row left
        if ( nbPlayerDisplayedMap*page < length):        
            await message.add_reaction("➡️") # row right
# 3 functions to find a player in the ctx . 
# Find idPLayer in mapmk8 and idPLayer and his place in maps
# return namePlayer to get the name if your are looking for someone
def findInMap(ctx ,idPlayer, namePlayer, mapmk8, maps, shroom):
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+str(ctx.guild.id)+"/"+ shroom + mapmk8)  
    if data != nofile:
        mk.dataToMapmk(data)
        addMap = False
        i = 1 # will count how many players in the map
        for player in mk._ttplayers :
            if player.getPlayerId() == int(idPlayer) :
                namePlayer = player.getPlayerName()
                timePlayer = player.getPlayerTime()
                addMap = True
                place = i # Classement of the player
                break
            else :
                i += 1
        if addMap == True :
            maps.append((mapmk8, place , timePlayer, len(mk._ttplayers) ))
        return namePlayer
    return namePlayer
    
async def drawFind(ctx , maps, playerName, shroom):
    title = "Player : {0}".format(playerName)
    title += titleType(shroom)
    description = ""
    j = 0
    for (mapmk8, place ,time, i) in maps:
        j += 1
        description += "{0} : **{1}/{2}** -> {3}\n".format(mapmk8, place , i, time)
    if description == "" :
        await ctx.send ("Pas de temps pour {0}".format(playerName))
    else :
        embedMap = discord.Embed(title=title,description=description)
        embedMap.set_thumbnail(url = urlImgCadoizzob)
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
def MapStats(ctx, option, mapmk8, playersStats, shroom):
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+str(ctx.guild.id)+"/"+shroom+mapmk8)  
    if data != nofile:
        mk.dataToMapmk(data)
        if ( option == ""):
            mk.addStats(playersStats)
        else :
            mk.addStatsTime(playersStats)

# Return total stats points at 10^-5 
# add nbplayer to the total for every map missing 
def fillPoint(total, mapPlayed, nbplayer):
    return round((total + (nbplayer*(48-mapPlayed)))/48, 5)

def addTime(playertime):
        (h , m ,s , ms) = playertime
        addtos = ms//1000
        newms = ms%1000
        rs = ((s+addtos)//60)
        news = (s+addtos)%60
        newh = ((m+rs)//60)
        newm = (h+m+rs)%60
        return ( newh, newm , news, newms)


async def drawStats(ctx,option, playersStats, shroom , page):
    # sort by the average place
    nbPlayer = len(playersStats)
    if (option == ""):
        sorted_playersStats = sorted(playersStats.values(), key=lambda value : fillPoint(value[1],value[2],nbPlayer), reverse= False)
        title = "Stats Average place : {0}".format(ctx.guild)
    else :
        newplayersStats = { k:v for k,v in playersStats.items() if v[2] == 48}
        sorted_playersStats = sorted(newplayersStats.values(), key=lambda value : addTime(value[1]) , reverse = False)
        title = "Stats Total Time : {0}".format(ctx.guild)
    title += titleType(shroom)
    description = ""
    i= 1
    for playerlist in sorted_playersStats:
        if (i == (page)*(nbPlayerDisplayedStats)+1): # draw nbPlayerDisplayedStats
            break
        if(i > (page-1)*nbPlayerDisplayedMap):
            if ( option == ""):
                description += "**{3}.{0}** : {1} ( {2}/48 maps )\n".format(playerlist[0], fillPoint(playerlist[1],playerlist[2],nbPlayer) , playerlist[2], i)
                i += 1
            else :
                (h , m , s, ms ) = addTime(playerlist[1])
                description += "**{}.{}** : {}:{:02d}:{:02d}.{:03d}\n".format(i,playerlist[0],h, m , s, ms, )
                i+= 1
    if description == "" :
        await ctx.send ("Pas de stats pour ce serveur.")
    else :
        embedMap = discord.Embed(title=title,description=description)
        embedMap.set_thumbnail(url = urlImgCadoizzob)
        embedMap.set_footer(text = str(page))
        message = await ctx.send(embed = embedMap)
        await setEmoji(message,page , len(sorted_playersStats) )
    
async def Stats(ctx, option, shroom):
    playersStats = dict()
    for mapmk8 in mapmk.MK8DXmap.keys() :
        if mapmk8 != 'week' :
            MapStats(ctx, option, mapmk8, playersStats, shroom)
    await drawStats(ctx,option, playersStats, shroom, 1)

#Set on mapmk8 the objective time. 
# Two type of objective.
async def setMapmkObjective(ctx, mapmk8, time, bonus, shroom) :
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+str(ctx.guild.id)+"/"+shroom+mapmk8)
    if data != nofile:
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
    if data != nofile:
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

async def drawMapmk(ctx , mapmk8, shroom, page):
    mk = mapmk.mapmk(mapmk8, '', '') #create a object mapmk with the name of the map
    data = mk.getFileR(path+str(ctx.guild.id)+"/"+shroom+mapmk8) # get the data from file
    if data == nofile:
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
        for player in mk._ttplayers:
            if (i == (page)*(nbPlayerDisplayedMap+1)) : # draw nbPlayerDisplayedMap players
                break
            if(i >= (page-1)*nbPlayerDisplayedMap):
                description += "**{}. {}** : {}\n".format(i , player.getPlayerName() , player.getPlayerTime())
            i= i+1
        title = mapmk.MK8DXmap.get(mapmk8)
        title += titleType(shroom)
        embedMap = discord.Embed(title=title,description=description)
        embedMap.set_thumbnail(url = urlImgCadoizzob)
        embedMap.set_footer(text = str(page))
        message = await ctx.send(embed = embedMap)
        await setEmoji(message,page , len(mk._ttplayers))

#Look for ctx.author.id in mapmk8 in the guild fromServ
def getCopyInMap(ctx , fromServ, mapmk8, maps, shroom):
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+fromServ+"/"+ shroom + mapmk8)  
    if data != nofile:
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


######## THE FOLLOW IS DISGUSTING #######
async def drawPlayerCommand(ctx,ListOfplayer, mapmk8, shroom):
    mk = mapmk.mapmk(mapmk8, '', '') #create a object mapmk with the name of the map
    data = mk.getFileR(path+str(ctx.guild.id)+"/"+shroom+mapmk8) # get the data from file
    if data == nofile:
        await ctx.send(ttTexts.get(get_language(ctx)).get("noFileMap"))
    else :
        mk.dataToMapmk(data)
        title = ListOfplayer.get("player")[0].getPlayerName() + " : " + mapmk.MK8DXmap.get(mapmk8)
        title += titleType(shroom)
        embedMap = discord.Embed(title=title)
        for (k,v) in ListOfplayer.items() :
            if k == "oldPlayer" :
                if v == None :
                    oldPlayerName = "None"
                    oldPlayerField = ""
                else :
                    player , place = v
                    oldPlayerName= player.getPlayerName()
                    oldPlayerField ="" + place + "\n"
                    oldPlayerField += player.getPlayerTime() +"\n"
                    (mins,second, milli) = ListOfplayer.get("player")[0].getDifSecond(player)
                    if mins != 0 :
                        oldPlayerField +=  "**-{:02}:{:02}.{:03}**\n".format(mins, second , milli)
                    else :
                        oldPlayerField +=  "**-{:02}.{:03}**\n".format( second , milli)
                    embedMap.add_field(name=oldPlayerName, value = oldPlayerField , inline= True)
            if k == "player" :
                if v == None :
                    playerField = ""
                else :
                    player , place = v
                    playerField ="" + place + "\n"
                    playerField += player.getPlayerTime() +"\n"
                   # playerField += "allez hola holé"
                    embedMap.add_field(name=player.getPlayerName(), value = playerField , inline= True)
            if k == "nextPlayer" :
                if v == None :
                    nextPlayerName= "None"
                    nextPlayerField = ""
                else :
                    player , place = v
                    nextPlayerName = player.getPlayerName()
                    nextPlayerField ="" + place + "\n"
                    nextPlayerField += player.getPlayerTime() +"\n"
                    (mins,second, milli) = player.getDifSecond(ListOfplayer.get("player")[0])
                    if mins != 0 :
                        nextPlayerField +=  "**+{:02}:{:02}.{:03}**\n".format(mins, second , milli)
                    else :
                        nextPlayerField +=  "**+{:02}.{:03}**\n".format( second , milli)
                    embedMap.add_field(name=nextPlayerName, value = nextPlayerField , inline= True)
        embedMap.set_thumbnail(url = "https://cdn.discordapp.com/attachments/729655998146674748/731625550858158102/cadoizz-bot-400x400px.png")
        await ctx.send(embed = embedMap)

# get the two around the player 
def findInMapBis(ctx ,idPlayer, mapmk8, shroom):
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+str(ctx.guild.id)+"/"+ shroom + mapmk8)  
    if data != nofile:
        mk.dataToMapmk(data)
        ListOfPlayer = {"oldPlayer" : None , "player" : None, "nextPlayer": None}
        i = 1 # will count how many players in the map
        playerfound = False
        for player in mk._ttplayers :
            if playerfound == True :
                ListOfPlayer.update({"nextPlayer"  : (player, str(i))} )
                break
            if player.getPlayerId() == int(idPlayer) :
                playerfound = True
                ListOfPlayer.update({"player" : (player, str(i))} )
                i += 1
            else :
                oldplayer = player
                i += 1
            if playerfound == True and i != 2:
                ListOfPlayer.update({"oldPlayer" : (oldplayer, str(i-2))} )
        return ListOfPlayer
    else :
        return []


            

