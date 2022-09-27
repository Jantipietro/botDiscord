import mapmk
import discord
import ttplayer
import os 
from text import path, ttTexts, tagsample, nbMK8DXmap, MK8DXTotalMap, MK8DXbooster, nbMK8DXbooster, MK8DXmap , nbMK8DXmap
from settings import get_language
from datetime import datetime
from text import speedPath, urlImgCadoizzob, nofile

nbPlayerDisplayedStats = 50
nbPlayerDisplayedMap =  20

# Bad fonction to get author nickname or name
def checkname(nick , name):
    if nick == None :
        return name
    else :
        return nick

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

# False to get the map pool
# True to get the number of race
def statsOption(option, nbmapPoolorNot) :
    mapPoolLength = 0
    mapPool = None
    if (option == "b" or option == "timeb") :
        mapPoolLength = nbMK8DXbooster
        mapPool = MK8DXbooster
    elif option == "total" or option == "totalTime":
        mapPoolLength = nbMK8DXmap + nbMK8DXbooster 
        mapPool = MK8DXTotalMap
    else :
        mapPoolLength = nbMK8DXmap
        mapPool = MK8DXmap
    
    if ( nbmapPoolorNot):
        return mapPoolLength
    else :
        return mapPool

# 3 functions to find a player in the ctx . 
# Find idPLayer in mapmk8 and idPLayer and his place in maps
# return namePlayer to get the name if your are looking for someone
def findInMap(guild_id ,idPlayer, namePlayer, mapmk8, maps, shroom):
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+str(guild_id)+"/"+ shroom + mapmk8)  
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
    
async def drawFind(channel , maps, playerName, shroom):
    title = "Player : {0}".format(playerName)
    title += titleType(shroom)
    description = ""
    for (mapmk8, place ,time, i) in maps:
        description += "{0} : **{1}/{2}** -> {3}\n".format(mapmk8, place , i, time)
    if description == "" :
        await channel.send ("Pas de temps pour {0}".format(playerName))
    else :
        embedMap = discord.Embed(title=title,description=description)
        embedMap.set_thumbnail(url = urlImgCadoizzob)
        await channel.send(embed = embedMap)

async def find(guild_id, channel, idPlayer, shroom, option):
    maps = list()
    playerName = ""
    mapPool = statsOption(option, False)
    for mapmk8 in mapPool :
        if mapmk8 != 'week' :
            playerName = findInMap(guild_id,idPlayer,playerName,mapmk8, maps, shroom)
    if playerName == "" :
        playerName = idPlayer
    await drawFind(channel, maps, playerName, shroom)

# 3 function to get the Stats of the ctx . 
# get stats of one maps
def MapStats(guild_id, option, mapmk8, playersStats, shroom):
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+str(guild_id)+"/"+shroom+mapmk8)  
    if data != nofile:
        mk.dataToMapmk(data)
        if ( option == "" or option == "b" or option == "total"):
            mk.addStats(playersStats)
        else :
            mk.addStatsTime(playersStats)

# Return total stats points at 10^-5 
# add nbplayer to the total for every map missing 
def fillPoint(total, mapPlayed, nbplayer, mapPoolLength):
    return round((total + (nbplayer*(mapPoolLength-mapPlayed)))/mapPoolLength, 5)

def addTime(playertime):
        (h , m ,s , ms) = playertime
        addtos = ms//1000
        newms = ms%1000
        rs = ((s+addtos)//60)
        news = (s+addtos)%60
        newh = ((m+rs)//60)
        newm = (h+m+rs)%60
        return ( newh, newm , news, newms)

def checkDrawStats(nbDraw, newPlayer, oldPlayer, nbPlayer, option, mapPoolLength):
    if( oldPlayer == None):
        return nbDraw, newPlayer
    if ( option == "" or option == "b" or option == "total"):
        if (fillPoint(newPlayer[1],newPlayer[2],nbPlayer, mapPoolLength) == fillPoint(oldPlayer[1],oldPlayer[2],nbPlayer, mapPoolLength)):
            return nbDraw +1, newPlayer
        else :
            return nbDraw, newPlayer
    else:
        (newh , newm , news, newms ) = addTime(newPlayer[1])
        (oldh , oldm , olds, oldms ) = addTime(oldPlayer[1])
        if ( newh == oldh and newm == oldm and news == olds and newms == oldms):
            return nbDraw +1, newPlayer
        else :
            return nbDraw, newPlayer

def optionTile(option):
    if ( option == "b" or option == "timeb"): 
        return "Booster "
    elif (option == "total" or option == "totalTime"):
        return "All Maps "
    else : 
        return ""
        
async def drawStats(channel, guild_name,option, playersStats, shroom , page):
    # sort by the average place
    nbPlayer = len(playersStats)
    mapPoolLength = statsOption(option, True)
    if (option == "" or option == "b" or option == "total"):
        sorted_playersStats = sorted(playersStats.values(), key=lambda value : fillPoint(value[1],value[2],nbPlayer, mapPoolLength), reverse= False)
        title = "Stats Average place {1}: {0}".format(guild_name, optionTile(option))
    else :
        newplayersStats = { k:v for k,v in playersStats.items() if v[2] == mapPoolLength }
        sorted_playersStats = sorted(newplayersStats.values(), key=lambda value : addTime(value[1]) , reverse = False)
        title = "Stats Total Time {1}: {0}".format(guild_name, optionTile(option))
    title += titleType(shroom)
    description = ""
    i= 1 # cpt for number of player draw
    nbDraw = 0 # cpt number of draw to have real placement
    oldPlayer = None
    for playerlist in sorted_playersStats:
        if (i == (page)*(nbPlayerDisplayedStats)+1): # draw nbPlayerDisplayedStats
            break
        if(i > (page-1)*nbPlayerDisplayedMap):
            if ( option == "" or option == "b" or option == "total"):
                nbDraw,oldPlayer = checkDrawStats(nbDraw, playerlist, oldPlayer, nbPlayer,option, mapPoolLength)
                description += "**{3}.{0}** : {1} ( {2}/{4} maps )\n".format(playerlist[0], fillPoint(playerlist[1],playerlist[2],nbPlayer, mapPoolLength) , playerlist[2], (i - nbDraw), mapPoolLength )
                i += 1
            else :
                nbDraw, oldPlayer = checkDrawStats(nbDraw, playerlist, oldPlayer, nbPlayer, option, mapPoolLength)
                (h , m , s, ms ) = addTime(playerlist[1])
                description += "**{}.{}** : {}:{:02d}:{:02d}.{:03d}\n".format((i-nbDraw),playerlist[0],h, m , s, ms)
                i+= 1
    if description == "" :
        await channel.send ("Pas de stats pour ce serveur.")
    else :
        embedMap = discord.Embed(title=title,description=description)
        embedMap.set_thumbnail(url = urlImgCadoizzob)
        embedMap.set_footer(text = str(page))
        message = await channel.send(embed = embedMap)
        await setEmoji(message,page , len(sorted_playersStats) )
    
async def Stats(guild_id, channel, guild_name, option, shroom):
    playersStats = dict()
    mapPool = statsOption(option, False)
    for mapmk8 in mapPool :
        if mapmk8 != 'week' :
            MapStats(guild_id, option, mapmk8, playersStats, shroom)
    await drawStats(channel, guild_name,option, playersStats, shroom, 1)

#Set on mapmk8 the objective time. 
# Two type of objective.
async def setMapmkObjective(guild_id, mapmk8, time, bonus, shroom) :
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+str(guild_id)+"/"+shroom+mapmk8)
    if data != nofile:
        mk.dataToMapmk(data)
    if bonus == '':
        mk.setObjective(time)
    else :
        mk.setBonusObjective(time)
    mk.writeFile(path+str(guild_id)+"/"+shroom+mapmk8)

async def deleteFile(guild_id,  channel, file, mapmk8):
    try :
        os.remove(file)
        await channel.send (ttTexts.get( get_language(guild_id)).get("mapFileSup").format(mapmk8))
    except :
        await channel.send(ttTexts.get( get_language(guild_id)).get("noMapFile"))

#Delete if from mapmk8
async def deleteTtplayerfromMap(guild_id , channel, mapmk8, id, shroom):
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+str(guild_id)+"/"+shroom+mapmk8)
    if data != nofile:
        mk.dataToMapmk(data)
        mk.deleteTtplayer(id)
        if len(mk._ttplayers) !=0 :
            mk.writeFile(path+str(guild_id)+"/"+shroom+mapmk8)
        else :
            await channel.send(ttTexts.get( get_language(guild_id)).get("noMorePlayer").format(mapmk8))
            await deleteFile(guild_id,  channel, path+str(guild_id)+"/"+shroom+mapmk8, mapmk8)

#Delete if from all maps
async def deleteTtplayerfromAll(guild_id , channel,  id, shroom):
    for mapmk8 in MK8DXTotalMap.keys() :
        await deleteTtplayerfromMap(guild_id, channel,  mapmk8, id, shroom)
    await channel.send(ttTexts.get( get_language(guild_id)).get("supPlayer").format(id))

#Add ctx.author time in mapmk8
async def addTimeInFile(guild_id, channel,  author_id, nick , name, mapmk8, time ,url,shroom, fromCopy):
    mk = mapmk.mapmk(mapmk8, '' , '') #create a object mapmk with the name of the map
    data = mk.getFileR(path+str(guild_id)+"/"+shroom+mapmk8) # get the data from file
    mk.dataToMapmk(data)
    name = checkname(nick, name)  # check if the person who does the command has a nick name
    newplayer = ttplayer.TtPlayer( author_id, #create new ttplayer
                name,
                time,
                url)
    mk.addplayer(newplayer)
    mk.writeFile(path+str(guild_id)+"/"+shroom+mapmk8)
    if (not fromCopy):
        message = ttTexts.get( get_language(guild_id)).get("addTimeMap").format(name, time , mapmk8)
        if ( url != "") :
            message += " : " + url
        await channel.send( message)

def checkDrawMapmk(nbDraw, newPlayer, oldPlayer):
    if( oldPlayer == None): # first turn on this so no draw possible
        return nbDraw, newPlayer
    if ( newPlayer.getPlayerTime() == oldPlayer.getPlayerTime()) :
        return nbDraw+1 , newPlayer
    else : 
        return nbDraw, newPlayer

async def drawMapmk(guild_id, channel ,  mapmk8, shroom, page):
    mk = mapmk.mapmk(mapmk8, '', '') #create a object mapmk with the name of the map
    data = mk.getFileR(path+str(guild_id)+"/"+shroom+mapmk8) # get the data from file
    if data == nofile:
        await channel.send(ttTexts.get( get_language(guild_id)).get("noFileMap"))
    else :
        mk.dataToMapmk(data)
        description=""
        if mk._objective != "" :
            description += "Objectif : **" + mk._objective + "**\n"
        if mk._bonusObjective != "":
            description  += "Objectif Bonus: **" + mk._bonusObjective + "**\n"
        description +='\n'
        i = 1
        nbDraw = 0
        oldPlayer = None
        for player in mk._ttplayers:
            if (i == (page)*(nbPlayerDisplayedMap+1)) : # draw nbPlayerDisplayedMap players
                break
            if(i >= (page-1)*nbPlayerDisplayedMap):
                nbDraw, oldPlayer = checkDrawMapmk(nbDraw,player, oldPlayer)
                description += player.stringMapmk(i-nbDraw)
            i= i+1
        title = MK8DXTotalMap.get(mapmk8)
        title += titleType(shroom)
        embedMap = discord.Embed(title=title,description=description)
        embedMap.set_thumbnail(url = urlImgCadoizzob)
        embedMap.set_footer(text = str(page))
        message = await channel.send(embed = embedMap)
        await setEmoji(message,page , len(mk._ttplayers))

#Look for ctx.author.id in mapmk8 in the guild fromServ
def getCopyInMap(author_id , fromServ, mapmk8, maps, shroom):
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+fromServ+"/"+ shroom + mapmk8)  
    if data != nofile:
        mk.dataToMapmk(data)
        for player in mk._ttplayers :
            if player.getPlayerId() == author_id :
                maps.append((mapmk8, player.getPlayerTime(), player.getPlayerUrl() ))
                break
        return maps
    return maps

#Copy ctx.author.id's time from fromServ
async def copy(author_id,fromServ, shroom, guild_id, channel ,  nick , name):
    maps = list()
    for mapmk8 in MK8DXTotalMap.keys() :
        if mapmk8 != 'week' :
            getCopyInMap(author_id, fromServ, mapmk8, maps, shroom)
    for (mapeuh, time, url) in maps :
        await addTimeInFile(guild_id, channel,  author_id, nick , name, mapeuh, time ,url ,shroom, True)
#Change


######## THE FOLLOW IS DISGUSTING #######
async def drawPlayerCommand(guild_id, channel,ListOfplayer, mapmk8, shroom):
    mk = mapmk.mapmk(mapmk8, '', '') #create a object mapmk with the name of the map
    data = mk.getFileR(path+str(guild_id)+"/"+shroom+mapmk8) # get the data from file
    if data == nofile:
        await channel.send(ttTexts.get( get_language(guild_id)).get("noFileMap"))
    else :
        mk.dataToMapmk(data)
        title = ListOfplayer.get("player")[0].getPlayerName() + " : " + MK8DXTotalMap.get(mapmk8)
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
        await channel.send(embed = embedMap)

# get the two around the player 
def findInMapBis(guild_id ,idPlayer, mapmk8, shroom):
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+str(guild_id)+"/"+ shroom + mapmk8)  
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


            

