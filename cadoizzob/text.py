import re

# File path
path = "tt/"
shroomPath = "shroom/"
noShroomPath = "noshroom/"

# FOrmat of the TT time; example : 
timesample = re.compile('^\d:\d{2}\.\d{3}$')
idsample = re.compile('^\d{10,35}$')
tagsample = re.compile('^<@!\d{10,30}>$')
rolesample = re.compile('^<@&\d{10,30}>$')

# Dict of all map and the key by cup.
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

helpTextFr = {
    "help" : "```Il y'a trois commandes pour l'instant :\n"
            + "{0}settings -> Pour changer les settings du serveur\n"
            + "{0}war -> Utiliser pour des disponibilités\n"
            + "{0}tt -> Enregistrer vos TT et plein d'autres fonction\n"
            + "Toutes les commandes ont une option help```"
}

helpTextEn = {
    "help" : "```There is three commands for now :\n"
            + "{0}settings -> To change settings of your server\n"
            + "{0}war -> Use for availability\n"
            + "{0}tt -> Record your TT and many other functions\n"
            + "Every commands have a help function```"
}

helpTexts = {
    "fr"    : helpTextFr,
    "en"    : helpTextEn
}

# Dict of string for war command 
warTextFr = { 
    "help": "```"
            + "{0}war vacances  --> Propose des wars de 14h à 00h du matin\n"
            + "{0}war XX XX...  --> Propose des wars à XXh. Exemple : {0}war 18 21 23\n\n"
            + "Principes importants du bot :\n"
            + "• Le bot ajoute un 'h' à chaque mot écrit après {0}war (sauf '{0}war vacances')\n"
            + "• Le bot ajoute les 3 emotes sur son propre message suite à la commande utilisée\n"
            + "• Sur tous les messages du discord : le bot enlève sa propre emote dès qu'il y a 4 émotes sur le message + le bot remet sa propre emote dès que les emotes redescendent à 1 (de ce fait il garde toujours l'ordre des emotes)\n\n"
            + "Si vous avez des retours ou des idées de commandes à ajouter qui pourraient être sympas, n'hésitez pas à me MP à @Cadoizz#5176 !```",    
    "args" : "Pas d'arguments à la commande war! pour plus d'infos **{0}war help** ",
    "noOption" : "Coucou on a pas ton option **{0}war help** est la pour te servir"  
    }

warTextEn = { 
    "help": "```{0}war vacances  --> Propose wars from 2PM to 12PM \n"
            + "{0}war XX XX...  --> Propose wars at XXh. Example: {0}war 18 21 23\n\n"
            + "Important principles of the bot:\n"
            + "• The bot adds an 'h' to every word written after {0}war (except '{0}war vacances')\n"
            + "• Once the command is used the bot will add the 3 emotes to its own message\n"
            + "• On all discord messages: the bot removes its own emote as soon as therare 4 emotes on the message + the bot gives his own emote as soon as the emotes go down to 1 (thereby it always keeps the emote order)\n\n"
            + "If you have any feedback or ideas to add that might be nice, feel free to DM me at @Cadoizz#5176!```",
    
    "args" : "No arguments **{0}war help** for more info",
    "noOption" : "Hey, your option doesn't exist so **{0}war helpCoucou on a pas ton option **{0}war help** est la pour te servir"  
    }

warTexts = {
    "fr"    : warTextFr,
    "en"    : warTextEn
}

# Dict of string for tt command
ttTextsFr = {
    "help"      :  "```<map> correspond soit aux raccourcis anglais des maps de mk8dx et à 'week' si vous voulez vous faire un tt de la semaine, de plus la commande {0}tt maps , renvoie une image avec les raccourcis utilisés.\n"
                    +"<time> doit suivre le modèle suivant : x:xx.xxx ; où les x sont des chiffres\n"
                    +"<id> correspond à l'identifiant discord de quelqu'un sinon celà ne marche pas, le tag marche aussi maintenant\n"
                    +"Tous les arguments peuvent être passé en miniscule ou majuscule, le bot les lira en minuscules.\n "
                    +"----------------------------------------------------------\n"
                    +"Ces commandes ne demandent aucun droit n'importe qui sur le serveur peut les utiliser\n"
                    +"Ajouter 'ni' après {0}tt , fait réfèrence au run no item , soit shroomless! Toutes les commandes suivantes marche de la même manière avec 'ni'. Exemple : {0}tt ni find . \n\n "
                    +"{0}tt <map> --> affiche si un fichier existe les temps de la map.\n" 
                    +"{0}tt <map> <time> --> ajoute ton temps à la <map> ou le remplace s'il y en a dejà un\n"
                    +"{0}tt <map> delete --> Supprime ton temps de la map\n"
                    +"{0}tt addlist help --> Affiche l'help de addlist\n"
                    +"{0}tt addlist <List> --> Ajoute plusieur map, aller voir {0}tt addlist help pour voir le format demandé\n"
                    +"{0}tt find --> Trouve toutes les maps ou tu apparais\n"
                    +"{0}tt find <id> --> Trouve toutes les maps ou <id> apparait\n"
                    +"{0}tt copy <idServ> --> Copie tes temps de ce serveur\n"                   
                    +"{0}tt stats --> Montre un classement des membres par moyenne des places\n"
                    +"{0}tt stats time--> Montre un classement des membres par temps de toutes les maps ajoutées\n"
                    +"Vous devez avoir ajouté les 48 maps pour y apparaître."
                    +"la map 'week' ne compte pas dans les stats```",
    "help2"     : "```Les commandes ci-dessous nécessitent le droit de gérer les messages sur le serveur\n\n"
                    +"{0}tt create --> Creer un dossier pour le serveur et permet d'y stocker les maps\n\n"
                    +"WARNING -> {0}tt delete --> Supprime le dossier du serveur et ce qu'il y'a dedans \n\n"
                    +"{0}tt delete <id> --> Supprime tous les temps de <id> dans les fichiers\n\n"
                    +"{0}tt delete <map> --> Supprime le fichier d'une map \n\n"
                    +"{0}tt <map> delete <id> --> Supprime le joueur <id> dans le fichier <map>\n\n"
                    +"{0}tt <map> objective <time> --> Ajoute <time> à la variable objective\n\n"
                    +"{0}tt <map> bonus <time> --> Ajoute <time> à la variable ObjectiveBonus\n\n"
                    +"{0}tt <map> objective delete --> Supprime le temps objective\n\n"
                    +"{0}tt <map> bonus delete --> Supprime le temps objectiveBonus\n```",
    "perm"      : "Tu n'as pas les perms pour cette commande",
    "noArg"       : "Pas d'arguments à la commande tt ! pour plus d'infos **{0}tt help** ",
    "create"    : "Votre Serveur a maintenant un fichier pour vos TT.Vous pouvez les remplirs",
    "pathExist" : "Votre serveur a deja un fichier, **{0}tt help**, pour savoir comment rentré vos temps",
    "delete"    : "Les fichiers de TT ont bien été supprimé",
    "wrongName" : "{0} n'est ni une commande ou une map disponible **{0}tt help** ou **{0}tt maps** pour t'aider",
    "noFile"    : "Votre serveur n'a pas de fichier , utiliser la commande *{0}tt create** pour en avoir un"
                    +" et pouvoir ajoutez vos temps sur les maps.",
    "noFileMap" : "Pas de fichier pour cette map, ajoutes un temps pour le créer." ,
    "badFormat" : "Temps au mauvais format, exemple : **1:20.546** \n ou trop d'arguments.",
    "registred" : "Votre temps a bien été enregistré.",
    "allMap"    : '```{0}tt addList "mks , <time> ; wp , <time> ; ssc , <time> ; tr , <time>;\n'
                + 'mc , <time> ; th , <time> ;  tm , <time> ;  sgf , <time>;\n'
                + 'sa , <time> ; ds , <time> ; ed , <time> ;  mw , <time>;\n'
                + 'cc , <time> ; bdd , <time> ; bc , <time> ; rr , <time>;\n'
                + 'dyc , <time> ; dea , <time> ; ddd , <time> ; dmc , <time>;\n'
                + 'dwgm , <time> ; drr , <time> ; diio , <time> ; dhc , <time>;\n'
                + 'rmmm , <time> ; rmc , <time> ; rccb , <time> ; rtt , <time>;\n'
                + 'rddd , <time> ; rdp3 , <time> ; rrry , <time> ; rdkj , <time>;\n'
                + 'rws , <time> ; rsl , <time> ; rmp , <time> ; ryv , <time>;\n'
                + 'rttc , <time> ; rpps , <time> ; rgv , <time> ; rrrd , <time>;\n'
                + 'dbp , <time> ;  dcl , <time> ; dww , <time> ; dac , <time>;\n'
                + 'dnbc , <time> ; drir , <time> ; dsbs , <time> ; dbb , <time>"```',
    "helpAllMap": 'Copier au dessus pour toutes les maps et remplacer les <time> par votre temps\nExample de Format: {0}tt addList "<map> , <time> ; <map> , <time> ; ..."\n'
                + "La virgule permet séparer la map de son temps\n"
                + "Le point virgule permet de passer à la prochaine map\n"
                + 'Ne pas oublier les " sinon ca ne marchera pas\n',
    "unknowCmd" : "Commande inconnue **{0}tt help** pour t'aider",
    "tooMuchArg": "Trop d'argument pour la commande, **{0}tt help** pour t'aider",
    "wrongID"   : "Ceci {0} ne ressemble pas à un ID discord",
    "shutilFail": "Vos fichiers n'ont pas été supprimé, ceci ne devrait pas arrivé",
    "objAdd"    : "Objectif Ajouté",
    "objBAdd"   : "Objectif bonus ajouté",
    "objSup"    : "Objectif Supprimé",
    "objBSup"   : "Objectif bonus supprimé",
    "timeSup"   : "Votre temps a bien été supprimé",
    "hisTimeSup": "Le temps du joueur {0} a bien été supprimé.",
    "wrongServ" : "Le serveur ciblé n'existe pas / mauvais id, n'hésitez pas a essayé une commande dans le serveur ciblé, pour voir s'il marche.",
    "noMapFile" : "Pas de fichier de ce nom",
    "mapFileSup": " La fichier de la map {0} a été supprimé",
    "noMorePlayer": "Plus de joueur dans la map {0}",
    "supPlayer" :"Le joueur avec l'id {0} a été supprimé de tous les fichiers",
    "addTimeMap": "Votre temps a bien été enregistré sur {0}",
    "copy"      : "Transfert terminé !",
    "notFind"   : "Le joueur n'a pas été trouvé."
}

ttTextsEn = {
    "help"      :  "```<map> corresponds either to the English shortcuts for mk8dx maps and to 'week' if you want to do a tt of the week, moreover the command {0} tt maps, returns an image with the shortcuts used.\n"
                    +"<time> must follow the following pattern: x:xx.xxx; where the x's are numbers\n"
                    +"<id> matches someone's discord id otherwise it doesn't work, the tag now works too\n"
                    +"All arguments can be passed in lowercase or uppercase, the bot will read them in lowercase.\n "
                    +"----------------------------------------------------------\n"
                    +"These commands do not require any rights anyone on the server can use them\n"
                    +"Ajouter 'ni' après {0}tt , fait réfèrence au run no item , soit shroomless! Toutes les commandes suivantes marche de la même manière avec 'ni'. Exemple : {0}tt ni find . \n\n "
                    +"{0}tt <map> --> displays if a file exists the times of the map.\n" 
                    +"{0}tt <map> <time> --> add your time to the <map> or replace it if there is already one\n"
                    +"{0}tt <map> delete --> Remove your time from the map\n"
                    +"{0}tt addlist help --> Show addlist help\n"
                    +"{0}tt addlist <List> --> Add several map, go to {0}tt addlist help to see the requested format\n"
                    +"{0}tt find --> Find all the maps where you appear\n"
                    +"{0}tt find <id> --> Find all maps where <id> appears\n"
                    +"{0}tt copy <idServ> --> Copy your times from this server\n"                   
                    +"{0}tt stats --> Show a classement of the server with the average position in all the maps.\n"
                    +"{0}tt stats time --> Show a classement of the server with the total time in all the maps.\n"
                    +"you have to have the 48 maps fill or you won't appear."
                    +"the 'week' map does not count in the stats, and you got points for every map which you are not in.```",
    "help2"     : "```The commands below require the right to manage messages on the server\n\n"
                    +"{0}tt create --> Create a folder for the server and store the maps there\n\n"
                    +"WARNING -> {0}tt delete --> Delete the server folder and what's in it, there is no verification\n\n"
                    +"{0}tt delete <id> --> Remove all times from <id> in files\n\n"
                    +"{0}tt delete <map> --> Delete the file from a map \n\n"
                    +"{0}tt <map> delete <id> --> Remove player <id> from file <map>\n\n"
                    +"{0}tt <map> objective <time> --> add <time> to the objective\n\n"
                    +"{0}tt <map> bonus <time> --> add <time> to the objective bonus\n\n"
                    +"{0}tt <map> objective delete --> Removes objective time\n\n"
                    +"{0}tt <map> bonus delete --> Removes bonus objective time\n```",
    "perm"      : "You don't have the perms for this order",
    "noArg"       : "No arguments to the tt command! for more info ** {0}tt help **",
    "create"    : "Your Server now has a file for your TTs, you can fill them in",
    "pathExist" : "Your server already has a file, ** {0}tt help **, to know how to enter your times",
    "delete"    : "TT files have been deleted successfully",
    "wrongName" : "Your args is not an available command or map ** {0}tt help ** or ** {0}tt maps ** to help you",
    "noFile"    : "Your server does not have a file, use the command * {0} tt create ** to have one"
                    +" files and you can add your time.",
    "noFileMap" : "No file for this map, add a time to create it." ,
    "badFormat" : "Time in wrong format, example: **1:20.546** , or too many arguments.",
    "registred" : "Your time has been registred.",
    "allMap"    : '```{0}tt addList "mks , <time> ; wp , <time> ; ssc , <time> ; tr , <time>;\n'
                + 'mc , <time> ; th , <time> ;  tm , <time> ;  sgf , <time>;\n'
                + 'sa , <time> ; ds , <time> ; ed , <time> ;  mw , <time>;\n'
                + 'cc , <time> ; bdd , <time> ; bc , <time> ; rr , <time>;\n'
                + 'dyc , <time> ; dea , <time> ; ddd , <time> ; dmc , <time>;\n'
                + 'dwgm , <time> ; drr , <time> ; diio , <time> ; dhc , <time>;\n'
                + 'rmmm , <time> ; rmc , <time> ; rccb , <time> ; rtt , <time>;\n'
                + 'rddd , <time> ; rdp3 , <time> ; rrry , <time> ; rdkj , <time>;\n'
                + 'rws , <time> ; rsl , <time> ; rmp , <time> ; ryv , <time>;\n'
                + 'rttc , <time> ; rpps , <time> ; rgv , <time> ; rrrd , <time>;\n'
                + 'dbp , <time> ;  dcl , <time> ; dww , <time> ; dac , <time>;\n'
                + 'dnbc , <time> ; drir , <time> ; dsbs , <time> ; dbb , <time>"```',
    "helpAllMap": 'COpy everything and change <time> by your time in the map wich is on the left of **,**\n'
                + 'Example of command line to add many maps: {0}tt addList "<map> , <time> ; <map> , <time> ; ..."\n'
                + "**,** is to separate args in the command line\n"
                + "**;** is too séparate the next command line\n"
                + 'Dont forget **"** , without them it doesnt work\n',
    "unknowCmd" : "Unknonws command **{0}tt help** to help you",
    "tooMuchArg": "Too many args for this command, **{0}tt help** to help you",
    "wrongID"   : "This {0} doesn't look like an discord ID",
    "shutilFail": "Your files were not deleted, this shouldn't have happened",
    "objAdd"    : "Objective Add",
    "objBAdd"   : "Objective bonus add",
    "objSup"    : "Objective deleted",
    "objBSup"   : "Objective bonus deleted",
    "timeSup"   : "Your time has been deleted",
    "hisTimeSup": "Time's player {0} has been deleted",
    "wrongServ" : "The targeted server doesn't exist or bad ID, don't hesitate to try the bot on the target server to check if it works.",
    "noMapFile" : "No file of this name",
    "mapFileSup": " Map file {0} has been deleted",
    "noMorePlayer": "No more player in map {0}",
    "supPlayer" :"Player with id {0} has been deleted from all files",
    "addTimeMap": "Your time is registred in {0}",
    "copy"      : "Copy done!",
    "notFind"   : "The player was not find in the map"
}

ttTexts = {
    "fr"    : ttTextsFr,
    "en"    : ttTextsEn
}

settingsTextsEn = {
    "noArgs"    : "No arguments for the settings command! For more info ** {0}settings help **",
    "help"      : "```Settings help : You can for now change your language and your prefix ( the way you call the bot )\n"
            + "{0}settings prefix <arg> -> This will change the prefix to <arg> and you will know use the bot with <arg>\n"
            + "{0}settings language <L> -> Will change the language to <L> : for now FR and EN are available.\n```",
    "tooManyArg": "Too many Arg for the command, **{0}settings help** to help you ",
    "wrongLanguage": "Language doesn't exist, for now only FR and EN works, **{0}settings help** to help you",
    "noCmd"     : "No Command with this name, **{0}settings help** to help you ",
    "prefix"    : "Your prefix has change to {0}",
    "language"  : "Your language has change to {0}",
    "check"     : "Your language is {0} and your prefix is {1}"
    
}

settingsTextsFr = {
    "noArgs"    : "Aucun argument pour la commande des paramètres! Pour plus d'informations ** {0} aide sur les paramètres **",
    "help"      : "``` Aide sur les paramètres: vous pouvez pour l'instant changer votre langue et votre préfixe (la façon dont vous appelez le bot) \n"
            + "{0}settings prefix <arg> -> Cela changera le préfixe en <arg> et vous saurez utiliser le bot avec <arg> \n"
            + "{0}settings language <L> -> Va changer la langue en <L>: pour l'instant FR et EN sont disponibles.\n```",
    "tooManyArg": "Trop d'arg pour la commande, **{0}settings help** pour vous aider",
    "wrongLanguage": "La langue n'existe pas, pour l'instant seuls FR et EN fonctionnent,** {0} settings help ** pour vous aider",
    "noCmd"     : "Pas de commande de ce nom , **{0}settings help** pour t'aider.",
    "prefix"    : "Le prefix du bot a été changé en {0}",
    "language"  : "La langue a été changé en {0}",
    "check"     : "La langue du bot est {0} et le prefix du bot est {1}"
}

settingsTexts = {
    "fr"    : settingsTextsFr,
    "en"    : settingsTextsEn
}