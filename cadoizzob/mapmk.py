import ttplayer
import json
import discord

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
        #Look if the player already exists
        for player in self._ttplayers:
            if player.getPlayerId() == ttplayer.getPlayerId() :
                sameplayer = player
                add = False
        if add == True :
            self._ttplayers.append(ttplayer)
        else :
            sameplayer.setPlayerName(ttplayer.getPlayerName())
            sameplayer.setPlayerTime(ttplayer.getPlayerTime())
            sameplayer.setPlayerUrl(ttplayer.getPlayerUrl())
        # sorted every time we add a player
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

    # Data from json to a mapmk
    # no return !
    def dataToMapmk(self, data):
        if data != 'no file' :
            self._objective = data.get("objective")
            self._bonusObjective = data.get("bonusObjective")
            ttplayers = data.get("ttplayers")
            for player in ttplayers :
                newplayer =ttplayer.TtPlayer(player.get("id"),player.get("name"), player.get("time"),player.get("url"))
                self._ttplayers.append(newplayer)
        

    def deleteTtplayer(self, idplayer):
        for player in self._ttplayers :
            if int(player.getPlayerId()) == int(idplayer) :
                self._ttplayers.remove(player)
    
    def checkPlayer(self,nbDraw, newPlayer , oldPlayer):
        if (oldPlayer == None):
            return nbDraw,newPlayer
        if ( newPlayer.getPlayerTime() == oldPlayer.getPlayerTime()):
            return nbDraw+1 , newPlayer
        else : 
            return nbDraw, newPlayer
    # Get place of every player of the mapmk in the dictionary playersStats
    def addStats(self, playersStats):
        i = 1 
        nbDraw = 0
        oldPlayer = None
        for player in self._ttplayers :
            nbDraw, oldPlayer = self.checkPlayer( nbDraw, player , oldPlayer)
            if not player.getPlayerId() in playersStats :
                playersStats.update({player.getPlayerId() : [ player.getPlayerName() , (i-nbDraw) , 1 ]})
                i += 1
            else :
                listplayer = playersStats.get(player.getPlayerId())
                listplayer[1] += (i-nbDraw)
                listplayer[2] += 1
                i += 1 

    def addStatsTime(self, playersStats):
        for player in self._ttplayers :
            if not player.getPlayerId() in playersStats :
                playersStats.update({player.getPlayerId() : [ player.getPlayerName() , player.getTime() , 1 ]})
            else :
                listplayer = playersStats.get(player.getPlayerId())
                listplayer[1] = tuple(map(sum,zip(listplayer[1], player.getTime())))
                listplayer[2] += 1
        
