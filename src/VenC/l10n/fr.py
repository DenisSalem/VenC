#! /usr/bin/python3

#    Copyright 2016, 2017 Denis Salem
# 
#    This file is part of VenC.
#
#    VenC is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    VenC is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with VenC.  If not, see <http://www.gnu.org/licenses/>.

class Messages:
    blogCreated = "Votre blog a été crée!"
    themeInstalled = "Le thème à bien été installé!"
    entryWritten = "La publication a bien été ajouté!"
    fileNotFound = "{0}: Ce fichier ou ce dossier n'existe pas."
    fileAlreadyExists = "{0}: {1}: Le fichier existe déjà."
    invalidEntryFilename = "{0}: Nom de fichier invalide pour une publication"
    blogName = "Nom du blog"
    yourName = "Votre nom"
    blogDescription = "Courte description du blog"
    blogKeywords = "Quelques mots clefs qui définissent votre blog"
    aboutYou = "À propos de vous"
    license = "La licence appliquée à votre contenu"
    blogUrl = "L'url du blog"
    blogLanguage = "La langue du blog"
    yourEmail = "Votre adresse email"
    missingParams = "{0}: Paramètres manquants."
    cannotReadIn = "{0}: Impossible de lire dans {1}."
    nothingToDo = "Rien à faire."
    unknownCommand = "{0}: Commande inconnue."
    noBlogConfiguration = "Le fichier de configuration du blog n'existe pas ou vous n'avez pas les bonnes permissions."
    missingMandatoryFieldInBlogConf = "Attention, le champ \"{0}\" est manquant dans le fichier de configuration principal du blog."
    username="Nom d'utilisateur: "
    userPasswd="Mot de passe utilisateur: "
    ftpHost="Nom d'hôte FTP"
    ftpPath="Chemin absolu de votre blog sur l'hôte FTP."
    cleanFtpDirectory="Nettoyage du repertoire FTP de destination..."
    copyToFtpDirectory="Copie du blog vers le repertoire FTP de destination..."
    possibleMalformedEntry="La publication {0} est probablement mal formée... Abandon."
    possibleMalformedBlogConfiguration="Le fichier de configuration du blog est probablement mal formée... Abandon."
    blogRecompilation="Recompilation du blog locale..."
    exportArchives="Exportation locale du fil de publications de '{0}'."
    exportMainThread="Exportation locale du fil de publications principal."
    exportMainThreadRss="Exportation locale du flux RSS du fil de publications principal."
    exportCategories="Exportation locale du fil de publications de la categorie '{0}'."
    exportCategoriesRss="Exportation locale du flux RSS du fil de publications de la categorie '{0}'."
    missingMandatoryFieldInEntry="Le champ '{0}' dans l'entrée numéro {1} est manquant."
    recursiveForUnknownValue="RecursiveFor: La valeur {0} n'existe pas."
    notEnoughArgs="Paramétres manquants."
    unknownPattern="Le motif '{0}' n'existe pas."
    unknownContextual="La variable contextuel {0} n'existe pas."
    inRessource="Dans la ressource '{0}'."
    somethingGoesWrongReturnEmptyString="Une erreur s'est produite. Remplacement pas une chaine de caractère vide."
    argBlogName="Nom du blog {0}"
    argEntryName="Nom de la publication"
    argTemplateName="Nom du template"
    argInputFilename="Nom de fichier"
    blogFolderDoesntExists="Le dossier de destination n'existe pas... VenC s'en fiche et va en faire un nouveau."
    themeDescriptionDummy = "Le thème vide. Il donne une bonne base pour concevoir le votre."
    themeDescriptionGentle = "Thème mono colonne, très clair, aéré et élégant. Idéal pour un blog."
    themeDescriptionTessellation = "Thème comportant trois colonnes, très clair, aéré et élégant. Idéal pour une galerie."
    themeDoesntExists = "{0}: Ce thème n'existe pas."
    unknownTextEditor = "{0}: Éditeur de texte inconnu."
    themeName = "Nom du thème"
    entryIsEmpty = "{0}: Le contenu de la publication est vide."
    missingEntryContentInclusion="Thème invalide. Il manque l'inclusion du contenu de la publication dans entry.html et/ou rssEntry.html"
    unknownLanguage="Pygments: {0}: Langage inconnu."
    preProcess="Pré-traitement du théme et des publications..."
