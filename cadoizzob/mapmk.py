import ttplayer
import json
import discord

MK8DXmap = { "mks" : "Mario Kart Stadium" , 'wp' :"Water Park" , 'ssc' : "Sweet Sweet Canyon" , 'tr' :"Thwomp Ruins" ,     # coupe Champignon
                'mc' : "Mario Circuit" , 'th' : "Toad Harbor" , 'tm' : "Twisted Mansion" , 'sgf' : "Shy Guy Falls",# coupe Fleur
                'sa' :"Sunshine Airport"  , 'ds' : "Dolphin Shoals"  , 'ed' : "Electrodrome" , 'mw' : "Mount Wario"  ,#coupe Etoile
                'cc' : "Cloudtop Cruise" , 'bdd' : 'Bone-Dry Dunes' , 'bc' : "Bowser's Castle" , 'rr' :"Rainbow Road"  ,# coupe Spéciale
                'dyc' :"Yoshi Circuit" , 'dea' :"Excitbike Arena" , 'ddd' :"Dragon Driftway" , 'dmc' :"Mute City" ,# coupe Oeuf
                'dwgm' :"Wario's Gold Mine", 'drr' :"Rainbow Road SNES" , 'diio' :"Ice Ice OutPost", 'dhc' : "Hyrule Circuit" ,#coupe Hyrule
                'rmmm' :"Moo Moo Meadows", 'rmc' : "Mario Circuit GBA" , 'rccb' :"Cheep Cheep Beach", 'rtt' :"Toad's Turnpike" ,#coupe Carapace
                'rddd' : "Dry Dry Desert", 'rdp3' : "Donut Plains 3", 'rrry' :"Royal Raceway", 'rdkj' : 'DK Jungle',# coupe Banane
                'rws' : "Wario Stadium", 'rsl' : "Sherbet Land" ,'rmp' : 'Music Park'  ,'ryv' :"Yoshi Valley"  ,# Coupe Feuille Morte
                'rttc': "Tick-Tock Clock", 'rpps' : 'Piranha Plant Slide','rgv' :" Grumble Volcano"  , 'rrrd' :"Rainbow Road N64",#coupe Eclair
                'dbp' : "Baby Park" , 'dcl' :"Cheese Land" , 'dww' : " Wild Woods", 'dac' :"Animal Crossing" ,#Coupe Feuille
                'dnbc' :"Neo Bowser City", 'drir' : "Ribbon Road", 'dsbs' :"Super Bell Subway", 'dbb' : "Big Blue", #Coupe Cloche
                'week' :"Map of the Week" 
}

statsPoints = { 1 : 15 , 
                2 : 12,
                3 : 10, 
                4 : 9 ,
                5 : 8 ,
                6 : 7 ,
                7 : 6 ,
                8 : 5 ,
                9 : 4 ,
                10 : 3 ,
                11 : 2 ,
                12 : 1 
                 }

class mapmk:

    def __init__(self , mapmk, objective, bonusObjective):
        self._mapmk= mapmk
        self._objective= objective
        self._bonusObjective= bonusObjective
        self._ttplayers = []

    def setObjective(self, objective):
        self._objective= objective
    
    def setBonusObjective(self, bonusObjective):
        self._bonusObjective = bonusObjective
    
    def  addplayer(self, ttplayer):
        add = True
        for player in self._ttplayers:
            if player.getPlayerId() == ttplayer.getPlayerId() :
                sameplayer = player
                add = False
        if add == True :
            self._ttplayers.append(ttplayer)
        else :
            sameplayer.setPlayerName(ttplayer.getPlayerName())
            sameplayer.setPlayerTime(ttplayer.getPlayerTime())
        self._ttplayers = sorted(self._ttplayers, key=lambda ttplayer : ttplayer._time )

    def addplayers(self,ttplayers):
        for player in ttplayers :
            self.addplayer(player)

    def asDict(self):
        ttplayerDict=[]
        for player in self._ttplayers:
            ttplayerDict.append(player.asDict()) 
        return { 'objective' : self._objective , 'bonusObjective' : self._bonusObjective , 'ttplayers' : ttplayerDict}

    def writeFile(self, file):
        with open(file,'w') as json_file:
            json.dump(self.asDict(), json_file)
            json_file.close()


    def getFileR(self, file):
        try :
            with open(file,"r") as jsonfile :
                data = json.loads(jsonfile.read())
                jsonfile.close()
                return data
        except :
            return "no file"

    def dataToMapmk(self, data):
        if data != 'no file' :
            self._objective = data.get("objective")
            self._bonusObjective = data.get("bonusObjective")
            ttplayers = data.get("ttplayers")
            for player in ttplayers :
                newplayer =ttplayer.TtPlayer(player.get("id"),player.get("name"), player.get("time"))
                self._ttplayers.append(newplayer)
        

    def deleteTtplayer(self, idplayer):
        for player in self._ttplayers :
            if int(player.getPlayerId()) == int(idplayer) :
                self._ttplayers.remove(player)
    
    def addStats(self, playersStats):
        i = 1 
        for player in self._ttplayers :
            if not player.getPlayerId() in playersStats :
                playersStats.update({player.getPlayerId() : [ player.getPlayerName() , statsPoints.get(i ,1 ) , 1 ]})
                i += 1
            else :
                listplayer = playersStats.get(player.getPlayerId())
                listplayer[1] += statsPoints.get(i , 1)
                listplayer[2] += 1
                i += 1 

        
