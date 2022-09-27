import json
from datetime import datetime

def opensettings():
    with open("cadoizzob/settings.json", "r") as f :
        settings = json.load(f)
        f.close()
    return settings

def writesettings(settings):
    with open("cadoizzob/settings.json", "w") as f :
        json.dump(settings,f, default = str)
        f.close()

def basicsettings(settings, guild):
    Dict = {
        str(guild) : { "language" : "en", "teams" : [], "last_use" : datetime.now()}
    }
    settings.update(Dict)
    writesettings(settings)

# on guild join / and after for the older one
def createguildsets(guild):
    settings = opensettings()
    basicsettings(settings, guild)

# # For the prefix of the bot 
# def get_prefix_cmd(client,message):
#     settings = opensettings()
#     # To create settings for server where the bot already in 
#     if settings.get(str(message.guild.id)) == None:
#         createguildsets(str(message.guild.id))
#         settings = opensettings() # get new settings 
#     prefix = settings.get(str(message.guild.k,,,,,,,,,,xwŝmpsdqqqqqqqqqqqqqqqqqid)).get("prefix")
#     return (prefix, str.upper(prefix))

def get_language(guildID):
    settings = opensettings()
    return settings.get(str(guildID)).get("language")

###########################################""

def get_teams(guild):
    settings = opensettings()
    if not "teams" in settings.get(guild) :
        settings.get(guild).update({"teams" : []})
        writesettings(settings)
        return []
    return settings.get(guild).get("teams")

def set_team(guild, team):
    settings = opensettings()
    if settings.get(guild) != None :
        if not "teams" in settings.get(guild) :
            settings.get(guild).update({"teams" : []})
        settings[guild]["teams"].append(team)
        writesettings(settings)

def del_team(guild, teamToDel):
    settings = opensettings()
    if settings.get(guild) != None :
        if not "teams" in settings.get(guild) :
            settings.get(guild).update({"teams" : []})
            writesettings(settings)
            return 0 # create the param
        try :
            settings.get(guild).get("teams").remove(teamToDel)
            writesettings(settings)
            return 1 # delete item well
        except:
            return 0 # no

def guildvarchange(var, guild, value):
    settings = opensettings()
    if settings.get(guild) != None :
        settings[guild][var]= value
        writesettings(settings)





