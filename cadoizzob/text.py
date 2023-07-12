import re

# 

urlImgCadoizzob = "https://cdn.discordapp.com/attachments/729655998146674748/731625550858158102/cadoizz-bot-400x400px.png"
nofile= 'no file' # help return statement

# File path
path = "tt/"
shroomPath = "shroom/"
noShroomPath = "noshroom/"
speedPath = "200cc/"

# FOrmat of the TT time; example : 
timesample = re.compile('^\d:\d{2}\.\d{3}$')
idsample = re.compile('^\d{10,35}$')
tagsample = re.compile('^<@!\d{10,30}>$')
rolesample = re.compile('^<@&\d{10,30}>$')
urlsample = re.compile('^https:\/\/(www.youtube|twitter|gyazo).com\/.{1,45}$')

# Dict of all map and the key by cup.
MK8DXmap = { "mks" : "Mario Kart Stadium" , 'wp' :"Water Park" , 'ssc' : "Sweet Sweet Canyon" , 'tr' :"Thwomp Ruins" ,     # coupe Champignon
                'mc' : "Mario Circuit" , 'th' : "Toad Harbor" , 'tm' : "Twisted Mansion" , 'sgf' : "Shy Guy Falls",# coupe Fleur
                'sa' :"Sunshine Airport"  , 'ds' : "Dolphin Shoals"  , 'ed' : "Electrodrome" , 'mw' : "Mount Wario"  ,#coupe Etoile
                'cc' : "Cloudtop Cruise" , 'bdd' : 'Bone-Dry Dunes' , 'bc' : "Bowser's Castle" , 'rr' :"Rainbow Road"  ,# coupe Spéciale
                'dyc' :"Yoshi Circuit" , 'dea' :"Excitebike Arena" , 'ddd' :"Dragon Driftway" , 'dmc' :"Mute City" ,# coupe Oeuf
                'dbp' : "Baby Park" , 'dcl' :"Cheese Land" , 'dww' : "Wild Woods", 'dac' :"Animal Crossing" ,#Coupe Feuille
                'rmmm' :"Moo Moo Meadows", 'rmc' : "Mario Circuit GBA" , 'rccb' :"Cheep Cheep Beach", 'rtt' :"Toad's Turnpike" ,#coupe Carapace
                'rddd' : "Dry Dry Desert", 'rdp3' : "Donut Plains 3", 'rrry' :"Royal Raceway", 'rdkj' : 'DK Jungle',# coupe Banane
                'rws' : "Wario Stadium", 'rsl' : "Sherbet Land" ,'rmp' : 'Music Park'  ,'ryv' :"Yoshi Valley"  ,# Coupe Feuille Morte
                'rttc': "Tick-Tock Clock", 'rpps' : 'Piranha Plant Slide','rgv' :"Grumble Volcano"  , 'rrrd' :"Rainbow Road N64",#coupe Eclair
                'dwgm' :"Wario's Gold Mine", 'drr' :"Rainbow Road SNES" , 'diio' :"Ice Ice OutPost", 'dhc' : "Hyrule Circuit" ,#coupe Hyrule
                'dnbc' :"Neo Bowser City", 'drir' : "Ribbon Road", 'dsbs' :"Super Bell Subway", 'dbb' : "Big Blue", #Coupe Cloche
                'week' :"Map of the Week" 
}

nbMK8DXmap = 48

MK8DXbooster = { "bpp" : "Tour Paris Promenade" , "btc" : "3DS Toad Circuit" , "bcm64" : "N64 Choco Mountain" , "bcmw" : "Wii Coconut Mall" ,# nouvelle première coupe
                "btb" : "Tour Tokyo Blur" , "bsr" : "DS Shroom Ridge", "bsg" : "GBA Sky Garden" , "bnh" : "Tour Ninja Hydeaway", # seconde coupe
                "bnym" : "MKT New York" , "bmc3" : "SNES Mario Circuit 3" , "bkd" : "N64 Kalimari Desert" , "bwp" : "DS Flipper Waluigi", #troisième coupe
                "bss" : "MKT Sydney", "bsl" : "GBA Snow Land" , "bmg" : "WII Mushroom Gorge" , "bshs" :"Sky High Sundae", #4ème coupe
                "bll" : "London Loop", "bbl" : "Boo Lake" ,"brrm" : "Rock Rock Mountain", "bmt" : "Maple Treeway" ,  # 5ème coupe
                "bbb" : "Berlin Byways", "bpg" : "Peach Gardens", "bmm" : "Merry Mountain", "brr7" : "Rainbow Road", #6eme coupe 
                "bad" : "Amsterdam Drift" ,"brp" : "Riverside Park" , "bdks" : "DK Summit" , "byi" : "Yoshi's Island", # 7eme coupe
                "bbr" : "Bangkok Rush" , "bmc" : "DS Mario Circuit" , "bws" : "Waluigi Stadium" , "bsis" : "Singapore Speedway", # 8eme coupe
                "batd" : "Athens Dash" , "bdc" : "Daisy Cruiser" , "bmh" : "Moonview Highway" , "bscs" : "Squeaky Clean Sprint", # 9eme coupe
                "blal" : "Los Angeles Laps" , "bsw" : "Sunset Wilds" , "bkc" : "Koopa Cape" , "bvv" : "Vancouver Velocity" # 10 eme coupe
 }

nbMK8DXbooster = 40

helpTextFr = {
    "help" : "```Il y'a trois commandes pour l'instant :\n"
            + "/settings -> Pour changer les settings du serveur\n"
            + "/war -> Utiliser pour des disponibilités\n"
            + "/tt -> Enregistrer vos TT et plein d'autres fonction\n"
            + "Toutes les commandes ont une option help```"
}

helpTextEn = {
    "help" : "```There is three commands for now :\n"
            + "/settings -> To change settings of your server\n"
            + "/war -> Use for availability\n"
            + "/tt -> Record your TT and many other functions\n"
            + "Every commands have a help function```"
}

helpTexts = {
    "fr"    : helpTextFr,
    "en"    : helpTextEn
}

# Dict of string for war command 
warTextFr = { 
    "help": "```"
            + "/war <first> <second> --> Ecrit les heures comprises entre <first> et <second>. Exemple : **/war 21 25** va demander envoyer des messages pour les horaires : 21 22 23 00 01\n\n"
            + "Principes importants du bot :\n"
            + "• Le bot envoie un message pour chaque horaire entre les deux variables modulo 24 (le reste de la division par 24)\n"
            + "• Le bot ajoute les 3 emotes sur son propre message suite à la commande utilisée\n"
            + "Si vous avez des retours ou des idées de commandes à ajouter qui pourraient être sympas, n'hésitez pas à me MP à @Cadoizz#5176 !```",    
    "args" : "Pas d'arguments à la commande war! pour plus d'infos **/war help** ",
    "noOption" : "Coucou on a pas ton option **/war help** est la pour te servir"  
    }

warTextEn = { 
    "help": "```"
            + "/war <first> <second> --> Write hour between <first> and <second> . Example: **/war 10 14** will write for the hour : 10 11 12 0 1 \n\n"
            + "Important principles of the bot:\n"
            + "• The bot send message for the hours between the two parameters modulo 13 ( the rest of the division by 13 )\n"
            + "• Once the command is used the bot will add the 3 emotes to its own message\n"
            + "If you have any feedback or ideas to add that might be nice, feel free to DM me at @Cadoizz#5176!```",
    "args" : "No arguments **/war help** for more info",
    "noOption" : "Hey, your option doesn't exist. To guide you : **/war help**"  
    }

warTexts = {
    "fr"    : warTextFr,
    "en"    : warTextEn
}

# Dict of string for tt command
ttTextsFr = {
    "help"      :  "```Pour utiliser ce bot : le paramètre 'option' est obligatoire.\n Si vous choissisez 150cc ou 200cc alors il faut **absolument** définir l'option "
                    +" 'categorie' avec shroom ou ni ( pour sans item) \n Puis vous choissisez les options 'third', 'four' , 'five' selon le nombre de paramètre de la commande.\n"
                    +"Mais attention toujours dans 'l'ordre'\n"
                    +"Un exemple pour ajouter un temps : /tt option:150cc categorie:ni third:rws four:3:12.345\n"
                    +"Exemple pour afficher les raccourcis des maps : /tt options:maps"
                    +"<map> correspond aux raccourcis anglais des maps de mk8dx et à 'week' si vous voulez vous faire un tt de la semaine, de plus la commande /tt maps , renvoie une image avec les raccourcis utilisés.\n"
                    +"<time> doit suivre le modèle suivant : x:xx.xxx ; où les x sont des chiffres\n"
                    +"<id> correspond à l'identifiant discord de quelqu'un sinon celà ne marche pas, le tag marche aussi maintenant\n"
                    +"Tous les arguments peuvent être passé en miniscule ou majuscule, le bot les lira en minuscules.\n``` ",
    "help2"     :   "```Ces commandes ne demandent aucun droit n'importe qui sur le serveur peut les utiliser\n"
                    +"Les deux premiers paramètres définissent les catégories : 150 ou 200 et ni ou shroom, pour choisir dans quel type de fichier vous voulez vous placer. Ensuite vous rajouter les commandes ci-dessous pour avoir ceux que vous voulez\n"
                    +"Faites attention à l'ordre ! En premier le paramètre option ( obligatoire) mais en second vous devez mettre la paramètre **categorie** pour tout ce qui est relié au TT ensuite third, four , five.\n\n"
                    +"/tt <map> --> affiche si un fichier existe les temps de la map.\n" 
                    +"/tt <map> <time> <lien>--> ajoute ton temps à la <map> ou le remplace s'il y en a dejà un, le lien est optionel\n"
                    +"/tt <map> delete --> Supprime ton temps de la map\n"
                    +"/tt addlist help --> Affiche l'help de addlist\n"
                    +"/tt addlist <List> --> Ajoute plusieur map, aller voir /tt addlist help pour voir le format demandé\n"
                    +"/tt <id> <map> --> Affiche le temps du joueur <id> sur la map <map> avec les temps des joueurs devant et derrière lui.\n"
                    +"/tt copy <idServ> --> Copie tes temps du serveur <idServ> dans la catégorie donné , '/tt ni copy <idServ> pour copier les temps shroomless\n"     
                    +"Pour les commandes ci-dessous on peut rajouter b ( ou booster) ou total à la fin des commandes pour avoir que les maps boosters ou le total de toutes les maps\n"
                    +"/tt find --> Trouve toutes les maps ou tu apparais\n"
                    +"/tt find <id> --> Trouve toutes les maps ou <id> apparait, ici on rajoute b ou total entre le find et <id>\n"              
                    +"/tt stats --> Montre un classement des membres par moyenne des places\n"
                    +"/tt stats time--> Montre un classement des membres par temps de toutes les maps ajoutées\n"
                    +"Vous devez avoir ajouté les 48 maps pour y apparaître."
                    +"la map 'week' ne compte pas dans les stats```",
    "help3"     : "```Les commandes ci-dessous nécessitent le droit de gérer les messages sur le serveur\n\n"
                    +"/tt create --> Creer un dossier pour le serveur et permet d'y stocker les maps\n\n"
                    +"/tt delete <id> --> Supprime tous les temps de <id> dans les fichiers\n\n"
                    +"/tt delete <map> --> Supprime le fichier d'une map \n\n"
                    +"/tt <map> delete <id> --> Supprime le joueur <id> dans le fichier <map>\n\n"
                    +"/tt <map> objective <time> --> Ajoute <time> à la variable objective\n\n"
                    +"/tt <map> bonus <time> --> Ajoute <time> à la variable ObjectiveBonus\n\n"
                    +"/tt <map> objective delete --> Supprime le temps objective\n\n"
                    +"/tt <map> bonus delete --> Supprime le temps objectiveBonus\n\n"
                    +"Les commandes ci-dessous nécissitent le droit Administrateur sur le serveur\n\n"
                    +"WARNING -> /tt deleteAll --> Supprime le dossier du serveur et ce qu'il y'a dedans \n\n```"
                    +"Si vous voulez aidez à la durée de ce bot, vous pouvez aider à payer Arcégis qui héberge le bot.\n"
                    +"Vous pouvez l'aider en donnant même des petites sommes sur le paypal : https://paypal.me/arcegis",
    "perm"      : "Tu n'as pas les perms pour cette commande",
    "noArg"       : "Pas d'arguments à la commande tt ! pour plus d'infos **/tt help** ",
    "create"    : "Votre Serveur a maintenant un fichier pour vos TT.Vous pouvez les remplirs",
    "pathExist" : "Votre serveur a deja un fichier, **/tt help**, pour savoir comment rentré vos temps",
    "delete"    : "Les fichiers de TT ont bien été supprimé",
    "wrongName" : "{0} n'est ni une commande ou une map disponible **/tt help** ou **/tt maps** pour t'aider",
    "noFile"    : "Votre serveur n'a pas de fichier , utiliser la commande */tt create** pour en avoir un"
                    +" et pouvoir ajoutez vos temps sur les maps.",
    "noFileMap" : "Pas de fichier pour cette map, ajoutes un temps pour le créer." ,
    "badFormat" : "Temps au mauvais format, exemple : **1:20.546** \n ou trop d'arguments.",
    "registred" : "Votre temps a bien été enregistré.",
    "allMap"    : '```/tt addList mks , <time> ; wp , <time> ; ssc , <time> ; tr , <time>;\n'
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
                + 'dnbc , <time> ; drir , <time> ; dsbs , <time> ; dbb , <time>```',
    "boosterMap" : '```/tt addList bpp , <time> ; btc , <time> ; bcm64 , <time> ; bcmw , <time> ;\n'
                + 'btb , <time> ; bsr , <time> ; bsg , <time> ; bnh , <time>```',
    "helpAllMap": 'Copier au dessus pour toutes les maps et remplacer les <time> par votre temps\nExample de Format: /tt addList "<map> , <time> ; <map> , <time> ; ..."\n'
                + "La virgule permet séparer la map de son temps\n"
                + "Le point virgule permet de passer à la prochaine map\n"
                + "Tout est mis dans le même paramètre",
    "unknowCmd" : "Commande inconnue **/tt help** pour t'aider",
    "tooMuchArg": "Trop d'argument pour la commande, **/tt help** pour t'aider",
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
    "addTimeMap": "Bien joué *{0}*, pour ton **{1}** sur *{2}*",
    "copy"      : "Transfert terminé !",
    "notFind"   : "Le joueur n'a pas été trouvé.",
    "badUrl"    : "Les urls acceptés doivent venir de www.youtube.com/ ou de twitter.com/ ou gyazo.com/ avec le format https:// et avec un maximum de 45 charactères après le nom de domaine."
                    + " Merci de le garder le plus court possible",
}

ttTextsEn = {
    "help"      :  "```<map> corresponds either to the English shortcuts for mk8dx maps and to 'week' if you want to do a tt of the week, moreover the command {0} tt maps, returns an image with the shortcuts used.\n"
                    +"<time> must follow the following pattern: x:xx.xxx; where the x's are numbers\n"
                    +"<id> matches someone's discord id otherwise it doesn't work, the tag now works too\n"
                    +"All arguments can be passed in lowercase or uppercase, the bot will read them in lowercase.\n``` "
                    +"THe first two parameters are mandatory for the followings commands, 150 or 200 choose your speed and then you choose 'ni' for shroomless time or 'shroom'\n",
    "help2"     :   "```These commands do not require any rights anyone on the server can use them\n"
                    +"Add 'ni' or '200' to acces other category, Every command will work the same in the category you ask. Exemple : /tt ni find for shroomless parts \n\n"
                    +"/tt <map> --> displays if a file exists the times of the map.\n" 
                    +"/tt <map> <time> <link> --> add your time to the <map> or replace it if there is already one, link is optionnal\n"
                    +"/tt <map> delete --> Remove your time from the map\n"
                    +"/tt addlist help --> Show addlist help\n"
                    +"/tt addlist <List> --> Add several map, go to /tt addlist help to see the requested format\n"
                    +"/tt <id> <map> --> draw difference around the player <id> on the map <map> \n"
                    +"/tt copy <idServ> --> Copy your times from server <idServ>, for only for the category you are in. Exemple : /tt ni copy <idServ> to copy your shroomless time\n"  
                    +"For the following command, you can use b ( or booster) or total to have only the booster list map or total list map\n"
                    +"/tt find --> Find all the maps where you appear\n"
                    +"/tt find <id> --> Find all maps where <id> appears\n"                 
                    +"/tt stats --> Show a classement of the server with the average position in all the maps.\n"
                    +"/tt stats time --> Show a classement of the server with the total time in all the maps.\n"
                    +"you have to have the 48 maps fill or you won't appear."
                    +"the 'week' map does not count in the stats, and you got points for every map which you are not in.```",
    "help2"     : "```The commands below require the right to manage messages on the server\n\n"
                    +"/tt create --> Create a folder for the server and store the maps there\n\n"
                    +"/tt delete <id> --> Remove all times from <id> in files\n\n"
                    +"/tt delete <map> --> Delete the file from a map \n\n"
                    +"/tt <map> delete <id> --> Remove player <id> from file <map>\n\n"
                    +"/tt <map> objective <time> --> add <time> to the objective\n\n"
                    +"/tt <map> bonus <time> --> add <time> to the objective bonus\n\n"
                    +"/tt <map> objective delete --> Removes objective time\n\n"
                    +"/tt <map> bonus delete --> Removes bonus objective time\n\n"
                    +"The commands below require the right Administrator on the server\n\n"
                    +"WARNING -> /tt delete --> Delete the server folder and what's in it, there is no verification\n```"
                    +"If you want to help to maintain this bot alive you can help Arcégis by giving even small donation to his paypal : https://paypal.me/arcegis",
    "perm"      : "You don't have the perms for this order",
    "noArg"       : "No arguments to the tt command! for more info ** /tt help **",
    "create"    : "Your Server now has a file for your TTs, you can fill them in",
    "pathExist" : "Your server already has a file, ** /tt help **, to know how to enter your times",
    "delete"    : "TT files have been deleted successfully",
    "wrongName" : "Your args is not an available command or map ** /tt help ** or ** /tt maps ** to help you",
    "noFile"    : "Your server does not have a file, use the command * {0} tt create ** to have one"
                    +" files and you can add your time.",
    "noFileMap" : "No file for this map, add a time to create it." ,
    "badFormat" : "Time in wrong format, example: **1:20.546** , or too many arguments.",
    "registred" : "Your time has been registred.",
    "allMap"    : '```/tt addList "mks , <time> ; wp , <time> ; ssc , <time> ; tr , <time>;\n'
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
    "boosterMap" : '```{}tt addList "bpp , <time> ; btc , <time> ; bcm64 , <time> ; bcmw , <time> ;\n'
                + 'btb , <time> ; bsr , <time> ; bsg , <time> ; bnh , <time>"```',
    "helpAllMap": 'COpy everything and change <time> by your time in the map wich is on the left of **,**\n'
                + 'Example of command line to add many maps: /tt addList "<map> , <time> ; <map> , <time> ; ..."\n'
                + "**,** is to separate args in the command line\n"
                + "**;** is too séparate the next command line\n"
                + 'Dont forget **"** , without them it doesnt work\n',
    "unknowCmd" : "Unknonws command **/tt help** to help you",
    "tooMuchArg": "Too many args for this command, **/tt help** to help you",
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
    "addTimeMap": "Well done *{0}* for your **{1}** on *{2}*",
    "copy"      : "Copy done!",
    "notFind"   : "The player was not find in the map",
    "badUrl"    : "Accepted urls must come from www.youtube.com/ or from twitter.com/ ou gyazo.com/ with the format https:// and with a maximum of 45 characters after the domain name."
                + " Thanks for getting the url as short as possible",
}

ttTexts = {
    "fr"    : ttTextsFr,
    "en"    : ttTextsEn
}

settingsTextsEn = {
    "noArgs"    : "No arguments for the settings command! For more info ** /settings help **",
    "help"      : "```Settings help : You can for now change your language and your prefix ( the way you call the bot )\n"
            + "/settings prefix <arg> -> This will change the prefix to <arg> and you will know use the bot with <arg>\n"
            + "/settings language <L> -> Will change the language to <L> : for now FR and EN are available.\n```",
    "tooManyArg": "Too many Arg for the command, **/settings help** to help you ",
    "wrongLanguage": "Language doesn't exist, for now only FR and EN works, **/settings help** to help you",
    "noCmd"     : "No Command with this name, **/settings help** to help you ",
    "prefix"    : "Your prefix has change to {0}",
    "language"  : "Your language has change to {0}",
    "check"     : "Your language is {0} and your prefix is {1}"
    
}

settingsTextsFr = {
    "noArgs"    : "Aucun argument pour la commande des paramètres! Pour plus d'informations ** {0} aide sur les paramètres **",
    "help"      : "``` Aide sur les paramètres: vous pouvez pour l'instant changer votre langue et votre préfixe (la façon dont vous appelez le bot) \n"
            + "/settings prefix <arg> -> Cela changera le préfixe en <arg> et vous saurez utiliser le bot avec <arg> \n"
            + "/settings language <L> -> Va changer la langue en <L>: pour l'instant FR et EN sont disponibles.\n```",
    "tooManyArg": "Trop d'arg pour la commande, **/settings help** pour vous aider",
    "wrongLanguage": "La langue n'existe pas, pour l'instant seuls FR et EN fonctionnent,**/settings help ** pour vous aider",
    "noCmd"     : "Pas de commande de ce nom , **/settings help** pour t'aider.",
    "prefix"    : "Le prefix du bot a été changé en {0}",
    "language"  : "La langue a été changé en {0}",
    "check"     : "La langue du bot est {0} et le prefix du bot est {1}"
}

settingsTexts = {
    "fr"    : settingsTextsFr,
    "en"    : settingsTextsEn
}


MK8DXTotalMap = { "mks" : "Mario Kart Stadium" , 'wp' :"Water Park" , 'ssc' : "Sweet Sweet Canyon" , 'tr' :"Thwomp Ruins" ,     # coupe Champignon
                'mc' : "Mario Circuit" , 'th' : "Toad Harbor" , 'tm' : "Twisted Mansion" , 'sgf' : "Shy Guy Falls",# coupe Fleur
                'sa' :"Sunshine Airport"  , 'ds' : "Dolphin Shoals"  , 'ed' : "Electrodrome" , 'mw' : "Mount Wario"  ,#coupe Etoile
                'cc' : "Cloudtop Cruise" , 'bdd' : 'Bone-Dry Dunes' , 'bc' : "Bowser's Castle" , 'rr' :"Rainbow Road"  ,# coupe Spéciale
                'dyc' :"Yoshi Circuit" , 'dea' :"Excitebike Arena" , 'ddd' :"Dragon Driftway" , 'dmc' :"Mute City" ,# coupe Oeuf
                'dbp' : "Baby Park" , 'dcl' :"Cheese Land" , 'dww' : "Wild Woods", 'dac' :"Animal Crossing" ,#Coupe Feuille
                'rmmm' :"Moo Moo Meadows", 'rmc' : "Mario Circuit GBA" , 'rccb' :"Cheep Cheep Beach", 'rtt' :"Toad's Turnpike" ,#coupe Carapace
                'rddd' : "Dry Dry Desert", 'rdp3' : "Donut Plains 3", 'rrry' :"Royal Raceway", 'rdkj' : 'DK Jungle',# coupe Banane
                'rws' : "Wario Stadium", 'rsl' : "Sherbet Land" ,'rmp' : 'Music Park'  ,'ryv' :"Yoshi Valley"  ,# Coupe Feuille Morte
                'rttc': "Tick-Tock Clock", 'rpps' : 'Piranha Plant Slide','rgv' :"Grumble Volcano"  , 'rrrd' :"Rainbow Road N64",#coupe Eclair
                'dwgm' :"Wario's Gold Mine", 'drr' :"Rainbow Road SNES" , 'diio' :"Ice Ice OutPost", 'dhc' : "Hyrule Circuit" ,#coupe Hyrule
                'dnbc' :"Neo Bowser City", 'drir' : "Ribbon Road", 'dsbs' :"Super Bell Subway", 'dbb' : "Big Blue", #Coupe Cloche
                "bpp" : "Tour Paris Promenade" , "btc" : "3DS Toad Circuit" , "bcm64" : "N64 Choco Mountain" , "bcmw" : "Wii Coconut Mall" ,# nouvelle première coupe
                "btb" : "Tour Tokyo Blur" , "bsr" : "DS Shroom Ridge", "bsg" : "GBA Sky Garden" , "bnh" : "Tour Ninja Hideaway", # seconde coupe
                "bnym" : "MKT New York" , "bmc3" : "SNES Mario Circuit 3" , "bkd" : "N64 Kalimari Desert" , "bwp" : "DS Flipper Waluigi", #troisième coupe
                "bss" : "MKT Sydney", "bsl" : "GBA Snow Land" , "bmg" : "WII Mushroom Gorge" , "bshs" :"Sky High Sundae", #4ème coupe
                "bll" : "London Loop", "bbl" : "Boo Lake" ,"brrm" : "Rock Rock Mountain", "bmt" : "Maple Treeway" ,  # 5ème coupe
                "bbb" : "Berlin Byways", "bpg" : "Peach Gardens", "bmm" : "Merry Mountain", "brr7" : "Rainbow Road", #6eme coupe 
                "bad" : "Amsterdam Drift" ,"brp" : "Riverside Park" , "bdks" : "DK Summit" , "byi" : "Yoshi's Island", # 7eme coupe
                "bbr" : "Bangkok Rush" , "bmc" : "DS Mario Circuit" , "bws" : "Waluigi Stadium" , "bsis" : "Singapore Speedway", # 8eme coupe
                "batd" : "Athens Dash" , "bdc" : "Daisy Cruiser" , "bmh" : "Moonview Highway" , "bscs" : "Squeaky Clean Sprint", # 9eme coupe
                "blal" : "Los Angeles Laps" , "bsw" : "Sunset Wilds" , "bkc" : "Koopa Cape" , "bvv" : "Vancouver Velocity", # 10 eme coupe
                'week' :"Map of the Week" 
}
