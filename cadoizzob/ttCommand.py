import os
import shutil
from text import *
from ttfunction import *
from settings import get_language, get_prefix

# check if the guild file exist
def verifGuild(ctx):
    # now guild file are by guild.id
    if not os.path.exists(path+str(ctx.guild.id)) :
        try :
            # Before that was by name so the change here
            os.rename(path+str(ctx.guild),path+str(ctx.guild.id))
        except :
            return False
    return True

#Delete guild file 
async def deleteGuildFile(ctx):
    #Delete all the file and the server name's file too
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.send( ttTexts.get(get_language(ctx)).get("perm"))
    else:
        try :
            shutil.rmtree(path+str(ctx.guild.id))
            await ctx.send( ttTexts.get(get_language(ctx)).get("delete"))
        except :
            # normally never happens, don't think rmtree can fail but in case
            await ctx.send(ttTexts.get(get_language(ctx)).get("shutilFail"))

# Create the guild file
async def createCommand(ctx):
    if not ctx.message.author.guild_permissions.manage_messages :
        await ctx.send( ttTexts.get(get_language(ctx)).get("perm"))
    else :
        try :
            os.makedirs(path+str(ctx.guild.id)+"/"+shroomPath) #150cc
            os.makedirs(path+str(ctx.guild.id)+"/"+noShroomPath)
            os.makedirs(path+str(ctx.guild.id)+"/"+speedPath+shroomPath) # 200cc 
            os.makedirs(path+str(ctx.guild.id)+"/"+speedPath+noShroomPath) 
            await ctx.send(ttTexts.get(get_language(ctx)).get("create"))
        except :
            await ctx.send(ttTexts.get(get_language(ctx)).get("pathExist").format(get_prefix(ctx)))

#Find a player or himself
async def findCommand(ctx , args , shroom):
    if verifGuild(ctx):
        if len(args) == 1 :
            await find(ctx, ctx.author.id, shroom)
        elif len(args) == 2 :
            #Check if this looks like an ID ( can be better)
            if idsample.match(args[1]):
                await find(ctx, args[1], shroom)
            else :
                await ctx.send(ttTexts.get(get_language(ctx)).get("wrongID").format(args[1]))
        else :
            await ctx.send(ttTexts.get(get_language(ctx)).get("tooMuchArg").format(get_prefix(ctx)))
    else :
        await ctx.send(ttTexts.get(get_language(ctx)).get("noFile").format(get_prefix(ctx)))

#Delete command only usable by manage_messages perimissions
async def deleteCommand(ctx , args , shroom ):
    if verifGuild(ctx):
        if not ctx.message.author.guild_permissions.manage_messages:
            await ctx.send( ttTexts.get(get_language(ctx)).get("perm"))
        # Delete an id from all the file 
        elif len(args) == 2 :
            if idsample.match(args[1]):
                await deleteTtplayerfromAll(ctx, args[1], shroom)
            # Delete a map file
            elif mapmk.MK8DXmap.get(args[1]) != None :
                await deleteFile(ctx , path+str(ctx.guild.id)+"/"+shroom +args[1] , args[1])
            else :
                await ctx.send(ttTexts.get(get_language(ctx)).get("wrongID").format(args[1]))
        else :
            await ctx.send(ttTexts.get(get_language(ctx)).get("tooMuchArg").format(get_prefix(ctx)))
    else :
        await ctx.send( ttTexts.get(get_language(ctx)).get("noFile").format(get_prefix(ctx)))

async def mapmkCommand( ctx , args , shroom):
    if verifGuild(ctx):
        # draw a file mapMK
        if len(args)== 1 :
            await drawMapmk(ctx, args[0], shroom, 1)
        # Add objectif 
        elif args[1] == 'objective' or args[1] == 'bonus' :
            if not ctx.message.author.guild_permissions.manage_messages:
                await ctx.send( ttTexts.get(get_language(ctx)).get("perm"))
            elif len(args) == 3 :
                if timesample.match(args[2]):
                    if args[1] == 'objective' :
                        await setMapmkObjective(ctx, args[0], args[2], '', shroom)
                        await ctx.send(ttTexts.get(get_language(ctx)).get("objAdd"))
                    else :
                        await setMapmkObjective(ctx, args[0], args[2], 'bonus', shroom)
                        await ctx.send(ttTexts.get(get_language(ctx)).get("objBAdd"))
                # put objectif at null
                elif args[2] == 'delete':
                    if args[1] == 'objective' :
                        await setMapmkObjective(ctx, args[0], '', '', shroom)
                        await ctx.send(ttTexts.get(get_language(ctx)).get("objSup"))
                    else :
                        await setMapmkObjective(ctx, args[0], '', 'bonus', shroom)
                        await ctx.send(ttTexts.get(get_language(ctx)).get("objBSup"))
                else :
                    await ctx.send(ttTexts.get(get_language(ctx)).get("badFormat"))
            else:
                await ctx.send (ttTexts.get(get_language(ctx)).get("tooMuchArg").format(get_prefix(ctx)))
        # Delete time into the file
        elif args[1]== 'delete':
            if len(args)== 2 :
                await deleteTtplayerfromMap(ctx,args[0], ctx.message.author.id, shroom)
                await ctx.send(ttTexts.get(get_language(ctx)).get("timeSup"))
            # To delete one player from a file
            elif len(args)==3:
                if not ctx.message.author.guild_permissions.manage_messages:
                    await ctx.send( ttTexts.get(get_language(ctx)).get("perm"))
                elif idsample.match(args[2]):
                    await deleteTtplayerfromMap(ctx,args[0], args[2], shroom)
                    await ctx.send(ttTexts.get(get_language(ctx)).get("hisTimeSup").format(args[2]))
                else :
                    await ctx.send(ttTexts.get(get_language(ctx)).get("wrongID").format(args[1]))
        # add a player in file
        elif timesample.match(args[1]) :
            await addTimeInFile(ctx, args[0], args[1], shroom)
        else : 
            # Bad timing format
            await ctx.send( ttTexts.get(get_language(ctx)).get("badFormat"))
    else :
        #No server file 
        await ctx.send( ttTexts.get(get_language(ctx)).get("noFile").format(get_prefix(ctx)))

#Command to add many maps and only 
async def addListCommand(ctx, args, shroom):
    if verifGuild(ctx):
        # Help command inside 
        if ( args == 'help'):
            await ctx.send(ttTexts.get(get_language(ctx)).get("allMap").format(get_prefix(ctx)))
            await ctx.send(ttTexts.get(get_language(ctx)).get("helpAllMap").format(get_prefix(ctx)))
        else :
            #Get away with space and \n in the string
            SeparateCouple = args.replace(" ","").replace("\n","").split(";")
            Allcouple = []
            # get the couple map time in the string
            for couple in SeparateCouple :
                Allcouple.append(couple.split(","))
            # add every couple with the map command 
            for args in Allcouple :
                if mapmk.MK8DXmap.get(args[0]) != None:
                    await mapmkCommand(ctx, args, shroom )
                else :
                    await ctx.send(ttTexts.get(get_language(ctx)).get("wrongName").format(get_prefix(ctx)))
    else :
        await ctx.send( ttTexts.get(get_language(ctx)).get("noFile").format(get_prefix(ctx)))

# get the Stats of a guild 
async def statsCommand(ctx , args , shroom) :
    if verifGuild(ctx):
        if len(args) == 1:
            await Stats(ctx, "" ,shroom)
        elif args[1] == "time":
            await Stats(ctx, "time" ,shroom)
        else :
            await ctx.send(ttTexts.get(get_language(ctx)).get("tooMuchArg").format(get_prefix(ctx)))
    else :
        await ctx.send( ttTexts.get(get_language(ctx)).get("noFile").format(get_prefix(ctx)))

#Copy the context id from a serv into the context guild.
async def copyCommand(ctx, fromServ,shroom):
    if verifGuild(ctx):
        if not os.path.exists(path+fromServ):
            await ctx.send(ttTexts.get(get_language(ctx)).get("wrongServ").format(get_prefix(ctx)))
        else :
            await copy(ctx, fromServ,shroom)
            await ctx.send(ttTexts.get(get_language(ctx)).get("copy"))
    else :
        await ctx.send( ttTexts.get(get_language(ctx)).get("noFile").format(get_prefix(ctx)))

# Command with player ID 
async def playerCommand(ctx, args, shroom):
    if verifGuild(ctx):
        if len(args) == 2 :
            if MK8DXmap.get(args[1]) != None :
                ListOfPlayer = findInMapBis(ctx, args[0], args[1], shroom)
                if ListOfPlayer.get("player") != None :
                    await drawPlayerCommand(ctx, ListOfPlayer, args[1], shroom)
                else :
                    await ctx.send(ttTexts.get(get_language(ctx)).get("notFind"))
            else :
                await ctx.send(ttTexts.get(get_language(ctx)).get("noFileMap"))#wrong map
        else :
            await ctx.send(ttTexts.get(get_language(ctx)).get("tooMuchArg").format(get_prefix(ctx))) #too much arg
    else :
        await ctx.send( ttTexts.get(get_language(ctx)).get("noFile").format(get_prefix(ctx)))

async def ttCommandGestion(ctx,args, speedPath):
    # Shroom section 
    # Copy your time from the serv args[1]
    if args[0] == 'copy':
        await copyCommand(ctx, args[1], speedPath+shroomPath)
    # Add a list of maps 
    elif args[0] == 'addlist':
        await addListCommand(ctx, args[1], speedPath+shroomPath)
    # Draw png with all maps nickname that it use
    elif args[0] == 'maps' :
        await ctx.send("https://media.discordapp.net/attachments/579573532263055381/583008091541471234/abveration.png?width=1202&height=510")
    # Stats section with all player in the section
    elif args[0] == 'stats':
        await statsCommand(ctx,args, speedPath+shroomPath)
    # Find command -> 
    elif args[0] == 'find' :
        await findCommand(ctx, args , speedPath+shroomPath)
    #Create files with the server name
    elif args[0] == 'create':
        await createCommand(ctx)
    # Delete all file from the server that call this.
    elif args[0] == 'delete':
        await deleteCommand(ctx, args , speedPath+shroomPath)
    # Check if the first arg is a map name
    elif MK8DXmap.get(args[0]) != None :
        await mapmkCommand(ctx, args , speedPath+shroomPath)
    elif idsample.match(args[0]) :
        await playerCommand(ctx, args , speedPath+shroomPath)
    # Noshroom way ^^
    elif args[0] == 'ni' :
        del args[0] # to call the other function , delete the arg "ni"
        if args[0] == 'stats':
            await statsCommand(ctx,args, speedPath+noShroomPath)
        # Copy your time from the serv args[1]
        elif args[0] == 'copy':
            await copyCommand(ctx, args[1], speedPath+noShroomPath)
        # Add many maps
        elif args[0] == 'addlist':
            await addListCommand(ctx, args[1], speedPath+noShroomPath)
        #Seek player
        elif args[0] == 'find' :
            await findCommand(ctx, args , speedPath+noShroomPath)
        # Delete all file from the server that call this.
        elif args[0] == 'delete':
            await deleteCommand(ctx, args , speedPath+noShroomPath)
        # Check if the first arg is a map name
        elif MK8DXmap.get(args[0]) != None :
            await mapmkCommand(ctx, args , speedPath+noShroomPath)
        elif idsample.match(args[0]) :
            await playerCommand(ctx, args , speedPath+noShroomPath)
        else :
            await ctx.send(ttTexts.get(get_language(ctx)).get("unknowCmd").format(get_prefix(ctx)))
    else :
        await ctx.send(ttTexts.get(get_language(ctx)).get("noArg").format(get_prefix(ctx)))

    
