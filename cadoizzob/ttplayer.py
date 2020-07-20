import json

class TtPlayer:

    def __init__(self,id, name,time):
        self._id = id
        self._name = name
        self._time= time
    
    def getPlayerId(self):
        return self._id

    def getPlayerName(self):
        return self._name
    
    def setPlayerName(self, name):
        self._name = name

    def getPlayerTime(self):
        return self._time
    
    def setPlayerTime(self, time):
        self._time= time

    def asDict(self):
        return {'id' : self._id ,'name': self._name , 'time' : self._time}

    def string(self):
        return "{0} ** \n Temps : {1}\n\n".format(self._name , self._time)

    def __str__(self):
        return "<Ttplayer name {0}>".format(self._name)

    






