# Projet : Développez une application Web en utilisant Django


*Auteur : Grégory ALLEN*

## Fonctionnalité : 

L'application permet a un utilisateur connecté de :
  - poster des avis sur des oeuvres 
  - poster des tickets demandant des avis à d'autres utilisateurs
  - répondre à des tickets d'autres utilisateurs
  - s'abonner à d'autres utilisateurs pour voir leurs avis/tickets

Il peut également modifier ses tickets/avis.

## Installation et utilisation :
  
### Créer un environnement virtuel Python : 
 
- #### En ligne de commande, se placer dans le répertoire de travail désiré :

  - sous Windows, saisir :

  `cd \chemin\vers_le\repertoire_desire` 

  - sous Linux, saisir :
   
  `cd chemin/vers_le/repertoire_desire`
     
- #### Créer un environnement virtuel dans le repertoire de travail désiré :
 
  - sous Windows, saisir :

  `python -m venv env`  

  - sous Linux, saisir :
   
  `python3 -m venv env`
   
- #### Activer l'environnement virtuel
       
  - sous Windows, saisir : 
       
  `env\Scripts\activate.bat`
       
  - sous Linux, saisir : 
      
  `source env/bin/activate`  

### Préparer l'environnement virtuel pour qu'il puisse lancer notre application

- #### Télécharger les fichiers du dépot Github et placer ces fichiers dans *chemin/vers_le/repertoire_desire/*  

- #### Récupérer les modules / packages nécessaires pour faire fonctionner notre script :
    
    Toujours en étant dans */chemin/vers_le/repertoire_desire* saisir :  
    
    `pip install -r requirements.txt`
    
### Lancer notre serveur django  

Le projet nous demandant d'inclure la base de donnée, nous allons faire un simple copier/coller du repertoire.

- #### En ligne de commande, toujours en étant dans *chemin/vers_le/repertoire_desire*, saisir :

  - sous Windows, saisir :
       
  `cd .\LITReview\`
  
  puis :
  
  `python .\manage.py runserver`
       
  - sous Linux, saisir : 
       
  `cd .\LITReview\`
  
  puis 
  
  `python3 manage.py runserver`

## Résultat attendu :  

- Se rendre à l'adresse : `localhost:8000` ou `127.0.0.1:8000`

- Une fois sur le site il est possible de s'inscrire ou se connecter.

- Une fois connecté et redirigé sur la page d'accueil, il est possible de profiter de toutes les fonctions du site.
