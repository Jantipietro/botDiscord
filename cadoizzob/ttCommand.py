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

# Create the guild file
async def createCommand(ctx):
    if not ctx.message.author.guild_permissions.manage_messages :
        await ctx.send( ttTexts.get(get_language(ctx)).get("perm"))
    else :
        try :
            os.makedirs(path+str(ctx.guild.id)+"/"+shroomPath)
            os.makedirs(path+str(ctx.guild.id)+"/"+noShroomPath)
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
        #Delete all the file and the server name's file too
        elif len(args) == 1 :
            try :
                shutil.rmtree(path+str(ctx.guild.id))
                await ctx.send( ttTexts.get(get_language(ctx)).get("delete"))
            except :
                # normally never happens, don't think rmtree can fail but in case
                await ctx.send(ttTexts.get(get_language(ctx)).get("shutilFail"))
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
            await drawMapmk(ctx, args[0], shroom)
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
        elif timesample.match(args[1]):
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
async def statsCommand(ctx, shroom) :
    if verifGuild(ctx):
        await Stats(ctx,shroom)
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
    

