authors: 'Denis Salem'
categories: ''
tags: ''
title: Foire aux questions
chapter: 9
---VENC-BEGIN-PREVIEW---
---VENC-END-PREVIEW---

## Pourquoi VenC n'est officiellement supporté que par GNU/Linux?

Et bien c'est très simple camarade, comme dirait Jean-Pierre Coffe, _Les systèmes d'exploitations propriétaires, c'est de la merde!_

## Commande introuvable

VenC devrait être installé avec [pip](https://pypi.python.org/pypi/pip), dans l'environment python, côté utilisateur (pas dans le système donc). De cette façon le système à besoin de connaître l'emplacement de VenC, dont l'exécutable devrait se trouver dans _~/.local/bin_.

Sur certaine distribution GNU/Linux, comme [Archlinux](https://www.archlinux.org/) et [Gentoo](https://www.gentoo.org/), la variable d'environnement _PATH_ peut être incomplète par défaut, ce qui produit en effet une erreur type _commande introuvable_.

Dans ce cas, vous pouvez ajouter à votre _~/.bashrc_ la ligne suivante:

> export PATH=$PATH:~/.local/bin

Si le fichier n'existe pas déjà cependant, il faudra le créer.

Après ça, tapez dans le terminal actif

> source ~/.bashrc

Et voilà, ça devrait être bon :)

## Erreurs python

Normalement VenC gère toutes les erreurs et exceptions de sorte de ne pas interrompre le programme ou de vous aviser du problème de façon commode.

Si malgré tout vous obtenez des erreurs c'est probablement que votre installation n'est pas correct.

Cela arrive lorsque VenC est installé avec la version python 2 de [pip](https://pypi.python.org/pypi/pip). VenC fonctionne avec python 3, il faut donc installer VenC avec pip3.
En général, la version de [pip](https://pypi.python.org/pypi/pip) que vous utilisez par défaut correspond à la version de python également utilisé par défaut sur votre système.

En particulier sur les système basés sur debian, vous devrez installer pip3

> sudo apt-get install python3-pip

Après ça, désinstallez VenC avec la version python 2 de [pip](https://pypi.python.org/pypi/pip), et réinstallez VenC avec la version python 3 de [pip](https://pypi.python.org/pypi/pip).

> pip3 install venc --user

Ça devrait le faire!

## latex2mathml semble incomplet ou ne fonctionne pas correctement.

C'est fort possible en effet, mais ce n'est pas du ressort de VenC dans la mesure où cette fonctionnalité dépend d'une [tierce librairie](https://github.com/Code-ReaQtor/latex2mathml) développée indépendament de VenC. Cette librairie est jeune et encore en développement. Son développeur étant très réactif, si quelque chose ne fonctionne pas correctement, signalez le problème sur [la page github du projet](https://github.com/Code-ReaQtor/latex2mathml), cela devrait être alors résolu relativement rapidement!

## Je n'arrive pas à créer de sous catégories dans ma publication!

Il se peut qu'il s'agisse d'une erreur de syntaxe. Le séparateur de sous catégorie est " > ", et non pas ">".

par exemple vous devriez avoir quelque chose comme

> categories: 'Acteurs > Jean Rochefort'

au lieu de 

> categories: 'Acteurs>Jean Rochefort'

## Les sous répertoires que j'ai définis ne fonctionne pas.

Vérifiez qu'aucuns de vos sous répertoires définis manuellement dans *blog_configuration.yaml* ne commencent par '/'.

Par exemple:

.:CodeHighlight::Yaml::False::
path:
  category_directory_name: '/{category}' # Incorrect
  dates_directory_name: '%m-%Y' # Correct
  dates_sub_folders: '/' # Incorrect
  categories_sub_folders: '' # Correct
  entries_sub_folders: '{entry_title}' # Correct
:.

