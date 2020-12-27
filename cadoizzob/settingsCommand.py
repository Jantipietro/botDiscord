from text import *
from settings import get_language, get_prefix, set_team, del_team


# put arg in the good format to get rid of 
def lowerArgSets (args):
    lowerarg=[]
    for arg in args:
        # to use tag instead of finding the user id 
        if rolesample.match(arg):
            newarg = arg.strip('<@&>')
            lowerarg.append(str.lower(newarg))
        else :
            lowerarg.append(str.lower(arg))
    return lowerarg

async def teamsCommand(ctx,args):
    if args[1] == "add" :
        # get strip of role mark so it's juste like an ID now
        if idsample.match(args[2]):
            set_team(str(ctx.guild.id), args[2])
            await ctx.send("team add")
    elif args[1] == "del":
        # get strip of role mark so it's juste like an ID now
        if idsample.match(args[2]):
            if del_team(str(ctx.guild.id), args[2]) == 1:
                await ctx.send("team del")
            else :
                await ctx.send("no team del")
    else :
        await ctx.send("wrong arg")
        # wrong argument

