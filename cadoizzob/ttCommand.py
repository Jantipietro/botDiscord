import os
import shutil
from text import *
from ttfunction import *
from settings import get_language

# check if the guild file exist
def verifGuild(guild_id):
    if not os.path.exists(path+str(guild_id)) :
            return False
    return True

#Delete guild file 
# Require Manage_message
async def deleteGuildFile(guild_id , channel,settings, hasPermission):
    #Delete all the file and the server name's file too
    if not hasPermission:
        await channel.send( ttTexts.get(get_language(guild_id, settings)).get("perm"))
    else:
        try :
            shutil.rmtree(path+str(guild_id))
            await channel.send( ttTexts.get(get_language(guild_id, settings)).get("delete"))
        except :
            # normally never happens, don't think rmtree can fail but in case
            await channel.send(ttTexts.get(get_language(guild_id, settings)).get("shutilFail"))

# Create the guild file
#Require Manage_message 
async def createCommand(guild_id , channel,settings, hasPermission):
    if not hasPermission:
        await channel.send( ttTexts.get(get_language(guild_id, settings)).get("perm"))
    else :
        try :
            os.makedirs(path+str(guild_id)+"/"+shroomPath) #150cc
            os.makedirs(path+str(guild_id)+"/"+noShroomPath)
            os.makedirs(path+str(guild_id)+"/"+speedPath+shroomPath) # 200cc 
            os.makedirs(path+str(guild_id)+"/"+speedPath+noShroomPath) 
            await channel.send(ttTexts.get(get_language(guild_id, settings)).get("create"))
        except :
            await channel.send(ttTexts.get(get_language(guild_id, settings)).get("pathExist"))

#Find a player or himself
async def findCommand(guild_id, channel , settings ,author_id, args , shroom):
    if verifGuild(guild_id):
        if len(args) == 1 :
            await find(guild_id, channel, author_id, shroom, "")
        elif len(args) == 2 :
            #Check if this looks like an ID ( can be better)
            if idsample.match(args[1]):
                await find(guild_id, channel, args[1], shroom, "total")
            elif args[1] == "b" or args[1] == "booster":
                await find(guild_id, channel , author_id, shroom , "b")
            elif args[1] == "total":
                await find(guild_id, channel , author_id, shroom , "total")
            else :
                await channel.send(ttTexts.get(get_language(guild_id, settings)).get("wrongID").format(args[1]))
        else :
            await channel.send(ttTexts.get(get_language(guild_id, settings)).get("tooMuchArg"))
    else :
        await channel.send(ttTexts.get(get_language(guild_id, settings)).get("noFile"))

#Delete command only usable by manage_messages perimissions
#Manage message Perm
async def deleteCommand(guild_id, channel, settings , args , shroom , hasPermission):
    if verifGuild(guild_id):
        if not hasPermission:
            await channel.send( ttTexts.get(get_language(guild_id, settings)).get("perm"))
        # Delete an id from all the file 
        elif len(args) == 2 :
            if idsample.match(args[1]):
                await deleteTtplayerfromAll(guild_id , channel, settings, args[1], shroom)
            # Delete a map file
            elif MK8DXTotalMap.get(args[1]) != None :
                await deleteFile(guild_id, settings ,channel , path+str(guild_id)+"/"+shroom +args[1] , args[1])
            else :
                await channel.send(ttTexts.get(get_language(guild_id, settings)).get("wrongID").format(args[1]))
        else :
            await channel.send(ttTexts.get(get_language(guild_id, settings)).get("tooMuchArg"))
    else :
        await channel.send( ttTexts.get(get_language(guild_id, settings)).get("noFile"))

#HasPermission -> check perm : manage_message 
async def mapmkCommand( guild_id, channel , settings , args , shroom, hasPermission, author_id, nick, name):
    if verifGuild(guild_id):
        # draw a file mapMK
        if len(args)== 1 :
            await drawMapmk(guild_id, channel , settings , args[0], shroom, 1)
        # Add objectif 
        elif args[1] == 'objective' or args[1] == 'bonus' :
            if not hasPermission:
                await channel.send( ttTexts.get(get_language(guild_id, settings)).get("perm"))
            elif len(args) == 3 :
                if timesample.match(args[2]):
                    if args[1] == 'objective' :
                        await setMapmkObjective(guild_id, args[0], args[2], '', shroom)
                        await channel.send(ttTexts.get(get_language(guild_id, settings)).get("objAdd"))
                    else :
                        await setMapmkObjective(guild_id, args[0], args[2], 'bonus', shroom)
                        await channel.send(ttTexts.get(get_language(guild_id, settings)).get("objBAdd"))
                # put objectif at null
                elif args[2] == 'delete':
                    if args[1] == 'objective' :
                        await setMapmkObjective(guild_id, args[0], '', '', shroom)
                        await channel.send(ttTexts.get(get_language(guild_id, settings)).get("objSup"))
                    else :
                        await setMapmkObjective(guild_id, args[0], '', 'bonus', shroom)
                        await channel.send(ttTexts.get(get_language(guild_id, settings)).get("objBSup"))
                else :
                    await channel.send(ttTexts.get(get_language(guild_id, settings)).get("badFormat"))
            else:
                await channel.send (ttTexts.get(get_language(guild_id, settings)).get("tooMuchArg"))
        # Delete time into the file
        elif args[1]== 'delete':
            if len(args)== 2 :
                await deleteTtplayerfromMap(guild_id, channel, settings, args[0], author_id, shroom)
                await channel.send(ttTexts.get(get_language(guild_id, settings)).get("timeSup"))
            # To delete one player from a file
            elif len(args)==3:
                if not hasPermission:
                    await channel.send( ttTexts.get(get_language(guild_id, settings)).get("perm"))
                elif idsample.match(args[2]):
                    await deleteTtplayerfromMap(guild_id, channel, settings, args[0], args[2], shroom)
                    await channel.send(ttTexts.get(get_language(guild_id, settings)).get("hisTimeSup").format(args[2]))
                else :
                    await channel.send(ttTexts.get(get_language(guild_id, settings)).get("wrongID").format(args[1]))
        # add a player in file with a link or not.
        elif timesample.match(args[1]) :
            if ( len(args) == 2): # url empty
                await addTimeInFile(guild_id, channel, settings, author_id, nick, name ,args[0], args[1],"", shroom, False)
            elif (len(args) == 3) :
                if ( urlsample.match(args[2])):
                    await addTimeInFile(guild_id, channel, settings, author_id, nick , name, args[0], args[1],args[2], shroom, False)
                else :
                    await channel.send (ttTexts.get(get_language(guild_id, settings)).get("badUrl"))
            else :
                await channel.send (ttTexts.get(get_language(guild_id, settings)).get("tooMuchArg"))
        else : 
            # Bad timing format
            await channel.send( ttTexts.get(get_language(guild_id, settings)).get("badFormat"))
    else :
        #No server file 
        await channel.send( ttTexts.get(get_language(guild_id, settings)).get("noFile"))

#Command to add many maps and only 
async def addListCommand(guild_id , channel, settings, args, shroom,  hasPermission, author_id, nick , name):
    if verifGuild(guild_id):
        # Help command inside 
        if ( args == 'help'):
            await channel.send(ttTexts.get(get_language(guild_id, settings)).get("allMap"))
            await channel.send(ttTexts.get(get_language(guild_id, settings)).get("boosterMap"))
            await channel.send(ttTexts.get(get_language(guild_id, settings)).get("helpAllMap"))
        else :
            #Get away with space and \n in the string
            SeparateCouple = args.replace(" ","").replace("\n","").split(";")
            Allcouple = []
            # get the couple map time in the string
            for couple in SeparateCouple :
                Allcouple.append(couple.split(","))
            # add every couple with the map command 
            for args in Allcouple :
                if MK8DXTotalMap.get(args[0]) != None:
                    await mapmkCommand( guild_id, channel , settings , args , shroom, hasPermission, author_id, nick , name)
                else :
                    await channel.send(ttTexts.get(get_language(guild_id, settings)).get("wrongName"))
    else :
        await channel.send( ttTexts.get(get_language(guild_id, settings)).get("noFile"))

# get the Stats of a guild 
async def statsCommand(guild_id, channel , guild_name, args , shroom) :
    if verifGuild(guild_id):
        if len(args) == 1:
            await Stats(guild_id, channel , guild_name , "" ,shroom)
        # Total time stats
        elif args[1] == "time":
            if len(args) == 2 :
                await Stats(guild_id, channel , guild_name , "time" ,shroom)
            elif len(args) == 3 :
                if args[2] == "booster" or args[2] == "b":
                    await Stats(guild_id, channel , guild_name , "timeb", shroom)
                elif args[2] == "total" :
                    await Stats(guild_id, channel , guild_name , "totalTime", shroom)
                else :
                    await channel.send(ttTexts.get(get_language(guild_id, settings)).get("unknowCmd"))
            else :
                await channel.send(ttTexts.get(get_language(guild_id, settings)).get("tooMuchArg"))
        elif args[1] == "booster" or args[1] == "b":
            await Stats(guild_id, channel , guild_name , "b" , shroom)
        elif args[1] == "total" :
            await Stats(guild_id, channel , guild_name , "total" , shroom)
        else :
            await channel.send(ttTexts.get(get_language(guild_id, settings)).get("tooMuchArg"))
    else :
        await channel.send( ttTexts.get(get_language(guild_id, settings)).get("noFile"))

#Copy the context id from a serv into the context guild.
async def copyCommand(guild_id , author_id, fromServ,shroom, channel, settings , nick , name):
    if verifGuild(guild_id):
        if not os.path.exists(path+fromServ):
            await channel.send(ttTexts.get(get_language(guild_id, settings)).get("wrongServ"))
        else :
            await copy(author_id, fromServ,shroom, guild_id, channel, settings , nick , name)
            await channel.send(ttTexts.get(get_language(guild_id, settings)).get("copy"))
    else :
        await channel.send( ttTexts.get(get_language(guild_id, settings)).get("noFile"))

# Command with player ID 
async def playerCommand(guild_id, channel,settings, args, shroom):
    if verifGuild(guild_id):
        if len(args) == 2 :
            if MK8DXTotalMap.get(args[0])!= None:
                ListOfPlayer = findInMapBis(guild_id, args[0], args[1], shroom)
                if ListOfPlayer.get("player") != None :
                    await drawPlayerCommand(guild_id, channel, ListOfPlayer, args[1], shroom)
                else :
                    await channel.send(ttTexts.get(get_language(guild_id, settings)).get("notFind"))
            else :
                await channel.send(ttTexts.get(get_language(guild_id, settings)).get("noFileMap"))#wrong map
        else :
            await channel.send(ttTexts.get(get_language(guild_id, settings)).get("tooMuchArg")) #too much arg
    else :
        await channel.send( ttTexts.get(get_language(guild_id, settings)).get("noFile"))

async def ttCommandGestion(interaction, settings, categorie, args, speedPath):
    if ( categorie != None):
    # get the good path's File
        if categorie == 'ni' : 
            strPath = speedPath + noShroomPath
        else :
            strPath = speedPath + shroomPath
        # Shroom section 
        # Copy your time from the serv args[1]
        if args[0] == 'copy':
            await copyCommand(interaction.guild_id, interaction.user.id, args[1], strPath, interaction.channel, settings, interaction.user.nick, interaction.user.name)
        # Add a list of maps 
        elif args[0] == 'addlist':
            await addListCommand(interaction.guild_id, interaction.channel, settings, args[1], strPath,interaction.user.guild_permissions.manage_messages, interaction.user.id ,  interaction.user.nick, interaction.user.name)
        # Stats section with all player in the section
        elif args[0] == 'stats':
            await statsCommand(interaction.guild_id, interaction.channel, interaction.guild.name,args, strPath)
        # Find command -> 
        elif args[0] == 'find' :
            await findCommand(interaction.guild_id, interaction.channel, settings, interaction.user.id, args , strPath)
        # Delete all file from the server that call this.
        elif args[0] == 'delete':
            await deleteCommand(interaction.guild_id , interaction.channel,settings, args , strPath,interaction.user.guild_permissions.manage_messages)
        # Check if the first arg is a map name
        elif MK8DXTotalMap.get(args[0])!= None:
            await mapmkCommand( interaction.guild_id, interaction.channel , settings , args , strPath, interaction.user.guild_permissions.manage_messages, interaction.user.id, interaction.user.nick, interaction.user.name)
        elif idsample.match(args[0]) :
            await playerCommand(interaction.guild_id, interaction.channel, settings, args , strPath)
        else :
            await interaction.channel.send(ttTexts.get(get_language(interaction.guild_id, settings)).get("noArg"))
    else :
        await interaction.channel.send("Missing 'categorie' in the command line")

    
