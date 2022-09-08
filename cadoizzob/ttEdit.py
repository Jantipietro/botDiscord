import re
import mapmk
import discord
from text import path,urlImgCadoizzob, nofile, MK8DXmap, shroomPath, speedPath, noShroomPath, MK8DXTotalMap
from ttfunction import nbPlayerDisplayedMap, nbPlayerDisplayedStats, setEmoji, titleType, fillPoint, addTime, optionTile , statsOption

async def editDrawMapmk(guildID ,message, mapmk8, shroom, page):
    mk = mapmk.mapmk(mapmk8, '', '') #create a object mapmk with the name of the map
    data = mk.getFileR(path+str(guildID)+"/"+shroom+mapmk8) # get the data from file
    mk.dataToMapmk(data)
    description=""
    if mk._objective != "" :
        description += "Objectif : **" + mk._objective + "**\n"
    if mk._bonusObjective != "":
        description  += "Objectif Bonus: **" + mk._bonusObjective + "**\n"
    description +='\n'
    i = 1
    for player in mk._ttplayers:
        if (i == (page)*(nbPlayerDisplayedMap)+1) : # draw nbPlayerDisplayedMap players
            break
        if(i > (page-1)*nbPlayerDisplayedMap):
            description += player.stringMapmk(i)
        i= i+1
    title = message.embeds[0].title
    embedMap = discord.Embed(title=title,description=description)
    embedMap.set_thumbnail(url = urlImgCadoizzob)
    embedMap.set_footer(text = str(page))
    await message.edit(embed = embedMap)
    await setEmoji(message,page , len(mk._ttplayers))


# 3 function to get the Stats. 
# get stats of one maps
def MapStats(guildName, guildID, message, option, mapmk8, playersStats, shroom):
    mk = mapmk.mapmk(mapmk8, '' ,'')
    data = mk.getFileR(path+str(guildID)+"/"+shroom+mapmk8)  
    if data != nofile:
        mk.dataToMapmk(data)
        if ( option == ""  or option == "b" or option == "total"):
            mk.addStats(playersStats)
        else :
            mk.addStatsTime(playersStats)

async def drawStats(guildName, guildID, message,option, playersStats, shroom , page):
    # sort by the average place
    nbPlayer = len(playersStats)
    mapPoolLength = statsOption(option, True)
    if (option == ""  or option == "b" or option == "total"):
        sorted_playersStats = sorted(playersStats.values(), key=lambda value : fillPoint(value[1],value[2],nbPlayer, mapPoolLength), reverse= False)
        title = "Stats Average place {1}: {0}".format(guildName, optionTile(option))
    else :
        newplayersStats = { k:v for k,v in playersStats.items() if v[2] == mapPoolLength } 
        sorted_playersStats = sorted(newplayersStats.values(), key=lambda value : addTime(value[1]) , reverse = False)
        title = "Stats Total Time {1}: {0}".format(guildName, optionTile(option))
    title += titleType(shroom)
    description = ""
    i= 1
    for playerlist in sorted_playersStats:
        if (i == (page)*(nbPlayerDisplayedStats)+1) :  # draw nbPlayerDisplayedStats players
            break
        if(i > (page-1)*nbPlayerDisplayedStats):
            if ( option == "" or option == "b" or option == "total"):
                description += "**{3}.{0}** : {1} ( {2}/{4} maps )\n".format(playerlist[0], fillPoint(playerlist[1],playerlist[2],nbPlayer, mapPoolLength) , playerlist[2], i, mapPoolLength)
            else :
                (h , m , s, ms ) = addTime(playerlist[1])
                description += "**{}.{}** : {}:{:02d}:{:02d}.{:03d}\n".format(i,playerlist[0],h, m , s, ms, )
        i += 1
    embedMap = discord.Embed(title=title,description=description)
    embedMap.set_thumbnail(url = urlImgCadoizzob)
    embedMap.set_footer(text = str(page))
    await message.edit(embed = embedMap)
    await setEmoji(message,page , len(sorted_playersStats))
    
async def editStats(guildName, guildID, message, option, shroom,page):
    playersStats = dict()
    mapPool = statsOption(option, False)
    for mapmk8 in mapPool:
        if mapmk8 != 'week' :
            MapStats(guildName, guildID, message, option, mapmk8, playersStats, shroom)
    await drawStats(guildName, guildID, message,option, playersStats, shroom, page)

##### COmmand edit ######
# Create the shroomPath from a list with/withou "Shroomless" and/or "200cc"
def createShroomPath(pathList):
    path = ""
    if ( "200cc" in pathList) :
        path+= speedPath
    if( "Shroomless" in pathList):
        path += noShroomPath
    else :
        path += shroomPath
    return path

# Find a map in MKD8DX map.
def findMap(mapmk):
    for key,map in MK8DXTotalMap.items():
        if map == mapmk :
            return key

async def ModifyEmbed(reaction):
    page = int(reaction.message.embeds[0].footer.text)
    if reaction.emoji == "➡️" : # add page if arro_right 
        page += 1
    else :
        page -= 1
    for reac in  reaction.message.reactions: # clear all reac
        await reac.clear()
    s = reaction.message.embeds[0].title
    pathList = re.findall("Shroomless|200cc",s)
    if ( s.startswith("Stats")): # Change STats embed.
        if(s.find("Total Time") == -1):
            if ( s.find("Booster", 15) != -1 ):
                await editStats(reaction.message.guild, reaction.message.guild.id, reaction.message, "b", createShroomPath(pathList),page)
            elif ( s.find("All Maps", 15) != -1 ):
                await editStats(reaction.message.guild, reaction.message.guild.id, reaction.message, "total", createShroomPath(pathList),page)
            else :
                await editStats(reaction.message.guild, reaction.message.guild.id, reaction.message, "", createShroomPath(pathList),page)
        else :
            # Time stats edit
            if ( s.find("Booster", 15) != -1 ):
                await editStats(reaction.message.guild, reaction.message.guild.id, reaction.message, "timeb", createShroomPath(pathList),page)
            elif ( s.find("All Maps", 15) != -1 ):
                await editStats(reaction.message.guild, reaction.message.guild.id, reaction.message, "totalTime", createShroomPath(pathList),page)
            else : 
                await editStats(reaction.message.guild, reaction.message.guild.id, reaction.message, "time", createShroomPath(pathList),page)
    else :
        # Change mapMK
        if (not pathList): # is empty
            await editDrawMapmk(reaction.message.guild.id ,reaction.message, findMap(s), createShroomPath(pathList), page)
        else :
            for x in pathList : # parse to get only the map name
                s = s.replace(x,"")
            s = s.rstrip()
            await editDrawMapmk(reaction.message.guild.id ,reaction.message, findMap(s), createShroomPath(pathList), page)