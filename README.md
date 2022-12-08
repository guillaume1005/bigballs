1. Add channels to telegram
2. LINK with servers

A. LAUNCH COINMARKETCAP pumps to buy/sell

1. python scrapc.py
2. node modules/sell
3. node server

B. LAUNCH AUTOMATIC PROCESS TO ADD IMAGES

1. node modules/mintAddedSubscribe
2. use 3010 server to link the process, or make a python server# bigballs


##### VERSION 2

Fichiers importants

--> on regarde server.py
les fonctions importantes sont link_tel_token (va chercher le nom du du token sur telegram)
la deuxieme fontion importante est compute_features_add qui va analyser les images par deep learning et les comparer à celle de telegram

À FAIRE
linker le twitter (je vais retrouver le code que j'ai déjà fait et push le fichier)
clean ce dossier pcq y'a des trucs qui servent à rien
PROGRAMMER un truc qui va aussi chercher le discord et la page web (avec le nombre de visites de la page web)

--> stocker tout ça sur une bdd (typiquement mongodb), je m'occupe du server mongodb en node js pcq en python je sais pas faire encore

--> QUAND ON A UNE ALERTE DE PUMP SUR LA BLOCKCHAIN, ON REGARDE ALORS LE NOMBRE DE GENS SUR TWITTER, TELEGRAM, DISCORD, LE NB DE VISITES SUR LE SITE ET ÇA NOUS DONNE L'INFO SI C'EST UN VRAI COIN OU NON


normalement le telegram devrait suffire mais c'est quand meme intéressant d'avoir le discord, donc le plus important c'est de cleaner ce dossier

Moi je m'occupe de montrer le nombre de swaps et le nombre de holders par token aujourd'hui
