import json

class TtPlayer:

    def __init__(self,id, name,time):
        self._id = id
        self._name = name
        self._time= time
        self._team = "LU1"
    
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

    def getTime(self):
        t = self._time.split(":")
        minutes = t[0]
        sms = t[1].split(".")
        hour = 0
        return (hour ,int(minutes), int(sms[0]), int(sms[1]))

    def getDifSecond(self, ttplayer):
        (h , m , s , ms) = self.getTime()
        (h1, m1 , s1 , ms1 ) = ttplayer.getTime()
        msf = ms - ms1 
        if msf < 0 :
            s1 +=1 
        msf = msf%1000 # milliseconds
        #transform all in seconds
        secondsFinal = s - s1 +  (m - m1) *60 + (h - h1) * 3600 
        minFinal = 0
        while ( secondsFinal > 60 ) :
            minFinal += 1
            secondsFinal -= 60
        return ( minFinal, secondsFinal, msf)
        




    def asDict(self):
        return {'id' : self._id ,'name': self._name , 'time' : self._time}

    def string(self):
        return "{0} ** \n Temps : {1}\n\n".format(self._name , self._time)

    def __str__(self):
        return "<Ttplayer name {0}>".format(self._name)

    






