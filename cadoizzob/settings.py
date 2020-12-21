import json

def opensettings():
    with open("cadoizzob/settings.json", "r") as f :
        settings = json.load(f)
        f.close()
    return settings

def writesettings(settings):
    with open("cadoizzob/settings.json", "w") as f :
        json.dump(settings,f)
        f.close()

def basicsettings(settings, guild):
    Dict = {
        str(guild) : { "language" : "EN" , "prefix" : "c!"}
    }
    settings.update(Dict)

def createguildsets(guild):
    settings = opensettings()
    basicsettings(settings, guild)
    writesettings(settings)

def get_prefix_cmd(client,message):
    settings = opensettings()
    # To create settings for server where the bot already in 
    if settings.get(str(message.guild.id)) == None:
        createguildsets(str(message.guild.id))
        settings = opensettings() # get new settings 
    return settings.get(str(message.guild.id)).get("prefix")

def get_prefix(ctx):
    settings = opensettings()
    return settings.get(str(ctx.guild.id)).get("prefix")

def get_language(ctx):
    settings = opensettings()
    return settings.get(str(ctx.guild.id)).get("language")

def guildvarchange(var, guild, value):
    settings = opensettings()
    if settings.get(guild) != None :
        settings[guild][var]= value
        writesettings(settings)
    else :
        return 0 # loose


